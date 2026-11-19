"""El ControladorBitacora: coordina el registro y arma la línea de tiempo (CA-01, CA-02, CU02-A1,
RF05 y RF10). Usa el repositorio en memoria como doble de prueba."""
from __future__ import annotations

import pytest

from datos_de_prueba import ACELGA, HOY, OTRA_USUARIA, TOMATE, USUARIA, nueva_entrada


def test_guarda_la_entrada_y_aparece_primera_en_la_linea_de_tiempo(controlador):  # CP-09
    controlador.registrar_entrada(TOMATE.id, "2026-03-02", "Trasplante a maceta.")

    respuesta = controlador.registrar_entrada(TOMATE.id, "2026-03-12", "Brotaron las primeras hojas.")

    linea = controlador.linea_de_tiempo(TOMATE.id).entradas
    assert respuesta.aceptada and respuesta.motivo is None
    assert linea[0] == respuesta.entrada and len(linea) == 2


@pytest.mark.parametrize("fecha, nota, motivo", [
    ("12/03/2026", "Brotes.", "Ingresá una fecha válida."),
    ("2026-03-16", "Brotes.", "La fecha no puede ser posterior a hoy."),
    ("2026-03-12", "   ", "Escribí la nota de la observación."),
])
def test_rechaza_datos_invalidos_con_su_motivo_y_no_guarda_nada(controlador, entradas, fecha, nota, motivo):  # CP-10
    respuesta = controlador.registrar_entrada(TOMATE.id, fecha, nota)

    assert (respuesta.aceptada, respuesta.motivo, respuesta.entrada) == (False, motivo, None)
    assert entradas.entradas_de(TOMATE.id, USUARIA) == []


def test_rechaza_la_entrada_de_una_especie_que_no_existe(controlador, entradas):  # CP-11
    respuesta = controlador.registrar_entrada(99, "2026-03-12", "Brotes.")

    assert (respuesta.aceptada, respuesta.motivo) == (False, "La especie no existe en el catálogo.")
    assert entradas.entradas_de(99, USUARIA) == []


def test_la_linea_de_tiempo_muestra_solo_las_entradas_propias_de_esa_especie(controlador, entradas):  # CP-12
    entradas.guardar(nueva_entrada(usuaria=OTRA_USUARIA, nota="De otra persona."))
    entradas.guardar(nueva_entrada(especie=ACELGA, nota="De la acelga."))
    propia = controlador.registrar_entrada(TOMATE.id, "2026-03-12", "Mía.").entrada

    assert controlador.linea_de_tiempo(TOMATE.id).entradas == [propia]


def test_ordena_de_la_mas_reciente_a_la_mas_vieja(controlador):  # CP-13
    for fecha, nota in [("2026-03-02", "b"), ("2026-02-20", "a"), ("2026-03-12", "c"), ("2026-03-02", "d")]:
        controlador.registrar_entrada(TOMATE.id, fecha, nota)

    notas = [entrada.nota for entrada in controlador.linea_de_tiempo(TOMATE.id).entradas]

    assert notas == ["c", "d", "b", "a"]  # con la misma fecha, arriba la que se guardó después


def test_no_hay_linea_de_tiempo_para_una_especie_que_no_existe(controlador):  # CP-14
    assert controlador.linea_de_tiempo(99) is None


def test_ofrece_las_especies_del_catalogo_para_elegir(controlador):  # CP-15
    assert [especie.nombre for especie in controlador.especies()] == ["Acelga", "Tomate perita"]


def test_expone_la_fecha_de_hoy_para_sugerirla_en_el_formulario(controlador):  # CP-16
    assert controlador.linea_de_tiempo(TOMATE.id).hoy == HOY
