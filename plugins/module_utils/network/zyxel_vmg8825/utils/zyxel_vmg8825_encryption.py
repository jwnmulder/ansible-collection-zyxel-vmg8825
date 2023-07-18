import base64
import json
import os

from . import ZyxelSessionContext

HAS_CRYPTOGRAPHY = False
CRYPTOGRAPHY_BACKEND = None
try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding, serialization
    from cryptography.hazmat.primitives.ciphers import (
        Cipher,
        algorithms,
        modes,
    )

    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
    from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

    CRYPTOGRAPHY_BACKEND = default_backend()
    HAS_CRYPTOGRAPHY = True
except ImportError:
    pass

NEED_CRYPTO_LIBRARY = (
    "zyxel_vmg8825 requires the cryptography library in order to function"
)


def load_rsa_public_key(context: ZyxelSessionContext, public_key_str: str):

    if not HAS_CRYPTOGRAPHY:
        raise ModuleNotFoundError(NEED_CRYPTO_LIBRARY)

    public_key_bytes = public_key_str.encode("ascii")
    context.router_public_key = serialization.load_pem_public_key(
        public_key_bytes, CRYPTOGRAPHY_BACKEND
    )


def zyxel_encrypt_cient_aes_key(context: ZyxelSessionContext, data: bytes) -> bytes:

    if not HAS_CRYPTOGRAPHY:
        raise ModuleNotFoundError(NEED_CRYPTO_LIBRARY)

    rsa_public_key: RSAPublicKey = context.router_public_key
    enc_data = rsa_public_key.encrypt(plaintext=data, padding=PKCS1v15())

    return enc_data


def zyxel_encrypt_request_dict(
    context: ZyxelSessionContext, request_data: dict
) -> dict:

    if not HAS_CRYPTOGRAPHY:
        raise ModuleNotFoundError(NEED_CRYPTO_LIBRARY)

    if not isinstance(request_data, dict):
        raise ValueError(
            "zyxel_encrypt_request_dict: request_data is not of type dict: "
            + str(request_data)
        )

    padder = padding.PKCS7(128).padder()

    data_str = json.dumps(request_data)
    data_bytes = data_str.encode("ascii")
    data_padded = padder.update(data_bytes) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(context.client_aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data_padded) + encryptor.finalize()

    zyxel_request_json = {
        "content": base64.b64encode(ciphertext).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
    }

    return zyxel_request_json


def zyxel_decrypt_response_dict(context: ZyxelSessionContext, response_data) -> dict:

    if not HAS_CRYPTOGRAPHY:
        raise ModuleNotFoundError(NEED_CRYPTO_LIBRARY)

    if not isinstance(response_data, dict):
        raise ValueError(
            "zyxel_decrypt_response_dict: response_data is not of type dict"
        )

    if "iv" in response_data and "content" in response_data:

        iv = base64.b64decode(response_data["iv"])[:16]

        content = response_data["content"]
        ciphertext = base64.b64decode(content)

        cipher = Cipher(algorithms.AES(context.client_aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        unpadder = padding.PKCS7(128).unpadder()

        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        plain_text = unpadder.update(decrypted_text) + unpadder.finalize()

        response_data = json.loads(plain_text)

    return response_data
