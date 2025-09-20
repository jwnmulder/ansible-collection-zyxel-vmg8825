# (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
author: Jan-Willem Mulder (@jwnmulder)
name: zyxel_vmg8825
short_description: HttpApi Plugin for Zyxel VMG 8825
description:
- plugin that uses the Zyxel Web REST interface to manage the router.
  Main usecase is to send commands on the /DAL interface
version_added: 0.1.0
"""
import base64
import json
import logging
import os

from ansible.plugins.httpapi import HttpApiBase

from ..module_utils.network.zyxel_vmg8825.utils.zyxel_vmg8825_requests import (
    ZyxelSessionContext,
    ZyxelRequests,
    zyxel_encrypt_request_dict,
    zyxel_decrypt_response_dict,
)

from ..module_utils.network.zyxel_vmg8825.utils.zyxel_vmg8825_encryption import (
    load_rsa_public_key,
    zyxel_encrypt_cient_aes_key,
)

OPTIONS = {
    "format": ["text", "json"],
    "diff_match": ["line", "strict", "exact", "none"],
    "diff_replace": ["line", "block", "config"],
    "output": ["text", "json"],
}


logger = logging.getLogger(__name__)
if os.environ.get("ANSIBLE_DEBUG") is not None:
    logger.setLevel(logging.DEBUG)

try:
    import q
except ImportError:
    HASS_Q_LIB = False
else:
    HASS_Q_LIB = True


class RequestsHandler(logging.Handler):
    def emit(self, record):
        if HASS_Q_LIB:
            msg = record.getMessage()
            # pylint: disable=not-callable
            q(msg)


logger.addHandler(RequestsHandler())


class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super().__init__(connection)

        self.context = ZyxelSessionContext()

        if self.context.encrypted_payloads is None:
            use_ssl = connection.get_option("use_ssl")
            if use_ssl is False:
                self.context.encrypted_payloads = True

        self.requests = ZyxelRequests(self, self.context)

        self._device_info = None

    def update_auth(self, response, response_text):
        response_code = response.code

        # update_auth is invoked
        # - after a successful login but
        # - not after an unseccessful login
        # - after a successful URL call (200 response)
        # - after an unseccessul URL call (e.g. 403 response when POST is disallowed on a resource)

        content_type = response.headers.get("Content-Type")
        logger.debug(
            "update_auth: response_code=%s, content_type=%s",
            response_code,
            content_type,
        )

        sessionkey = None
        if content_type == "application/json":
            response_data = json.loads(response_text.getvalue())

            # data here is not yet decrypted
            if self.context.encrypted_payloads:
                response_data = zyxel_decrypt_response_dict(self.context, response_data)

            logger.debug("update_auth - response_data=%s", response_data)

            # if 'result' in response and response['result'] == 'ZCFG_SUCCESS':
            sessionkey = response_data.get("sessionkey")
            if sessionkey:
                self.context.sessionkey = sessionkey

        cookie = response.info().get("Set-Cookie")

        if cookie or sessionkey:
            logger.debug(
                "update_auth - sessionkey=%s, cookie=%s",
                self.context.sessionkey,
                cookie,
            )

        if cookie:
            return {"Cookie": cookie}

        return None

    def login(self, username, password):
        """Call a defined login endpoint to receive an authentication token."""
        if username is None or password is None:
            raise ValueError("Please provide username/password to login")

        logger.debug("login with username '%s' and password", username)

        login_path = "/UserLogin"
        login_request_data = {
            "Input_Account": username,
            "Input_Passwd": base64.b64encode(password.encode("ascii")).decode("ascii"),
            "RememberPassword": 0,
            "SHA512_password": False,
        }

        logger.debug("login/request: %s", login_request_data)

        self.detect_router_api_capabilities()
        if self.context.encrypted_payloads:
            self._load_public_key()
            self.context.client_aes_key = os.urandom(32)

            login_request_data = zyxel_encrypt_request_dict(
                self.context, login_request_data
            )

            # Encrypt the aes key with RSA pubkey of the device
            enc_aes_key = zyxel_encrypt_cient_aes_key(
                self.context, base64.b64encode(self.context.client_aes_key)
            )
            login_request_data["key"] = base64.b64encode(enc_aes_key).decode("ascii")

            logger.debug("login/request-encrypted: %s", login_request_data)

        response_data, response_code = self.send_request(
            data=login_request_data, path=login_path, method="POST"
        )

        logger.debug(
            "login/response: response_code=%s, context.session_key=%s, response_data=%s",
            response_code,
            self.context.sessionkey,
            response_data,
        )

    def logout(self):
        logger.debug(
            "logout: context.sessionkey=%s, connection._auth=%s",
            self.context.sessionkey,
            self.connection._auth,
        )

        if self.context.sessionkey:
            try:
                self.send_request(
                    data=None,
                    path="/cgi-bin/UserLogout",
                    method="POST",
                    sessionkey=self.context.sessionkey,
                )
            except Exception as e:
                logger.debug("logout error: %s", e)

        self.context.sessionkey = None
        self.connection._auth = None

    def detect_router_api_capabilities(self):
        # In certain situations, Zyxel devices use encrypted payloads for some
        # requests and responses. If encryption is used depends on firmware versions
        # and response types (200 responses might be encrypted while 401 are not).

        # Sometimes it can be determined based on ansible config. E.g. when overriding automatic
        # detection or when HTTP is used

        if (
            self.context.encrypted_payloads is None
            or self.context.sessionkey_method is None
        ):
            # In all other cases, lets try some dynamic detection methods
            info = self.get_device_info()

            software_version = info["network_os_version"]
            # Starting from an certain version (not sure which one), HTTPS requests and responses became encrypted.
            # This was only required for HTTP plain text communication before

            # HTTP  + unecrpyted msg  : Never supported by Zyxel
            # HTTPS + unencrypted msg : Was working on V5.50(ABPY.1)b16_20210525
            # HTTP  + encrypted msg   : Supported by Zyxel but not by this library
            # HTTPS + encrypted msg   : Required starting from V5.50(ABPY.1)b21_20230112
            software_version_major = int(software_version[1:2])
            software_version_minor = int(software_version[3:5])
            software_build = int(software_version[14:16])

            if software_version_major > 5 or (
                software_version_major == 5
                and software_version_minor >= 50
                and software_build >= 21
            ):
                encrypted_payloads = True
                sessionkey_method = ZyxelSessionContext.SESSIONKEY_METHOD_CSRF_TOKEN
            else:
                encrypted_payloads = False
                sessionkey_method = ZyxelSessionContext.SESSIONKEY_METHOD_QUERY_PARAM

            # respect overrides
            if self.context.encrypted_payloads is None:
                self.context.encrypted_payloads = encrypted_payloads

            if self.context.sessionkey_method is None:
                self.context.sessionkey_method = sessionkey_method

    def send_request(self, data, **message_kwargs):
        return self.requests.send_request(data, **message_kwargs)

    def send_dal_request(self, data, **message_kwargs):
        return self.requests.send_dal_request(data, **message_kwargs)

    def handle_httperror(self, exc):
        return self.requests.handle_httperror(exc)

    def _display(self, http_method, title, msg=""):
        pass
        # self.connection.queue_message('vvvv', 'REST:%s:%s:%s\n%s' % (http_method, self.connection._url, title, msg))

    def _load_public_key(self):
        if not self.context.router_public_key:
            response_data, response_code = self.send_request(
                data=None, path="/getRSAPublickKey"
            )

            public_key_str = str(response_data["RSAPublicKey"])

            # Not sure why but Zyxel is escaping some characters that should not be escaped
            public_key_str = public_key_str.replace("\\/", "/")

            load_rsa_public_key(self.context, public_key_str)

    def get_device_info(self):
        if self._device_info:
            return self._device_info

        device_info = {}

        device_info["network_os"] = "zyxel"
        response_data, response_code = self.send_request(
            data=None, path="/getBasicInformation"
        )
        # data = json.loads(reply)

        device_info["network_os_version"] = response_data["SoftwareVersion"]
        device_info["network_os_model"] = response_data["ModelName"]

        # device_info["network_os_hostname"] = data["hostname"]

        self._device_info = device_info
        return self._device_info

    def dal_get(self, oid):
        return self.requests.dal_get(oid)

    def dal_put(self, oid, data):
        return self.requests.dal_put(oid, data)

    def dal_post(self, oid, data):
        return self.requests.dal_post(oid, data)

    def dal_delete(self, oid, index):
        return self.requests.dal_delete(oid, index)

    def get_device_operations(self):
        return {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": False,
            "supports_commit_comment": False,
            "supports_multiline_delimiter": False,
            "supports_diff_match": False,
            "supports_diff_ignore_lines": False,
            "supports_generate_diff": False,
            "supports_replace": False,
        }

    def get_capabilities(self):
        result = {}
        # result["rpc"] = []
        result["device_info"] = self.get_device_info()
        result["device_operations"] = self.get_device_operations()
        result.update(OPTIONS)
        result["network_api"] = "zyxel"

        return json.dumps(result)

    # Shims for resource module support
    def get(self, command, output=None):
        # This method is ONLY here to support resource modules. Therefore most
        # arguments are unsupported and not present.

        return self.send_request(data=command, output=output)

    def edit_config(self, candidate):
        return self.requests.edit_config(candidate)
