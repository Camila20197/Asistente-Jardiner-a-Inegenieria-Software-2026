"""Repositorio local en memoria: listas de Python que duran mientras corre el programa.

Sirve para las pruebas y para mostrar que la persistencia se cambia sin tocar el controlador. No
cifra: no deja nada guardado en el teléfono, así que no hay datos en reposo que proteger.
"""
from __future__ import annotations

from collections.abc import Iterable

from aplicacion.puertos import RepositorioBitacora, RepositorioEspecies
from dominio.entrada_bitacora import EntradaBitacora
from dominio.especie import Especie


class RepositorioEspeciesEnMemoria(RepositorioEspecies):
    def __init__(self, catalogo: Iterable[Especie]) -> None:
        self._especies = {especie.id: especie for especie in catalogo}

    def especie(self, especie_id: int) -> Especie | None:
        return self._especies.get(especie_id)

    def todas(self) -> list[Especie]:
        return sorted(self._especies.values(), key=lambda especie: especie.nombre)


class RepositorioBitacoraEnMemoria(RepositorioBitacora):
    def __init__(self) -> None:
        self._entradas: list[EntradaBitacora] = []

    def guardar(self, entrada: EntradaBitacora) -> None:
        self._entradas.append(entrada)

    def entradas_de(self, especie_id: int, usuario_id: int) -> list[EntradaBitacora]:
        return [entrada for entrada in self._entradas
                if entrada.especie_id == especie_id and entrada.usuario_id == usuario_id]
