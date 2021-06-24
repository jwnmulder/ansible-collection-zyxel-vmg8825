# https://github.com/ansible-collections/community.network/blob/main/plugins/module_utils/network/avi/ansible_utils.py
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import logging
import os
import traceback

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection
from ansible.module_utils.connection import ConnectionError

ZYXEL_LIB_NAME = "zyxelclient_vmg8825"
ZYXEL_LIB_ERR = None
try:
    from zyxelclient_vmg8825.httpclient import ZyxelResponse

    # from zyxelclient_vmg8825.factory import ZyxelClientFactory
except ImportError:
    ZYXEL_LIB_ERR = traceback.format_exc()

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


class ZyxelCheckModeResponse:
    """
    Class to support ansible check mode.
    """

    def __init__(self, obj, status_code=200):
        self.obj = obj
        self.status_code = status_code

    def json(self):
        return self.obj


def ansible_return(module, rsp, changed, req=None, existing_obj=None):
    """
    :param module: AnsibleModule
    :param rsp: ApiResponse from zyxel_api
    :param changed: boolean
    :param req: ApiRequest to zyxel_api
    :param existing_obj: object to be passed debug output
    :param api_context: api login context
    helper function to return the right ansible based on the error code and changed
    Returns: specific ansible module exit function
    """

    obj_val = rsp.json() if rsp else existing_obj
    old_obj_val = existing_obj if changed and existing_obj else None

    zyxel_result = None
    if isinstance(rsp, ZyxelResponse):
        zyxel_result = f"{rsp.zyxel_zcfg_result} - {rsp.success()}"
        # if not rsp.success():
        if rsp.status_code > 299:
            return module.fail_json(
                msg="Error %d Msg %s req: %s" % (rsp.status_code, rsp.text, req),
                obj=obj_val,
                old_obj=old_obj_val,
                zyxel_result=zyxel_result,
            )

    return module.exit_json(
        changed=changed,
        request_data=req,
        obj=obj_val,
        old_obj=old_obj_val,
        zyxel_result=zyxel_result,
        result=rsp.zyxel_zcfg_result,
        response=rsp.response_data,
        response2=rsp.text,
    )


def get_connection(module):
    return Connection(module._socket_path)


def zyxel_ansible_api(
    module, api_oid, api_method, request_data=None, sensitive_fields=None
):

    connection = get_connection(module)
    logger.debug(
        "pre-send-request: connection=%s, api_oid=%s, api_method=%s",
        connection,
        api_oid,
        api_method,
    )
    try:
        response_data, response_code = connection.send_request(
            data=None, path=f"/cgi-bin/DAL?oid={api_oid}", method=api_method
        )
        logger.debug(
            "post-send-request: connection=%s, api_oid=%s, api_method=%s",
            connection,
            api_oid,
            api_method,
        )

        rsp = ZyxelResponse(response_code, response_data)

        return ansible_return(
            module=module,
            rsp=rsp,
            changed=False,
            req=request_data,
            existing_obj=None,
        )
    except ConnectionError as exc:
        return module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
