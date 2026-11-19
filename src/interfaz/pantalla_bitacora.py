"""PantallaBitacora: la frontera de la HU, en el componente «Vistas de stock y bitácora» del TP3.

La página de la aplicación le habla en JSON. La pantalla no decide nada: pasa al controlador lo que
escribió la persona y muestra lo que responde, incluidos los rechazos. Conoce solo al controlador.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from aplicacion.controlador_bitacora import ControladorBitacora


class PantallaBitacora:
    def __init__(self, controlador: ControladorBitacora) -> None:
        self._controlador = controlador
        self.blueprint = Blueprint("pantalla", __name__, url_prefix="/app")
        self.blueprint.add_url_rule("/especies", view_func=self.elegir_especie)
        self.blueprint.add_url_rule("/especies/<int:especie_id>", view_func=self.mostrar_linea_de_tiempo)
        self.blueprint.add_url_rule("/especies/<int:especie_id>/entradas", view_func=self.guardar,
                                    methods=["POST"])

    def elegir_especie(self):
        """Lista las especies del catálogo local para elegir una."""
        return jsonify([{"id": especie.id, "nombre": especie.nombre}
                        for especie in self._controlador.especies()])

    def mostrar_linea_de_tiempo(self, especie_id: int):
        """Muestra la línea de tiempo de la especie, con la fecha de hoy para el formulario."""
        estado = self._controlador.linea_de_tiempo(especie_id)
        if estado is None:
            return jsonify({"motivo": "La especie no existe en el catálogo."}), 404
        return jsonify({"especie": {"id": estado.especie.id, "nombre": estado.especie.nombre},
                        "hoy": estado.hoy.isoformat(),
                        "entradas": [_entrada_a_json(entrada) for entrada in estado.entradas]})

    def guardar(self, especie_id: int):
        """Pasa la fecha y la nota al controlador y muestra la entrada guardada o el motivo del rechazo."""
        datos = request.get_json(silent=True) or {}
        respuesta = self._controlador.registrar_entrada(especie_id, str(datos.get("fecha") or ""),
                                                        str(datos.get("nota") or ""))
        if not respuesta.aceptada:
            return jsonify({"aceptada": False, "motivo": respuesta.motivo}), 422
        return jsonify({"aceptada": True, "entrada": _entrada_a_json(respuesta.entrada)}), 201


def _entrada_a_json(entrada) -> dict:
    return {"id": entrada.id, "fecha": entrada.fecha.isoformat(), "nota": entrada.nota,
            "estado_sync": entrada.estado_sync.value}
