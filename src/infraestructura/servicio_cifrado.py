"""ServicioCifrado: el componente «Cifrado local» del TP3, para EC-04 (escenario 4.1 del TP2).

Cifra con AES-256-GCM, el mismo algoritmo que ofrece la Web Crypto API en la PWA. GCM además
autentica: si alguien modifica lo guardado, no se descifra.

La clave no se guarda en ningún lado: se deriva de la contraseña del usuario con PBKDF2. Así se
cumple la medida del escenario 4.1: sin las credenciales, lo guardado en el teléfono no se puede leer.
"""
from __future__ import annotations

import base64
import hashlib
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class DatosIlegibles(Exception):
    """Lo guardado no se puede descifrar: la clave no corresponde o el dato fue modificado."""


class ServicioCifrado:
    ITERACIONES = 600_000  # PBKDF2-HMAC-SHA256: el valor que recomienda OWASP
    LARGO_NONCE = 12       # 96 bits, el tamaño estándar para GCM

    def __init__(self, clave: bytes) -> None:
        self._aes = AESGCM(clave)

    @classmethod
    def desde_contrasena(cls, contrasena: str, sal: bytes,
                         iteraciones: int = ITERACIONES) -> ServicioCifrado:
        """Deriva una clave de 256 bits a partir de la contraseña y de una sal guardada en el teléfono."""
        clave = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, iteraciones, dklen=32)
        return cls(clave)

    def cifrar(self, texto: str) -> str:
        """Devuelve el texto cifrado, con un nonce nuevo al principio, en base64."""
        nonce = os.urandom(self.LARGO_NONCE)
        cifrado = self._aes.encrypt(nonce, texto.encode("utf-8"), None)
        return base64.b64encode(nonce + cifrado).decode("ascii")

    def descifrar(self, cifrado: str) -> str:
        """Devuelve el texto original, o lanza DatosIlegibles si la clave no corresponde."""
        try:
            datos = base64.b64decode(cifrado, validate=True)
            texto = self._aes.decrypt(datos[:self.LARGO_NONCE], datos[self.LARGO_NONCE:], None)
        except (InvalidTag, ValueError) as error:
            raise DatosIlegibles("No se puede leer lo guardado: la clave no corresponde.") from error
        return texto.decode("utf-8")
