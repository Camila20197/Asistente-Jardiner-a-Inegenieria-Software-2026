"""EntradaBitacora: una observación de campo sobre una especie (modelo de dominio del TP1).

Las reglas de una entrada válida viven acá (criterio Experto en información): cualquier camino que
cree una entrada pasa por ellas. La pantalla puede ayudar, pero el dominio es el que garantiza.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from uuid import uuid4

from dominio.especie import Especie


class EntradaInvalida(ValueError):
    """La fecha o la nota no cumplen las reglas de la HU-08 (criterio de aceptación CA-02)."""


class EstadoSync(Enum):
    """Toda entrada nace pendiente de sincronizar (EC-01). La pasa a sincronizada el Gestor de
    sincronización, que no forma parte de esta HU."""

    PENDIENTE_SYNC = "pendiente_sync"
    SINCRONIZADA = "sincronizada"


@dataclass(frozen=True)
class EntradaBitacora:
    id: str
    usuario_id: int
    especie_id: int
    fecha: date
    nota: str
    last_modified: datetime
    estado_sync: EstadoSync = EstadoSync.PENDIENTE_SYNC
    version: int = 1

    def __post_init__(self) -> None:
        """Invariante: no puede existir una entrada sin nota, ni siquiera construyéndola a mano."""
        if not self.nota.strip():
            raise EntradaInvalida("Escribí la nota de la observación.")

    @classmethod
    def registrar(cls, especie: Especie, usuario_id: int, fecha_texto: str, nota: str,
                  hoy: date, ahora: datetime) -> EntradaBitacora:
        """Crea una entrada nueva, pendiente de sincronizar, si la fecha y la nota son válidas.

        La fecha llega como la manda el selector (AAAA-MM-DD), tiene que existir en el calendario
        y no puede ser posterior a hoy. Si algo no se cumple, lanza EntradaInvalida con el motivo.
        """
        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
        except ValueError as error:
            raise EntradaInvalida("Ingresá una fecha válida.") from error
        if fecha > hoy:
            raise EntradaInvalida("La fecha no puede ser posterior a hoy.")
        return cls(str(uuid4()), usuario_id, especie.id, fecha, nota.strip(), ahora)
