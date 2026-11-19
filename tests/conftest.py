"""Preparación común. Todas las pruebas corren con la red cortada: es la forma de simular la huerta
sin señal (EC-01), y garantiza que registrar una observación no depende de la red."""
from __future__ import annotations

import socket

import pytest

from aplicacion.controlador_bitacora import ControladorBitacora
from datos_de_prueba import CATALOGO, HOY, USUARIA, Reloj
from infraestructura.repositorios_en_memoria import RepositorioBitacoraEnMemoria, RepositorioEspeciesEnMemoria


class SinSenal(OSError):
    """Lo que recibe cualquier intento de usar la red durante las pruebas."""


@pytest.fixture(autouse=True)
def sin_red(monkeypatch):
    def cortar(*args, **kwargs):
        raise SinSenal("Sin señal: la prueba intentó usar la red.")

    monkeypatch.setattr(socket.socket, "connect", cortar)
    monkeypatch.setattr(socket.socket, "connect_ex", cortar)
    monkeypatch.setattr(socket, "create_connection", cortar)
    monkeypatch.setattr(socket, "getaddrinfo", cortar)


@pytest.fixture
def entradas():
    return RepositorioBitacoraEnMemoria()


@pytest.fixture
def controlador(entradas):
    return ControladorBitacora(USUARIA, RepositorioEspeciesEnMemoria(CATALOGO), entradas,
                               hoy=lambda: HOY, ahora=Reloj())
