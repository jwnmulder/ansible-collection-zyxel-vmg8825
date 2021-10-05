# (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import logging
import os

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError

# pylint: disable-all
# pyright: reportMissingImports=false
from ansible.module_utils.six.moves.urllib.error import HTTPError

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


class ZyxelHttpApiRequests(object):
    def __init__(self, httpapi):
        self.httpapi = httpapi

    def send_request(self, data, **message_kwargs):
        # Fixed headers for requests
        headers = {"Content-Type": "application/json"}
        path = message_kwargs.get("path", "/")
        method = message_kwargs.get("method", "GET")

        if isinstance(data, dict):
            data = json.dumps(data)

        logger.debug(f"send_request: {method, path, data}")

        self.httpapi._display(method, "send_request/oid")

        try:
            # https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py
            response, response_data = self.httpapi.connection.send(
                path, data, method=method, headers=headers
            )
        except HTTPError as exc:
            response = exc
            response_data = exc
            return handle_response(method, path, response, response_data)

        # # return response.status, to_text(response_data.getvalue())
        # except Exception as err:
        #     log(f"3, {err}")
        #     log(traceback.format_exc())
        #     raise Exception(err)

        # handle_response (defined separately) will take the format returned by the device
        # and transform it into something more suitable for use by modules.
        # This may be JSON text to Python dictionaries, for example.
        return handle_response(method, path, response, response_data)

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

    def send_dal__request(self, data, **message_kwargs):
        oid = message_kwargs.get("oid")
        oid_index = message_kwargs.get("oid_index")

        if oid:
            path = f"/cgi-bin/DAL?oid={oid}"
            if self.httpapi._sessionkey:
                path += f"&sessionkey={self.httpapi._sessionkey}"
            if oid_index:
                path += f"&Index={oid_index}"

        return self.send_request(data, path=path, **message_kwargs)

    def handle_httperror(self, exc):

        # Delegate to super().handle_httperror() for 401?

        # is_auth_related_code = exc.code == TOKEN_EXPIRATION_STATUS_CODE or exc.code == UNAUTHORIZED_STATUS_CODE
        # if not self._ignore_http_errors and is_auth_related_code:
        #     self.connection._auth = None
        #     self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))
        #     return True
        # False means that the exception will be passed further to the caller

        logger.warning(exc)

        # just ignore HTTPErrors if they contain json data
        content_type = exc.headers.get("Content-Type")
        if content_type != "application/json":
            return exc

        return False

    def dal_get(self, oid):
        response_data, response_code = self.send_dal__request(
            oid=oid, method="GET", data=None
        )
        data = response_data["Object"]
        return data

    def dal_put(self, oid, data):
        response_data, response_code = self.send_dal__request(
            oid=oid, method="PUT", data=data
        )
        return response_data

    def dal_post(self, oid, data):
        response_data, response_code = self.send_dal__request(
            oid=oid, method="POST", data=data
        )
        return response_data

    def dal_delete(self, oid, index):
        response_data, response_code = self.send_dal__request(
            oid=oid, method="POST", oid_index=index
        )
        return response_data


def handle_response(method, path, response, response_data):

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

    logger.debug(f"handle_response: {method, path, response_data}")

    if isinstance(response, HTTPError):
        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join((error["error-message"] for error in errors))
            else:
                error_text = response_data

            logger.debug("A: %s", response_data)
            raise ConnectionError(error_text, code=response.code)
        logger.debug("B")
        raise ConnectionError(to_text(response), code=response.code)

    return response_data, response.code
