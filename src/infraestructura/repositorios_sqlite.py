"""Repositorio local sobre SQLite: el archivo hace de Almacén local (IndexedDB en la PWA).

La fecha y la nota de cada entrada se guardan cifradas por el Cifrado local (EC-04). Quedan en claro
solo los datos que hacen falta para buscar sin descifrar todo: los identificadores, el estado de
sincronización, la versión y la fecha de modificación.
"""
from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from contextlib import closing
from datetime import date, datetime
from pathlib import Path

from aplicacion.puertos import RepositorioBitacora, RepositorioEspecies
from dominio.entrada_bitacora import EntradaBitacora, EstadoSync
from dominio.especie import Especie
from infraestructura.servicio_cifrado import ServicioCifrado

ESQUEMA = """
CREATE TABLE IF NOT EXISTS especie (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entrada_bitacora (
    id             TEXT PRIMARY KEY,
    usuario_id     INTEGER NOT NULL,
    especie_id     INTEGER NOT NULL REFERENCES especie (id),
    datos_cifrados TEXT NOT NULL,
    estado_sync    TEXT NOT NULL,
    version        INTEGER NOT NULL,
    last_modified  TEXT NOT NULL
);
"""


def _conectar(ruta: Path | str) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.executescript(ESQUEMA)
    return conexion


class RepositorioEspeciesSQLite(RepositorioEspecies):
    def __init__(self, ruta: Path | str, catalogo: Iterable[Especie] = ()) -> None:
        """Abre el almacén y carga la copia local del catálogo (en la PWA la trae la sincronización)."""
        self._ruta = ruta
        with closing(_conectar(ruta)) as conexion:
            with conexion:  # confirma los cambios al terminar
                conexion.executemany("INSERT OR IGNORE INTO especie (id, nombre) VALUES (?, ?)",
                                     [(especie.id, especie.nombre) for especie in catalogo])

    def especie(self, especie_id: int) -> Especie | None:
        with closing(_conectar(self._ruta)) as conexion:
            fila = conexion.execute("SELECT id, nombre FROM especie WHERE id = ?", (especie_id,)).fetchone()
        return Especie(*fila) if fila else None

    def todas(self) -> list[Especie]:
        with closing(_conectar(self._ruta)) as conexion:
            filas = conexion.execute("SELECT id, nombre FROM especie ORDER BY nombre").fetchall()
        return [Especie(*fila) for fila in filas]


class RepositorioBitacoraSQLite(RepositorioBitacora):
    def __init__(self, ruta: Path | str, cifrado: ServicioCifrado) -> None:
        self._ruta = ruta
        self._cifrado = cifrado
        with closing(_conectar(ruta)):
            pass  # crea las tablas si es la primera vez

    def guardar(self, entrada: EntradaBitacora) -> None:
        datos = json.dumps({"fecha": entrada.fecha.isoformat(), "nota": entrada.nota}, ensure_ascii=False)
        with closing(_conectar(self._ruta)) as conexion:
            with conexion:  # confirma los cambios al terminar
                conexion.execute(
                    "INSERT INTO entrada_bitacora (id, usuario_id, especie_id, datos_cifrados, estado_sync, "
                    "version, last_modified) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (entrada.id, entrada.usuario_id, entrada.especie_id, self._cifrado.cifrar(datos),
                     entrada.estado_sync.value, entrada.version, entrada.last_modified.isoformat()))

    def entradas_de(self, especie_id: int, usuario_id: int) -> list[EntradaBitacora]:
        with closing(_conectar(self._ruta)) as conexion:
            filas = conexion.execute(
                "SELECT id, usuario_id, especie_id, datos_cifrados, estado_sync, version, last_modified "
                "FROM entrada_bitacora WHERE especie_id = ? AND usuario_id = ? ORDER BY rowid",
                (especie_id, usuario_id)).fetchall()
        return [self._a_entrada(fila) for fila in filas]

    def _a_entrada(self, fila: tuple) -> EntradaBitacora:
        entrada_id, usuario_id, especie_id, cifrados, estado, version, modificada = fila
        datos = json.loads(self._cifrado.descifrar(cifrados))
        return EntradaBitacora(entrada_id, usuario_id, especie_id, date.fromisoformat(datos["fecha"]),
                               datos["nota"], datetime.fromisoformat(modificada), EstadoSync(estado), version)
