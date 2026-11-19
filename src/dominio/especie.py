"""Especie: entidad de referencia del catálogo compartido (modelo de dominio del TP1)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Especie:
    """La HU-08 solo consulta que exista y usa su nombre. Sus otros atributos (meses de siembra,
    cuidados) son de HU-05 y HU-06."""

    id: int
    nombre: str
