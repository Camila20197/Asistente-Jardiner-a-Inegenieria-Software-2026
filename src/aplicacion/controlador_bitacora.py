"""ControladorBitacora: el modelo de vista de la bitácora, dentro del componente «Modelos de vista de
stock y bitácora» del TP3.

Coordina el registro y arma el estado que muestra la pantalla. No valida la fecha ni la nota: eso es
de la entidad. Tampoco conoce la red: guarda siempre en el teléfono (Local-First, DA-01).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime

from aplicacion.puertos import RepositorioBitacora, RepositorioEspecies
from dominio.entrada_bitacora import EntradaBitacora, EntradaInvalida
from dominio.especie import Especie


@dataclass(frozen=True)
class Respuesta:
    """Lo que la pantalla muestra después de guardar: la entrada aceptada o el motivo del rechazo."""

    aceptada: bool
    motivo: str | None = None
    entrada: EntradaBitacora | None = None


@dataclass(frozen=True)
class EstadoBitacora:
    """La línea de tiempo de una especie, lista para mostrar, y la fecha de hoy para el formulario."""

    especie: Especie
    entradas: list[EntradaBitacora]
    hoy: date


class ControladorBitacora:
    def __init__(self, usuario_id: int, especies: RepositorioEspecies, entradas: RepositorioBitacora,
                 hoy: Callable[[], date] = date.today,
                 ahora: Callable[[], datetime] = datetime.now) -> None:
        self._usuario_id = usuario_id
        self._especies = especies
        self._entradas = entradas
        self._hoy = hoy
        self._ahora = ahora

    def especies(self) -> list[Especie]:
        """El catálogo local, para elegir a qué especie corresponde la observación (CU02, paso 2)."""
        return self._especies.todas()

    def linea_de_tiempo(self, especie_id: int) -> EstadoBitacora | None:
        """Las entradas propias de la especie, de la más reciente a la más vieja (RF05, RF10).
        Devuelve None si la especie no existe."""
        especie = self._especies.especie(especie_id)
        if especie is None:
            return None
        entradas = self._entradas.entradas_de(especie_id, self._usuario_id)
        ordenadas = sorted(entradas, key=lambda e: (e.fecha, e.last_modified), reverse=True)
        return EstadoBitacora(especie, ordenadas, self._hoy())

    def registrar_entrada(self, especie_id: int, fecha_texto: str, nota: str) -> Respuesta:
        """Registra la observación en el teléfono (CA-01) o informa por qué no (CA-02, CU02-A1)."""
        especie = self._especies.especie(especie_id)
        if especie is None:
            return Respuesta(False, "La especie no existe en el catálogo.")
        try:
            entrada = EntradaBitacora.registrar(especie, self._usuario_id, fecha_texto, nota,
                                                self._hoy(), self._ahora())
        except EntradaInvalida as error:
            return Respuesta(False, str(error))
        self._entradas.guardar(entrada)
        return Respuesta(True, entrada=entrada)
