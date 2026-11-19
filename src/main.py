"""Punto de arranque: el único lugar que conoce las clases concretas y las arma (inyección de
dependencias). Levanta la aplicación de la HU-08 y el panel de la demostración.

    python src/main.py            # Almacén local en SQLite, cifrado, en la carpeta datos/
    python src/main.py --memoria  # el mismo flujo con el repositorio en memoria
    python src/main.py --limpio   # borra datos/ y empieza de cero
"""
from __future__ import annotations

import argparse
import os
import shutil
from collections.abc import Callable
from datetime import date, datetime, time
from pathlib import Path

from flask import Flask

from aplicacion.controlador_bitacora import ControladorBitacora
from aplicacion.puertos import RepositorioBitacora
from demo.inspector import InspectorAlmacen
from demo.panel import PanelDeDemostracion
from dominio.entrada_bitacora import EntradaBitacora, EstadoSync
from dominio.especie import Especie
from infraestructura.repositorios_en_memoria import RepositorioBitacoraEnMemoria, RepositorioEspeciesEnMemoria
from infraestructura.repositorios_sqlite import RepositorioBitacoraSQLite, RepositorioEspeciesSQLite
from infraestructura.servicio_cifrado import ServicioCifrado
from interfaz.pantalla_bitacora import PantallaBitacora

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "datos"

# La sesión del inicio de sesión (CU00) está simulada: la cuenta «usuario» precargada del TP1 ya
# entró, y con su contraseña se deriva la clave del Cifrado local.
USUARIO = 2
CONTRASENA = "huerta2026"

CATALOGO = (Especie(1, "Tomate perita"), Especie(2, "Acelga"), Especie(3, "Frutilla"), Especie(4, "Vid"))

# Las dos observaciones del maquetado del TP2, ya sincronizadas en algún día con señal.
EJEMPLOS = (
    ("3f2b8c1e-6a4d-4c1b-9e7a-2d5f8b0c1a01", date(2026, 2, 20),
     "Germinación completa, 8 de 10 semillas del lote #14."),
    ("3f2b8c1e-6a4d-4c1b-9e7a-2d5f8b0c1a02", date(2026, 3, 2),
     "Trasplante a maceta individual. Sustrato con compost propio."),
)


def crear_app(carpeta: Path = CARPETA_DATOS, en_memoria: bool = False,
              hoy: Callable[[], date] = date.today, ahora: Callable[[], datetime] = datetime.now) -> Flask:
    """Arma la aplicación. El reloj se recibe de afuera para que las pruebas usen uno fijo."""
    if en_memoria:
        especies, entradas = RepositorioEspeciesEnMemoria(CATALOGO), RepositorioBitacoraEnMemoria()
        archivo, sal, primera_vez = None, None, True
    else:
        carpeta.mkdir(parents=True, exist_ok=True)
        archivo = carpeta / "almacen_local.db"
        primera_vez = not archivo.exists()
        sal = _leer_o_crear_sal(carpeta / "sal.bin")
        especies = RepositorioEspeciesSQLite(archivo, CATALOGO)
        entradas = RepositorioBitacoraSQLite(archivo, ServicioCifrado.desde_contrasena(CONTRASENA, sal))
    if primera_vez:
        _cargar_ejemplos(entradas)

    controlador = ControladorBitacora(USUARIO, especies, entradas, hoy=hoy, ahora=ahora)
    app = Flask(__name__, static_folder=None)  # los archivos de la página los sirve el panel de la demo
    app.register_blueprint(PantallaBitacora(controlador).blueprint)
    app.register_blueprint(PanelDeDemostracion(InspectorAlmacen(archivo), sal).blueprint)
    return app


def _leer_o_crear_sal(ruta: Path) -> bytes:
    """La sal no es secreta: se guarda en el teléfono. Lo secreto es la contraseña."""
    if not ruta.exists():
        ruta.write_bytes(os.urandom(16))
    return ruta.read_bytes()


def _cargar_ejemplos(entradas: RepositorioBitacora) -> None:
    for entrada_id, fecha, nota in EJEMPLOS:
        entradas.guardar(EntradaBitacora(entrada_id, USUARIO, CATALOGO[0].id, fecha, nota,
                                         datetime.combine(fecha, time(18, 0)), EstadoSync.SINCRONIZADA))


def main(argumentos_de_consola: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Asistente de Huerta: HU-08, la bitácora sin señal.")
    parser.add_argument("--puerto", type=int, default=8000, help="puerto local (8000 por defecto)")
    parser.add_argument("--memoria", action="store_true", help="usa el repositorio en memoria en lugar de SQLite")
    parser.add_argument("--limpio", action="store_true", help="borra los datos de la demostración y empieza de cero")
    argumentos = parser.parse_args(argumentos_de_consola)
    if argumentos.limpio:
        shutil.rmtree(CARPETA_DATOS, ignore_errors=True)
    app = crear_app(en_memoria=argumentos.memoria)
    print(f"Asistente de Huerta: abrí http://127.0.0.1:{argumentos.puerto} en el navegador.")
    app.run(host="127.0.0.1", port=argumentos.puerto)


if __name__ == "__main__":
    main()
