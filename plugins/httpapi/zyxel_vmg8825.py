# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = """
author: Ansible Networking Team
httpapi: eos
short_description: Use eAPI to run command on eos platform
description:
- This eos plugin provides low level abstraction api's for sending and receiving CLI
  commands with eos network devices.
version_added: 1.0.0
options:
  eos_use_sessions:
    type: int
    default: 1
    description:
    - Specifies if sessions should be used on remote host or not
    env:
    - name: ANSIBLE_EOS_USE_SESSIONS
    vars:
    - name: ansible_eos_use_sessions
"""
import json
import time
import q
import base64
import traceback

from datetime import datetime

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible.plugins.httpapi import HttpApiBase


OPTIONS = {
    "format": ["text", "json"],
    "diff_match": ["line", "strict", "exact", "none"],
    "diff_replace": ["line", "block", "config"],
    "output": ["text", "json"],
}


class HttpApi(HttpApiBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._device_info = None
        # self._session_support = None
        self._conn = args[0]
        self._log = None
        self._sessionkey = None

    def log(self, msg):
        # log_enabled = self._conn.get_option('enable_log')
        # if not log_enabled:
        #    return
        if not self._log:
            self._log = open("/tmp/fortios.ansible.log", "a")
        log_message = str(datetime.now())
        log_message += ": " + str(msg) + "\n"
        self._log.write(log_message)
        self._log.flush()

    def update_auth(self, response, response_text):
        cookie = response.info().get("Set-Cookie")
        if cookie:
            return {"Cookie": cookie}

        return None

    def login(self, username, password):

        """Call a defined login endpoint to receive an authentication token."""
        if username is None or password is None:
            raise Exception("Please provide username/password to login")

        self.log("login with username and password")
        q("login")

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
        q(f"data: {data}")
        response = self.send_request(data=data, path=login_path, method="POST")
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

    def logout(self):
        self.log("logout")
        q("logout")

        try:
            self.send_request(
                data=None,
                path="/cgi-bin/UserLogout?sessionkey={self.sessionkey}",
                method="POST",
            )
        except Exception as e:
            q(f"logout error: {e}")
            pass

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
        # data = message_kwargs.get('data', None)

        if isinstance(data, dict):
            data = json.dumps(data)

        q(f"send_request: {path}")
        try:
            # https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py
            response, response_content = self.connection.send(
                path, data, method=method, headers=headers
            )
            q(f"2a, {response}")
            q(f"2b, {response_content}")
        # except HTTPError as exc:
        #     q(f"3, {exc.headers}")
        #     return exc.code, exc.read()

        # return response.status, to_text(response_data.getvalue())
        except Exception as err:
            q(f"3, {err}")
            q(traceback.format_exc())
            raise Exception(err)

        q("4")
        try:
            response_content = json.loads(to_text(response_content.getvalue()))
            q("5")
        except ValueError:
            raise ConnectionError(
                "Response was not valid JSON, got {}".format(
                    to_text(response_content.getvalue())
                )
            )

        # handle_response (defined separately) will take the format returned by the device
        # and transform it into something more suitable for use by modules.
        # This may be JSON text to Python dictionaries, for example.
        return response, handle_response(response_content)

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

    def get_device_info(self):
        # if self._device_info:
        # return self._device_info

        device_info = {}

        device_info["network_os"] = "zyxel"
        data = self.send_request(data=None, path="/getBasicInformation")
        # data = json.loads(reply)

        # device_info["network_os_version"] = data["version"]
        device_info["network_os_model"] = data["ModelName"]

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


def handle_response(response):

    return response
    # if "error" in response:
    #     error = response["error"]

    #     error_text = []
    #     for data in error.get("data", []):
    #         error_text.extend(data.get("errors", []))
    #     error_text = "\n".join(error_text) or error["message"]

    #     raise ConnectionError(error_text, code=error["code"])

    # results = []

    # for result in response["result"]:
    #     if "messages" in result:
    #         results.append(result["messages"][0])
    #     elif "output" in result:
    #         results.append(result["output"].strip())
    #     else:
    #         results.append(json.dumps(result))

    # return results
