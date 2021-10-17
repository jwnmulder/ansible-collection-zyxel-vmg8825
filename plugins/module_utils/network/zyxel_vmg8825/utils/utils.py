from __future__ import absolute_import, division, print_function

__metaclass__ = type


# utils
from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection
from ansible.module_utils.connection import ConnectionError


def get_connection(module):
    return Connection(module._socket_path)


def ansible_zyxel_dal_request(module, oid, method, data=None, oid_index=None):

    connection = get_connection(module)
    try:
        response_data, response_code = connection.send_dal_request(
            data=data, oid=oid, oid_index=oid_index, method=method
        )

        obj = response_data.get("Object")
        reply_msg = response_data.get("ReplyMsg")
        reply_msg_multi_lang = response_data.get("ReplyMsgMultiLang")

        result = {}
        result["changed"] = method in ["POST", "PUT"]
        result["result"] = response_data.get("result")
        result["obj"] = obj
        if data:
            result["request_data"] = data
        if reply_msg:
            result["reply_msg"] = reply_msg
        if reply_msg_multi_lang:
            result["reply_msg_multi_lang"] = reply_msg_multi_lang

        if response_code > 299:
            result["msg"] = "Error %d Msg %s req: %s" % (
                response_code,
                response_data,
                data,
            )
            return module.fail_json(result)

        return module.exit_json(**result)

    except ConnectionError as exc:
        return module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))


def equal_dicts(d1, d2, ignore_keys):
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered
