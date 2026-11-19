"""Panel de la demostración: sirve la página y deja ver el archivo del teléfono tal como quedó en
disco. No es parte de la HU: la aplicación es la que atiende PantallaBitacora."""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory

from demo.inspector import InspectorAlmacen
from infraestructura.servicio_cifrado import DatosIlegibles, ServicioCifrado

ESTATICOS = Path(__file__).parent / "static"


class PanelDeDemostracion:
    def __init__(self, inspector: InspectorAlmacen, sal: bytes | None) -> None:
        self._inspector = inspector
        self._sal = sal
        self.blueprint = Blueprint("demo", __name__, static_folder=str(ESTATICOS), static_url_path="/static")
        self.blueprint.add_url_rule("/", view_func=self.pagina)
        self.blueprint.add_url_rule("/demo/almacen", view_func=self.almacen)
        self.blueprint.add_url_rule("/demo/abrir-almacen", view_func=self.abrir_almacen, methods=["POST"])

    def pagina(self):
        return send_from_directory(ESTATICOS, "index.html")

    def almacen(self):
        """Las filas del archivo, sin descifrar."""
        ruta = self._inspector.ruta
        return jsonify({"modo": "memoria" if ruta is None else "sqlite",
                        "archivo": None if ruta is None else f"{ruta.parent.name}/{ruta.name}",
                        "filas": self._inspector.filas()})

    def abrir_almacen(self):
        """Intenta leer el archivo con la contraseña que escriben en la demo (escenario 4.1 del TP2)."""
        filas = self._inspector.filas()
        if self._sal is None or not filas:
            return jsonify({"legible": False, "motivo": "No hay un archivo guardado en el teléfono."})
        contrasena = str((request.get_json(silent=True) or {}).get("contrasena") or "")
        cifrado = ServicioCifrado.desde_contrasena(contrasena, self._sal)
        try:
            datos = [cifrado.descifrar(fila["datos_cifrados"]) for fila in filas]
        except DatosIlegibles as error:
            return jsonify({"legible": False, "motivo": str(error)})
        return jsonify({"legible": True, "datos": datos})
