"""Pruebas de contrato del Repositorio local: las dos implementaciones (memoria y SQLite cifrado) se
comportan igual para el controlador. Por eso se puede cambiar una por otra sin tocarlo."""
from __future__ import annotations

import pytest

from datos_de_prueba import ACELGA, CATALOGO, CLAVE, OTRA_USUARIA, TOMATE, USUARIA, nueva_entrada
from infraestructura.repositorios_en_memoria import RepositorioBitacoraEnMemoria, RepositorioEspeciesEnMemoria
from infraestructura.repositorios_sqlite import RepositorioBitacoraSQLite, RepositorioEspeciesSQLite
from infraestructura.servicio_cifrado import ServicioCifrado


@pytest.fixture(params=["memoria", "sqlite"])
def repositorios(request, tmp_path):
    if request.param == "memoria":
        return RepositorioEspeciesEnMemoria(CATALOGO), RepositorioBitacoraEnMemoria()
    ruta = tmp_path / "almacen_local.db"
    return RepositorioEspeciesSQLite(ruta, CATALOGO), RepositorioBitacoraSQLite(ruta, ServicioCifrado(CLAVE))


def test_devuelve_las_entradas_de_esa_especie_y_ese_usuario_en_orden_de_guardado(repositorios):  # CP-22
    _, entradas = repositorios
    primera, de_otra, de_acelga, segunda = (nueva_entrada(nota="a"), nueva_entrada(usuaria=OTRA_USUARIA),
                                            nueva_entrada(especie=ACELGA), nueva_entrada(nota="d"))
    vacio = entradas.entradas_de(TOMATE.id, USUARIA)
    for entrada in (primera, de_otra, de_acelga, segunda):
        entradas.guardar(entrada)

    assert vacio == []
    assert entradas.entradas_de(TOMATE.id, USUARIA) == [primera, segunda]


def test_conserva_todos_los_datos_de_la_entrada(repositorios):  # CP-23
    _, entradas = repositorios
    original = nueva_entrada(nota="Hojas con manchas: ¿hongo? Revisar el riego.")

    entradas.guardar(original)

    assert entradas.entradas_de(TOMATE.id, USUARIA) == [original]


def test_busca_especies_del_catalogo_local(repositorios):  # CP-24
    especies, _ = repositorios

    assert especies.especie(TOMATE.id) == TOMATE and especies.especie(99) is None
    assert especies.todas() == [ACELGA, TOMATE]
