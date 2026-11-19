"""La entidad EntradaBitacora: las reglas de una entrada válida (CA-01 y CA-02)."""
from __future__ import annotations

from datetime import date
from uuid import UUID

import pytest

from datos_de_prueba import AHORA, HOY, TOMATE, USUARIA, nueva_entrada
from dominio.entrada_bitacora import EntradaBitacora, EntradaInvalida, EstadoSync


def test_registra_una_entrada_valida_pendiente_de_sincronizar():  # CP-01
    entrada = EntradaBitacora.registrar(TOMATE, USUARIA, "2026-03-12", "  Brotaron las primeras hojas.  ",
                                        HOY, AHORA)

    assert UUID(entrada.id).version == 4
    assert (entrada.usuario_id, entrada.especie_id, entrada.fecha, entrada.nota) == (
        USUARIA, TOMATE.id, date(2026, 3, 12), "Brotaron las primeras hojas.")
    assert (entrada.estado_sync, entrada.version, entrada.last_modified) == (EstadoSync.PENDIENTE_SYNC, 1, AHORA)


@pytest.mark.parametrize("fecha", ["", "ayer", "12/03/2026", "2026-02-30"])
def test_rechaza_una_fecha_que_no_es_valida(fecha):  # CP-02
    with pytest.raises(EntradaInvalida, match="Ingresá una fecha válida."):
        nueva_entrada(fecha=fecha)


def test_acepta_la_fecha_de_hoy():  # CP-03
    assert nueva_entrada(fecha="2026-03-15").fecha == HOY


def test_rechaza_la_fecha_de_manana():  # CP-04
    with pytest.raises(EntradaInvalida, match="La fecha no puede ser posterior a hoy."):
        nueva_entrada(fecha="2026-03-16")


@pytest.mark.parametrize("nota", ["", " \t\n "])
def test_rechaza_una_nota_vacia_o_con_solo_espacios(nota):  # CP-05
    with pytest.raises(EntradaInvalida, match="Escribí la nota de la observación."):
        nueva_entrada(nota=nota)


def test_acepta_una_nota_de_un_solo_caracter():  # CP-06
    assert nueva_entrada(nota="x").nota == "x"


def test_acepta_una_nota_larga_sin_recortarla():  # CP-07
    nota = "Riego profundo y control de pulgones. " * 130

    assert nueva_entrada(nota=nota).nota == nota.strip()


def test_no_se_puede_crear_una_entrada_sin_nota_ni_saltando_registrar():  # CP-08
    with pytest.raises(EntradaInvalida, match="Escribí la nota de la observación."):
        EntradaBitacora("3f2b8c1e-6a4d-4c1b-9e7a-2d5f8b0c1a99", USUARIA, TOMATE.id, HOY, "   ", AHORA)
