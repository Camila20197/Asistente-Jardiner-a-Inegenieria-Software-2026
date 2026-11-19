"""El programa completo, como lo arma main.py: el que se usa en la demostración. El reloj es fijo,
como en el resto de las pruebas."""
from __future__ import annotations

from flask import Flask

import main as programa
from datos_de_prueba import HOY, Reloj


def armar(carpeta, en_memoria: bool = False):
    return programa.crear_app(carpeta, en_memoria, hoy=lambda: HOY, ahora=Reloj()).test_client()


def _codigo(cliente, ruta):
    with cliente.get(ruta) as respuesta:  # cierra el archivo que manda Flask
        return respuesta.status_code


def test_arranca_con_el_catalogo_y_los_ejemplos_guardados_cifrados(tmp_path):  # CP-33
    cliente = armar(tmp_path)

    linea = cliente.get("/app/especies/1").json
    almacen = cliente.get("/demo/almacen").json

    assert [_codigo(cliente, ruta) for ruta in ("/", "/static/app.js", "/static/estilo.css")] == [200] * 3
    assert [entrada["estado_sync"] for entrada in linea["entradas"]] == ["sincronizada", "sincronizada"]
    assert len(almacen["filas"]) == 2 and b"Trasplante" not in (tmp_path / "almacen_local.db").read_bytes()


def test_al_volver_a_arrancar_conserva_lo_guardado_y_no_repite_los_ejemplos(tmp_path):  # CP-34
    armar(tmp_path).post("/app/especies/1/entradas", json={"fecha": "2026-03-12", "nota": "Brotes."})

    linea = armar(tmp_path).get("/app/especies/1").json

    assert [entrada["nota"] for entrada in linea["entradas"]][0] == "Brotes."
    assert len(linea["entradas"]) == 3


def test_con_el_repositorio_en_memoria_el_flujo_es_el_mismo_y_no_deja_archivo(tmp_path):  # CP-35
    cliente = armar(tmp_path, en_memoria=True)

    guardada = cliente.post("/app/especies/1/entradas", json={"fecha": "2026-03-12", "nota": "Brotes."})
    abrir = cliente.post("/demo/abrir-almacen", json={"contrasena": "huerta2026"}).json

    assert guardada.status_code == 201
    assert cliente.get("/demo/almacen").json == {"modo": "memoria", "archivo": None, "filas": []}
    assert abrir == {"legible": False, "motivo": "No hay un archivo guardado en el teléfono."}
    assert list(tmp_path.iterdir()) == []


def test_el_panel_de_la_demo_abre_el_archivo_solo_con_la_contrasena_de_la_cuenta(tmp_path):  # CP-36
    cliente = armar(tmp_path)

    con_otra = cliente.post("/demo/abrir-almacen", json={"contrasena": "adivinanza"}).json
    con_la_correcta = cliente.post("/demo/abrir-almacen", json={"contrasena": "huerta2026"}).json

    assert con_otra == {"legible": False, "motivo": "No se puede leer lo guardado: la clave no corresponde."}
    assert con_la_correcta["legible"] and "Trasplante" in con_la_correcta["datos"][0]


def test_las_opciones_de_la_consola_cambian_el_repositorio_y_borran_los_datos(tmp_path, monkeypatch,
                                                                              capsys):  # CP-37
    datos = tmp_path / "datos"
    datos.mkdir()
    (datos / "almacen_local.db").write_bytes(b"de una demo anterior")
    servidores = []
    monkeypatch.setattr(programa, "CARPETA_DATOS", datos)
    # En lugar de levantar el servidor, anota cómo se lo pidieron: la prueba no abre puertos.
    monkeypatch.setattr(Flask, "run", lambda app, **opciones: servidores.append(dict(opciones, app=app)))

    programa.main(["--memoria"])
    seguia = datos.exists()
    programa.main(["--memoria", "--limpio", "--puerto", "8123"])

    assert seguia and not datos.exists()
    assert [(servidor["host"], servidor["port"]) for servidor in servidores] == [("127.0.0.1", 8000),
                                                                                  ("127.0.0.1", 8123)]
    assert servidores[1]["app"].test_client().get("/demo/almacen").json["modo"] == "memoria"
    assert "http://127.0.0.1:8123" in capsys.readouterr().out
