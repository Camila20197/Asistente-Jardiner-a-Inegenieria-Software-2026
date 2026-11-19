"""Datos fijos de las pruebas. La fecha de hoy y el reloj están controlados: ninguna prueba depende
del reloj del sistema."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from dominio.entrada_bitacora import EntradaBitacora
from dominio.especie import Especie

HOY = date(2026, 3, 15)
AHORA = datetime(2026, 3, 15, 10, 30)
USUARIA = 2
OTRA_USUARIA = 3
TOMATE = Especie(1, "Tomate perita")
ACELGA = Especie(2, "Acelga")
CATALOGO = (TOMATE, ACELGA)
CLAVE = bytes(range(32))
SAL = b"sal-de-prueba-16"


class Reloj:
    """Devuelve un momento distinto en cada llamada (un minuto después del anterior)."""

    def __init__(self, inicio: datetime = AHORA) -> None:
        self._siguiente = inicio

    def __call__(self) -> datetime:
        actual = self._siguiente
        self._siguiente += timedelta(minutes=1)
        return actual


def nueva_entrada(especie: Especie = TOMATE, usuaria: int = USUARIA, fecha: str = "2026-03-12",
                  nota: str = "Brotes.", ahora: datetime = AHORA) -> EntradaBitacora:
    return EntradaBitacora.registrar(especie, usuaria, fecha, nota, HOY, ahora)
