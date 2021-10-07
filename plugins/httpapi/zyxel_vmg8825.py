# (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

# TODO check restconf.py
# TODO check checkpoint.py / HttpApi
# TODO check BaseConfigurationResource

DOCUMENTATION = """
author: Ansible Networking Team
httpapi: zyxel_vmg8825
short_description: Zyxel Web REST interface
description:
- plugin that uses the Zyxel Web REST interface to manage the router.
  Main usecase is to send commands on the /DAL interface
version_added: 1.0.0
options:
  eos_use_sessions:
    type: int
    # default: 1
    description:
    - Specifies if sessions should be used on remote host or not
    env:
    - name: ANSIBLE_EOS_USE_SESSIONS
    vars:
    - name: ansible_eos_use_sessions
"""
import base64
import json
import logging
import os

from ansible.plugins.httpapi import HttpApiBase

from ..module_utils.network.zyxel_vmg8825.utils.zyxel_vmg8825_requests import (
    ZyxelHttpApiRequests,
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.requests = ZyxelHttpApiRequests(self)

        # self._device_info = None
        # self._session_support = None
        self._log = None
        self._sessionkey = None

    def update_auth(self, response, response_text):

        logger.debug("update_auth")

        # update_auth is not invoked when an HTTPError occurs
        response_data = json.loads(response_text.getvalue())

        logger.debug("update_auth - response_data=%s", response_data)

        # if 'result' in response and response['result'] == 'ZCFG_SUCCESS':
        if "sessionkey" in response_data:
            self._sessionkey = response_data["sessionkey"]
            logger.debug("update_auth - sessiokey=%s", self._sessionkey)

        cookie = response.info().get("Set-Cookie")
        if cookie:
            logger.debug("update_auth - cookie=%s", cookie)
            return {"Cookie": cookie}

        return None

    def login(self, username, password):

        """Call a defined login endpoint to receive an authentication token."""
        if username is None or password is None:
            raise ValueError("Please provide username/password to login")

        logger.debug("login with username '%s' and password", username)

        login_path = "/UserLogin"
        data = {
            "Input_Account": username,
            "Input_Passwd": base64.b64encode(password.encode("ascii")).decode("ascii"),
            "RememberPassword": 0,
            "SHA512_password": False,
        }

        # http_response = self.r.post(f"{self.url}/UserLogin", data=json.dumps(request))
        # zyxel_response = self._process_http_response(http_response)

        # response = self.send_request(data, path=login_path)
        logger.debug("login/data: %s", data)
        response_data, response_code = self.send_request(
            data=data, path=login_path, method="POST"
        )
        logger.debug("login/response: %s, %s", response_code, response_data)

        # try:
        # This is still sent as an HTTP header, so we can set our connection's _auth
        # variable manually. If the token is returned to the device in another way,
        # you will have to keep track of it another way and make sure that it is sent
        # with the rest of the request from send_request()

        # self.connection._auth = {'X-api-token': response['token']}
        # except KeyError:
        #     raise AnsibleAuthenticationFailure(message="Failed to acquire login token.")
        # return response

        # try:
        #     self.connection._auth = {'X-chkp-sid': response_data['sid']}
        #     self.connection._session_uid = response_data['uid']
        # except KeyError:
        #     raise ConnectionError(
        #         'Server returned response without token info during connection authentication: %s' % response)

    def logout(self):
        logger.debug(
            "logout: _sessionkey=%s, connecion._auth=%s",
            self._sessionkey,
            self.connection._auth,
        )

        if self._sessionkey:
            try:
                self.send_request(
                    data=None,
                    path=f"/cgi-bin/UserLogout?sessionkey={self._sessionkey}",
                    method="POST",
                )
            except Exception as e:
                logger.debug("logout error: %s", e)

        self._sessionkey = None
        self.connection._auth = None

    # def supports_sessions(self):
    #     use_session = self.get_option("eos_use_sessions")
    #     try:
    #         use_session = int(use_session)
    #     except ValueError:
    #         pass

    #     if not bool(use_session):
    #         self._session_support = False
    #     else:
    #         if self._session_support:
    #             return self._session_support

    #         response = self.send_request("show configuration sessions")
    #         self._session_support = "error" not in response

    #     return self._session_support

    def send_request(self, data, **message_kwargs):
        return self.requests.send_request(data, **message_kwargs)

    def send_dal_request(self, data, **message_kwargs):
        return self.requests.send_dal_request(data, **message_kwargs)

    def handle_httperror(self, exc):
        return self.requests.handle_httperror(exc)

    def _display(self, http_method, title, msg=""):
        pass
        # self.connection.queue_message('vvvv', 'REST:%s:%s:%s\n%s' % (http_method, self.connection._url, title, msg))

    def get_device_info(self):
        # if self._device_info:
        # return self._device_info

        device_info = {}

        device_info["network_os"] = "zyxel"
        response_data, response_code = self.send_request(
            data=None, path="/getBasicInformation"
        )
        # data = json.loads(reply)

        # device_info["network_os_version"] = data["version"]
        device_info["network_os_model"] = response_data["ModelName"]

        return device_info
        # data = self.send_request("show hostname", output="json")
        # data = json.loads(reply)

        # device_info["network_os_hostname"] = data["hostname"]

        # self._device_info = device_info
        # return self._device_info

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
