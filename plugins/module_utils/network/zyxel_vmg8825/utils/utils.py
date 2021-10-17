from __future__ import absolute_import, division, print_function

__metaclass__ = type


# utils
from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection
from ansible.module_utils.connection import ConnectionError


def _ansible_return(
    module, response_code, response_data, changed, req=None, existing_obj=None
):
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

    obj_val = response_data or existing_obj
    old_obj_val = existing_obj if changed and existing_obj else None

    obj = obj_val.get("Object")
    reply_msg = obj_val.get("ReplyMsg")
    reply_msg_multi_lang = obj_val.get("ReplyMsgMultiLang")
    # zyxel_result = None

    result = {}
    result["changed"] = False
    result["result"] = response_data.get("result")
    result["obj"] = obj
    if req:
        result["request_data"] = req
    if old_obj_val:
        result["old_obj"] = old_obj_val
    if reply_msg:
        result["reply_msg"] = reply_msg
    if reply_msg_multi_lang:
        result["reply_msg_multi_lang"] = reply_msg_multi_lang

    if response_code > 299:
        result["msg"] = "Error %d Msg %s req: %s" % (response_code, response_data, req)
        return module.fail_json(result)

    return module.exit_json(**result)


def get_connection(module):
    return Connection(module._socket_path)


def zyxel_ansible_api(
    module, api_oid, api_method, request_data=None, api_oid_index=None
):

    connection = get_connection(module)
    try:
        response_data, response_code = connection.send_dal_request(
            data=None, oid=api_oid, method=api_method
        )

        return _ansible_return(
            module=module,
            response_code=response_code,
            response_data=response_data,
            changed=False,
            req=request_data,
            existing_obj=None,
        )
    except ConnectionError as exc:
        return module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))


def equal_dicts(d1, d2, ignore_keys):
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered
