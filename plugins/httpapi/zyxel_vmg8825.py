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

# import logging
import time

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible.plugins.httpapi import HttpApiBase

try:
    import q
except ImportError:
    HASS_Q_LIB = False
else:
    HASS_Q_LIB = True

OPTIONS = {
    "format": ["text", "json"],
    "diff_match": ["line", "strict", "exact", "none"],
    "diff_replace": ["line", "block", "config"],
    "output": ["text", "json"],
}


def log_debug(msg):
    print(msg)

    if HASS_Q_LIB:
        q(msg)

    # log = logging.getLogger(__name__)
    # log.info(msg)
    # log_enabled = self._conn.get_option('enable_log')
    # if not log_enabled:
    #    return
    # if not self._log:
    #     self._log = open("/tmp/fortios.ansible.log", "a")
    # log_message = str(datetime.now())
    # log_message += ": " + str(msg) + "\n"
    # self._log.write(log_message)
    # self._log.flush()


class HttpApi(HttpApiBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._device_info = None
        # self._session_support = None
        self._conn = args[0]
        self._log = None
        self._sessionkey = None

    def update_auth(self, response, response_text):

        log_debug("update_auth")

        # update_auth is not invoked when an HTTPError occurs
        response_data = json.loads(response_text.getvalue())

        # if 'result' in response and response['result'] == 'ZCFG_SUCCESS':
        if "sessionkey" in response_data:
            self.sessionkey = response_data["sessionkey"]

        cookie = response.info().get("Set-Cookie")
        if cookie:
            return {"Cookie": cookie}

        return None

    def login(self, username, password):

        """Call a defined login endpoint to receive an authentication token."""
        if username is None or password is None:
            raise AnsibleConnectionFailure("Please provide username/password to login")

        log_debug(f"login with username '{ username }' and password")

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
        log_debug(f"login/data: {data}")
        response_data, response = self.send_request(
            data=data, path=login_path, method="POST"
        )
        log_debug(f"login/response: {response}")
        return response

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
        log_debug(
            f"logout: sessionkey={self.sessionkey},"
            f" connecion._auth={self.connection._auth}"
        )

        if self.sessionkey:
            try:
                self.send_request(
                    data=None,
                    path="/cgi-bin/UserLogout?sessionkey={self.sessionkey}",
                    method="POST",
                )
            except Exception as e:
                log_debug(f"logout error: {e}")

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
        # def send_request(self, path=None, data=None, method='GET', output=json):
        # def send_request(self, **message_kwargs):
        # Fixed headers for requests
        headers = {"Content-Type": "application/json"}
        path = message_kwargs.get("path", "/")
        method = message_kwargs.get("method", "GET")
        oid = message_kwargs.get("oid")
        # data = message_kwargs.get('data', None)

        if isinstance(data, dict):
            data = json.dumps(data)

        if oid:
            path = f"/cgi-bin/DAL?oid={oid}&sessionkey={self.sessionkey}"

        log_debug(f"send_requestB: {path, data}")

        self._display(method, "send_request/oid")

        try:
            # https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py
            response, response_data = self.connection.send(
                path, data, method=method, headers=headers
            )
            log_debug(f"2a, {response}")
            log_debug(f"2b, {response_data}")
        except HTTPError as exc:
            response = exc
            response_data = exc
            return handle_response(response, response_data)

        # # return response.status, to_text(response_data.getvalue())
        # except Exception as err:
        #     log(f"3, {err}")
        #     log(traceback.format_exc())
        #     raise Exception(err)

        # handle_response (defined separately) will take the format returned by the device
        # and transform it into something more suitable for use by modules.
        # This may be JSON text to Python dictionaries, for example.
        return handle_response(response, response_data)

        # data = to_list(data)
        # become = self._become
        # if become:
        #     self.connection.queue_message("vvvv", "firing event: on_become")
        #     data.insert(0, {"cmd": "enable", "input": self._become_pass})

        # output = message_kwargs.get("output") or "text"
        # request = request_builder(data, output)
        # headers = {"Content-Type": "application/json-rpc"}

        # _response, response_data = self.connection.send(
        #     "/command-api", request, headers=headers, method="POST"
        # )

        # try:
        #     response_data = json.loads(to_text(response_data.getvalue()))
        # except ValueError:
        #     raise ConnectionError(
        #         "Response was not valid JSON, got {0}".format(
        #             to_text(response_data.getvalue())
        #         )
        #     )

        # results = handle_response(response_data)

        # if become:
        #     results = results[1:]
        # if len(results) == 1:
        #     results = results[0]

        # return results

    def handle_httperror(self, exc):

        # Delegate to super().handle_httperror() for 401?

        # is_auth_related_code = exc.code == TOKEN_EXPIRATION_STATUS_CODE or exc.code == UNAUTHORIZED_STATUS_CODE
        # if not self._ignore_http_errors and is_auth_related_code:
        #     self.connection._auth = None
        #     self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))
        #     return True
        # False means that the exception will be passed further to the caller

        print(exc)

        # just ignore HTTPErrors if they contain json data
        content_type = exc.headers.get("Content-Type")
        if content_type != "application/json":
            return exc

        return False

    def _display(self, http_method, title, msg=""):
        pass
        # self.connection.queue_message('vvvv', 'REST:%s:%s:%s\n%s' % (http_method, self.connection._url, title, msg))

    def get_device_info(self):
        # if self._device_info:
        # return self._device_info

        device_info = {}

        device_info["network_os"] = "zyxel"
        response_data, response = self.send_request(
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
        # This method is ONLY here to support resource modules. Therefore most
        # arguments are unsupported and not present.

        session = None
        if self.supports_sessions():
            session = "ansible_%d" % int(time.time())
            candidate = ["configure session %s" % session] + candidate
        else:
            candidate = ["configure"] + candidate
        candidate.append("commit")

        try:
            responses = self.send_request(candidate)
        except ConnectionError:
            if session:
                self.send_request(["configure session %s" % session, "abort"])
            raise

        return [resp for resp in to_list(responses) if resp != "{}"]


def handle_response(response, response_data):

    content_type = response.headers.get("Content-Type")
    if content_type != "application/json":
        raise ValueError(f"Expected application/json content-type, got {content_type}")

    # log("4")
    # try:
    #     response_content = json.loads(to_text(response_data.read()))
    #     log("5")
    # except ValueError:
    #     raise ConnectionError(
    #         "Response was not valid JSON, got {0}".format(
    #             to_text(response_content.getvalue())
    #         )
    #     )
    response_data = response_data.read()
    response_data = json.loads(response_data)

    if isinstance(response, HTTPError):
        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join((error["error-message"] for error in errors))
            else:
                error_text = response_data

            q(f"A: {response_data}")
            raise ConnectionError(error_text, code=response.code)
        q("B")
        raise ConnectionError(to_text(response), code=response.code)

    return response_data, response
