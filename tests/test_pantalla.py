"""La frontera PantallaBitacora: traduce los pedidos de la página al controlador y muestra sus
respuestas, sin decidir nada. Se prueba con el cliente de pruebas de Flask, sin navegador: los
criterios de aceptación se prueban sobre el controlador y la entidad, no a través de la pantalla."""
from __future__ import annotations

import pytest
from flask import Flask

from aplicacion.controlador_bitacora import ControladorBitacora
from datos_de_prueba import HOY, TOMATE, USUARIA, Reloj
from infraestructura.repositorios_en_memoria import RepositorioBitacoraEnMemoria, RepositorioEspeciesEnMemoria
from interfaz.pantalla_bitacora import PantallaBitacora


def cliente_de(controlador: ControladorBitacora):
    app = Flask(__name__)
    app.register_blueprint(PantallaBitacora(controlador).blueprint)
    return app.test_client()


@pytest.fixture
def pantalla(controlador):
    return cliente_de(controlador)


def test_la_pantalla_muestra_la_linea_de_tiempo_y_guarda_una_entrada(pantalla):  # CP-30
    especies = pantalla.get("/app/especies").json
    antes = pantalla.get(f"/app/especies/{TOMATE.id}").json

    guardada = pantalla.post(f"/app/especies/{TOMATE.id}/entradas", json={"fecha": "2026-03-12", "nota": "Brotes."})

    despues = pantalla.get(f"/app/especies/{TOMATE.id}").json
    assert [especie["nombre"] for especie in especies] == ["Acelga", "Tomate perita"]
    assert (antes["hoy"], antes["entradas"]) == ("2026-03-15", [])
    assert guardada.status_code == 201 and guardada.json["entrada"]["estado_sync"] == "pendiente_sync"
    assert [entrada["nota"] for entrada in despues["entradas"]] == ["Brotes."]


@pytest.mark.parametrize("cuerpo, motivo", [
    ({"fecha": "2026-03-16", "nota": "Brotes."}, "La fecha no puede ser posterior a hoy."),
    (None, "Ingresá una fecha válida."),
    ({"nota": "Brotes."}, "Ingresá una fecha válida."),
    ({"fecha": "2026-03-12"}, "Escribí la nota de la observación."),
], ids=["fecha futura", "sin datos", "sin fecha", "sin nota"])
def test_la_pantalla_muestra_el_rechazo_que_decide_el_dominio(pantalla, cuerpo, motivo):  # CP-31
    respuesta = pantalla.post(f"/app/especies/{TOMATE.id}/entradas", json=cuerpo)

    assert (respuesta.status_code, respuesta.json) == (422, {"aceptada": False, "motivo": motivo})


def test_la_pantalla_no_muestra_especies_que_no_estan_en_el_catalogo():  # CP-32
    vacia = cliente_de(ControladorBitacora(USUARIA, RepositorioEspeciesEnMemoria(()), RepositorioBitacoraEnMemoria(),
                                           hoy=lambda: HOY, ahora=Reloj()))

    assert vacia.get("/app/especies").json == []
    pedida = vacia.get(f"/app/especies/{TOMATE.id}")
    assert (pedida.status_code, pedida.json) == (404, {"motivo": "La especie no existe en el catálogo."})
