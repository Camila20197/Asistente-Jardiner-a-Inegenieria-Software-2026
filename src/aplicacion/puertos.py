"""Interfaces que usa el controlador: el Repositorio local del TP3, detrás de interfaces para poder
cambiar dónde se guarda sin tocar el controlador (DA-01, patrón Repository)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from dominio.entrada_bitacora import EntradaBitacora
from dominio.especie import Especie


class RepositorioEspecies(ABC):
    """La copia local del catálogo de especies."""

    @abstractmethod
    def especie(self, especie_id: int) -> Especie | None:
        """Devuelve la especie, o None si no está en el catálogo."""

    @abstractmethod
    def todas(self) -> list[Especie]:
        """Devuelve todas las especies, ordenadas por nombre."""


class RepositorioBitacora(ABC):
    """Las entradas de la bitácora guardadas en el teléfono."""

    @abstractmethod
    def guardar(self, entrada: EntradaBitacora) -> None:
        """Guarda una entrada nueva."""

    @abstractmethod
    def entradas_de(self, especie_id: int, usuario_id: int) -> list[EntradaBitacora]:
        """Devuelve las entradas de esa especie escritas por ese usuario, en orden de guardado."""
