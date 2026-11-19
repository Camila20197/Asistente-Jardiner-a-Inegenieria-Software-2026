"""Mira el archivo del Almacén local tal como quedó en disco, sin la contraseña: lo que vería alguien
que tuviera el teléfono en la mano. Es solo para la demostración, no es parte de la HU."""
from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


class InspectorAlmacen:
    def __init__(self, ruta: Path | None) -> None:
        self.ruta = ruta

    def filas(self) -> list[dict]:
        """Las entradas guardadas, de la más nueva a la más vieja, con la fecha y la nota cifradas."""
        if self.ruta is None or not self.ruta.exists():
            return []
        with closing(sqlite3.connect(f"file:{self.ruta}?mode=ro", uri=True)) as conexion:
            filas = conexion.execute(
                "SELECT e.id, s.nombre, e.datos_cifrados, e.estado_sync, e.version, e.last_modified "
                "FROM entrada_bitacora e JOIN especie s ON s.id = e.especie_id ORDER BY e.rowid DESC").fetchall()
        claves = ("id", "especie", "datos_cifrados", "estado_sync", "version", "last_modified")
        return [dict(zip(claves, fila)) for fila in filas]
