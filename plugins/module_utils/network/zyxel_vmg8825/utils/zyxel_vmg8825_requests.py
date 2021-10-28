# (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import logging
import os

# import time

from ansible_collections.ansible.utils.plugins.module_utils.common.utils import (
    to_list,
)

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

        logger.debug("send_request: %s, %s, %s", method, path, data)

        self.httpapi._display(method, "send_request/oid")

        try:
            # https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py
            response, response_data = self.httpapi.connection.send(
                path, data, method=method, headers=headers
            )
        # except Exception as e:
        #     logger.warn("XXX 1: " + str(e))
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

    def send_dal_request(self, data, **message_kwargs):

        oid = message_kwargs.get("oid")
        oid_index = message_kwargs.get("oid_index")
        method = message_kwargs.get("method")

        if oid:
            path = "/cgi-bin/DAL?oid=%s" % (oid)
            if self.httpapi._sessionkey:
                path += "&sessionkey=%s" % (self.httpapi._sessionkey)
            if oid_index:
                path += "&Index=%s" % (oid_index)

        response_data, response_code = self.send_request(data, path=path, method=method)

        dal_result = response_data.get("result")
        if dal_result and dal_result != "ZCFG_SUCCESS":
            dal_reply_msg = response_data.get("ReplyMsg")
            dal_reply_msg_multi_lang = response_data.get("ReplyMsgMultiLang")

            msg = (
                "Server returned non successful DAL response, result=%s, ReplyMsg=%s,"
                " ReplyMsgMultiLang=%s"
                % (dal_result, dal_reply_msg, dal_reply_msg_multi_lang)
            )
            raise ConnectionError(
                msg,
                code=response_code,
                result=dal_result,
                reply_msg=dal_reply_msg,
                reply_msg_multi_lang=dal_reply_msg_multi_lang,
            )

        return response_data, response_code

    def handle_httperror(self, exc):

        logger.warning("handle_httperror, exc=%s", exc)

        content_type = exc.headers.get("Content-Type")
        if content_type == "application/json":
            # propogate exceptions to users as the response
            # body might contain useful information
            return exc

        # returning false will make Ansible raise an HTTPError
        # which is than handled in send_request
        return False

    # from
    # def handle_httperror(self, exc):
    #     """
    #     propogate exceptions to users
    #     :param exc: Exception
    #     """
    #     self.log('Exception thrown from handling http: ' + to_text(exc))

    #     return exc

    def dal_get(self, oid):
        response_data, response_code = self.send_dal_request(
            oid=oid, method="GET", data=None
        )
        data = response_data["Object"]
        return data

    def dal_put(self, oid, data):
        response_data, response_code = self.send_dal_request(
            oid=oid, method="PUT", data=data
        )
        return response_data

    def dal_post(self, oid, data):
        response_data, response_code = self.send_dal_request(
            oid=oid, method="POST", data=data
        )
        return response_data

    def dal_delete(self, oid, index):
        response_data, response_code = self.send_dal_request(
            oid=oid, method="POST", oid_index=index
        )
        return response_data

    def edit_config(self, candidate):
        logger.info("edit_config, candidate=%s", candidate)

        results = []
        requests = []

        for cmd in to_list(candidate):
            data = cmd.get("data")
            oid = cmd.get("oid")
            oid_index = cmd.get("oid_index")
            method = cmd.get("method")

            results.append(
                self.send_dal_request(
                    data=data, oid=oid, oid_index=oid_index, method=method
                )
            )
            requests.append(cmd)

        resp = {}
        resp["request"] = requests
        resp["response"] = results
        return resp

        # return [resp for resp in to_list(responses) if resp != "{}"]


def handle_response(method, path, response, response_data):

    response_code = response.code
    content_type = response.headers.get("Content-Type")
    if content_type != "application/json":
        raise ConnectionError(
            "Error while sending '%s' request to '%s'. Expected application/json"
            " content-type, response_code=%s, content_type=%s"
            % (method, path, response_code, content_type),
            code=response_code,
        )

    response_data = response_data.read()
    response_data = json.loads(response_data)

    logger.debug(
        "handle_response: %s, %s, %s, %s" % (method, response_code, path, response_data)
    )

    if isinstance(response, HTTPError):

        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join((error["error-message"] for error in errors))
            else:
                error_text = response_data
        else:
            error_text = to_text(response)

        msg = "Server returned error response, code=%s, error_text=%s" % (
            response_code,
            error_text,
        )
        raise ConnectionError(msg, code=response_code)

    return response_data, response.code
