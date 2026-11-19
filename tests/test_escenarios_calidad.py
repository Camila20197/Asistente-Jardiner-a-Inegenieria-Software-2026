"""Las medidas de los escenarios de calidad que alcanzan a la HU, sobre el Almacén local real
(SQLite) y el Cifrado local real:

- EC-01 (escenario 3.1 del TP2): sin red, el 100% de las cargas se guarda en el teléfono, en menos
  de 1 segundo, y queda visible como pendiente de sincronizar.
- EC-04 (escenario 4.1 del TP2): en el teléfono, sin la contraseña, lo guardado no se puede leer.
"""
from __future__ import annotations

import socket
import time

import pytest

from aplicacion.controlador_bitacora import ControladorBitacora
from datos_de_prueba import CATALOGO, HOY, SAL, TOMATE, USUARIA, Reloj
from dominio.entrada_bitacora import EstadoSync
from infraestructura.repositorios_sqlite import RepositorioBitacoraSQLite, RepositorioEspeciesSQLite
from infraestructura.servicio_cifrado import DatosIlegibles, ServicioCifrado


def armar_telefono(carpeta, contrasena: str = "huerta2026") -> ControladorBitacora:
    """El teléfono como lo arma main.py: SQLite y la clave derivada de la contraseña."""
    ruta = carpeta / "almacen_local.db"
    cifrado = ServicioCifrado.desde_contrasena(contrasena, SAL)
    return ControladorBitacora(USUARIA, RepositorioEspeciesSQLite(ruta, CATALOGO),
                               RepositorioBitacoraSQLite(ruta, cifrado), hoy=lambda: HOY, ahora=Reloj())


def test_la_red_esta_cortada_durante_las_pruebas():  # CP-25
    with pytest.raises(OSError, match="Sin señal"):
        socket.create_connection(("127.0.0.1", 9), timeout=1)


def test_sin_red_el_100_por_ciento_de_las_cargas_se_guarda_en_menos_de_1_segundo(tmp_path):  # CP-26
    telefono = armar_telefono(tmp_path)
    duraciones, aceptadas = [], 0

    for numero in range(100):
        inicio = time.perf_counter()
        aceptadas += telefono.registrar_entrada(TOMATE.id, "2026-03-12", f"Observación {numero}").aceptada
        duraciones.append(time.perf_counter() - inicio)

    linea = telefono.linea_de_tiempo(TOMATE.id).entradas
    assert aceptadas == 100 and max(duraciones) < 1.0
    assert len(linea) == 100 and all(entrada.estado_sync is EstadoSync.PENDIENTE_SYNC for entrada in linea)


def test_lo_guardado_sin_red_sigue_ahi_al_reabrir_la_aplicacion(tmp_path):  # CP-27
    guardada = armar_telefono(tmp_path).registrar_entrada(TOMATE.id, "2026-03-12", "Brotes.").entrada

    reabierto = armar_telefono(tmp_path)

    assert reabierto.linea_de_tiempo(TOMATE.id).entradas == [guardada]


def test_en_el_archivo_del_telefono_la_fecha_y_la_nota_no_estan_en_claro(tmp_path):  # CP-28
    armar_telefono(tmp_path).registrar_entrada(TOMATE.id, "2026-03-12", "Pulgones en el envés de las hojas")

    contenido = (tmp_path / "almacen_local.db").read_bytes()  # el archivo, como lo vería quien tenga el teléfono

    assert b"Pulgones" not in contenido and b"2026-03-12" not in contenido


def test_sin_la_contrasena_lo_guardado_no_se_puede_leer(tmp_path):  # CP-29
    armar_telefono(tmp_path).registrar_entrada(TOMATE.id, "2026-03-12", "Pulgones.")

    intruso = armar_telefono(tmp_path, contrasena="adivinanza")

    with pytest.raises(DatosIlegibles):
        intruso.linea_de_tiempo(TOMATE.id)
