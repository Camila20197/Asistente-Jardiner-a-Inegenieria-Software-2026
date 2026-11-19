"""El ServicioCifrado (Cifrado local del TP3): AES-256-GCM con la clave derivada de la contraseña."""
from __future__ import annotations

import base64

import pytest

from datos_de_prueba import CLAVE, SAL
from infraestructura.servicio_cifrado import DatosIlegibles, ServicioCifrado


def test_descifra_lo_que_cifro():  # CP-17
    cifrado = ServicioCifrado(CLAVE)

    assert cifrado.descifrar(cifrado.cifrar("Brotes en la maceta 3, ñandú incluido.")) == \
        "Brotes en la maceta 3, ñandú incluido."


def test_el_mismo_texto_cifrado_dos_veces_da_resultados_distintos():  # CP-18
    cifrado = ServicioCifrado(CLAVE)

    primero, segundo = cifrado.cifrar("Riego."), cifrado.cifrar("Riego.")

    assert primero != segundo
    assert cifrado.descifrar(primero) == cifrado.descifrar(segundo) == "Riego."


def test_con_otra_clave_no_se_puede_leer():  # CP-19
    guardado = ServicioCifrado(CLAVE).cifrar("Riego.")

    with pytest.raises(DatosIlegibles, match="la clave no corresponde"):
        ServicioCifrado(bytes(32)).descifrar(guardado)


def _cambiar_un_byte(guardado: str) -> str:
    datos = bytearray(base64.b64decode(guardado))
    datos[-1] ^= 1
    return base64.b64encode(bytes(datos)).decode("ascii")


@pytest.mark.parametrize("estropear", [_cambiar_un_byte, lambda guardado: "esto no es base64!"],
                         ids=["un byte cambiado", "texto que no es base64"])
def test_si_lo_guardado_fue_modificado_no_se_descifra(estropear):  # CP-20
    cifrado = ServicioCifrado(CLAVE)

    with pytest.raises(DatosIlegibles):
        cifrado.descifrar(estropear(cifrado.cifrar("Riego.")))


def test_la_clave_sale_de_la_contrasena_y_de_la_sal():  # CP-21
    guardado = ServicioCifrado.desde_contrasena("huerta2026", SAL, iteraciones=1000).cifrar("Riego.")

    assert ServicioCifrado.desde_contrasena("huerta2026", SAL, iteraciones=1000).descifrar(guardado) == "Riego."
    with pytest.raises(DatosIlegibles):
        ServicioCifrado.desde_contrasena("huerta2025", SAL, iteraciones=1000).descifrar(guardado)
