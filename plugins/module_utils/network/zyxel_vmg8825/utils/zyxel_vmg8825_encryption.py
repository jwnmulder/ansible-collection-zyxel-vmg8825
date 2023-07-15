from . import ZyxelSessionContext

from ansible.errors import AnsibleError

HAS_CRYPTOGRAPHY = False
CRYPTOGRAPHY_BACKEND = None
try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.hmac import HMAC
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import (
        Cipher as C_Cipher,
        algorithms,
        modes,
    )

    CRYPTOGRAPHY_BACKEND = default_backend()
    HAS_CRYPTOGRAPHY = True
except ImportError:
    pass

NEED_CRYPTO_LIBRARY = (
    "zyxel_vmg8825 requires the cryptography library in order to function"
)


def zyxel_encrypt_request(context: ZyxelSessionContext, request_data):

    if not HAS_CRYPTOGRAPHY:
        raise AnsibleError(NEED_CRYPTO_LIBRARY)

    if not isinstance(request_data, dict):
        raise ValueError("request_data is not of type dict")

    # iv = get_random_bytes(AES.block_size)

    # cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
    # content = cipher.encrypt(pad(json.dumps(request_data).encode("ascii"), 16))

    # request = {
    #     "content": base64.b64encode(content).decode("ascii"),
    #     "iv": base64.b64encode(iv).decode("ascii"),
    # }

    # return request
    return request_data


def zyxel_decrypt_response(response_data):

    if not HAS_CRYPTOGRAPHY:
        raise AnsibleError(NEED_CRYPTO_LIBRARY)

    if not isinstance(response_data, dict):
        raise ValueError("response_data is not of type dict")

    result = response_data
    # if "iv" in response_data and "content" in response_data:

    #     content = response_data["content"]
    #     iv = base64.b64decode(response_data["iv"])[:16]

    #     cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
    #     decrypted_text = unpad(cipher.decrypt(base64.b64decode(content)), 16)
    #     result = json.loads(decrypted_text)

    return result
