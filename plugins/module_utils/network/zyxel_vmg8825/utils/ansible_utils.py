# https://github.com/ansible-collections/community.network/blob/main/plugins/module_utils/network/avi/ansible_utils.py
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import logging
import traceback

from ansible.module_utils.basic import env_fallback
from ansible.module_utils.connection import Connection

ZYXEL_LIB_NAME = "zyxelclient_vmg8825"
ZYXEL_LIB_ERR = None
try:
    from zyxelclient_vmg8825.httpclient import ZyxelResponse
    from zyxelclient_vmg8825.factory import ZyxelClientFactory
except ImportError:
    ZYXEL_LIB_ERR = traceback.format_exc()

log = logging.getLogger(__name__)


class ZyxelCheckModeResponse:
    """
    Class to support ansible check mode.
    """

    def __init__(self, obj, status_code=200):
        self.obj = obj
        self.status_code = status_code

    def json(self):
        return self.obj


class ZyxelCredentials:
    url = ""
    username = ""
    password = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update_from_ansible_module(self, m):
        """
        :param m: ansible module
        :return:
        """
        if m.params.get("zyxel_credentials"):
            for k, v in m.params["zyxel_credentials"].items():
                if hasattr(self, k):
                    setattr(self, k, v)
        if m.params["url"]:
            self.url = m.params["url"]
        if m.params["username"]:
            self.username = m.params["username"]
        if m.params["password"]:
            self.password = m.params["password"]
        # if m.params.get('session_id'):
        #    self.session_id = m.params['session_id']
        # if m.params.get('csrftoken'):
        #    self.csrftoken = m.params['csrftoken']

    def __str__(self):
        return f"url {self.url} user {self.username}"


def ansible_return(module, rsp, changed, req=None, existing_obj=None, api_context=None):
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

    api_creds = ZyxelCredentials()
    api_creds.update_from_ansible_module(module)
    key = f"{api_creds.url}:{api_creds.username}"
    disable_fact = module.params.get("zyxel_disable_session_cache_as_fact")

    fact_context = None
    if not disable_fact:
        fact_context = module.params.get("api_context", {})
        if fact_context:
            fact_context.update({key: api_context})
        else:
            fact_context = {key: api_context}

    obj_val = rsp.json() if rsp else existing_obj
    # print(f"obj_val: {obj_val}")
    # if (obj_val and module.params.get("obj_username", None) and
    #        "username" in obj_val):
    #    obj_val["obj_username"] = obj_val["username"]
    # if (obj_val and module.params.get("obj_password", None) and
    #        "password" in obj_val):
    #    obj_val["obj_password"] = obj_val["password"]
    old_obj_val = existing_obj if changed and existing_obj else None
    api_context_val = api_context if disable_fact else None
    ansible_facts_val = dict(zyxel_api_context=fact_context) if not disable_fact else {}

    zyxel_result = None
    if isinstance(rsp, ZyxelResponse):
        zyxel_result = f"{rsp.zyxel_zcfg_result} - {rsp.success()}"
        # if not rsp.success():
        if rsp.status_code > 299:
            return module.fail_json(
                msg="Error %d Msg %s req: %s api_context:%s "
                % (rsp.status_code, rsp.text, req, api_context),
                obj=obj_val,
                old_obj=old_obj_val,
                ansible_facts=ansible_facts_val,
                api_context=api_context_val,
                zyxel_result=zyxel_result,
            )

    return module.exit_json(
        changed=changed,
        request_data=req,
        obj=obj_val,
        old_obj=old_obj_val,
        ansible_facts=ansible_facts_val,
        api_context=api_context_val,
        zyxel_result=zyxel_result,
    )


def get_api_context(module, api_creds):
    api_context = module.params.get("api_context")
    if api_context and module.params.get("zyxel_disable_session_cache_as_fact"):
        return api_context
    elif api_context and not module.params.get("zyxel_disable_session_cache_as_fact"):
        key = f"{api_creds.url}:{api_creds.username}"
        return api_context.get(key)
    else:
        return None


def zyxel_get_client(module, sensitive_fields=None):

    api_creds = ZyxelCredentials()
    api_creds.update_from_ansible_module(module)

    api = ZyxelClientFactory.get_client(
        api_creds.url, api_creds.username, api_creds.password
    )

    api_context = get_api_context(module, api_creds)
    if api_context:
        api.set_context(api_context)

    return api


def zyxel_ansible_api(
    module, api_oid, api_method, request_data=None, sensitive_fields=None
):

    if module._socket_path is None:

        # don't use ansible.netcommon.httpapi
        return zyxel_ansible_classic_api(
            module=module,
            api_oid=api_oid,
            api_method=api_method,
            request_data=None,
            sensitive_fields=None,
        )

    else:

        connection = Connection(module._socket_path)
        http_response, response_data = connection.sexnd_request(
            data=None, path=f"/cgi-bin/DAL?oid={api_oid}", method=api_method
        )

        # print(http_response)
        rsp = ZyxelResponse(http_response, response_data)

        # return ansible_return(module, response, False, None, existing_obj=None)

        return ansible_return(
            module=module, rsp=rsp, changed=False, req=request_data, existing_obj=None
        )


def zyxel_ansible_classic_api(
    module, api_oid, api_method, request_data=None, sensitive_fields=None
):
    """
    This converts the Ansible module into Zyxel object and invokes APIs
    :param module: Ansible module
    :param obj_type: string representing Avi object type
    :param sensitive_fields: sensitive fields to be excluded for comparison
        purposes.
    Returns:
        success: module.exit_json with obj=avi object
        faliure: module.fail_json
    """
    # api_oid = api_oid or module.params.get('api_oid', 'none')
    # api_method = api_method or module.params.get('api_method', 'get')

    api_creds = ZyxelCredentials()
    api_creds.update_from_ansible_module(module)

    if not api_creds.url:
        return module.fail_json(msg="Missing value for 'url' (classic)")
    if not api_creds.username:
        return module.fail_json(msg="Missing value for 'username' (classic)")
    if not api_creds.password:
        return module.fail_json(msg="Missing value for 'password' (classic)")

    api = zyxel_get_client(module, sensitive_fields)

    # state = module.params['state']
    check_mode = module.check_mode

    changed = True
    existing_obj = None  # api.get(None).json()

    if check_mode:
        rsp = ZyxelCheckModeResponse(obj=None)
    else:
        try:
            if api_method == "get":
                changed = False
                rsp = api.dal_get(oid=api_oid)
            elif api_method == "put":
                rsp = api.dal_put(oid=api_oid, data=request_data)
            elif api_method == "post":
                rsp = api.dal_post(oid=api_oid, data=request_data)
            elif api_method == "delete":
                rsp = api.dal_delete(oid=api_oid)
        except Exception as e:
            if len(e.args) > 1 and isinstance(e.args[1], ZyxelResponse):
                rsp = e.args[1]
            else:
                raise e

    return ansible_return(
        module=module,
        rsp=rsp,
        changed=changed,
        req=request_data,
        existing_obj=existing_obj,
        api_context=api.get_context(),
    )


def zyxel_common_argument_spec():
    """
    Returns common arguments for all Avi modules
    :return: dict
    """
    credentials_spec = dict(
        url=dict(type="str", fallback=(env_fallback, ["ZYXEL_URL"])),
        username=dict(type="str", fallback=(env_fallback, ["ZYXEL_USERNAME"])),
        password=dict(
            type="str", fallback=(env_fallback, ["ZYXEL_PASSWORD"]), no_log=True
        ),
    )

    return dict(
        url=dict(type="str", fallback=(env_fallback, ["ZYXEL_URL"])),
        username=dict(type="str", fallback=(env_fallback, ["ZYXEL_USERNAME"])),
        password=dict(
            type="str", fallback=(env_fallback, ["ZYXEL_PASSWORD"]), no_log=True
        ),
        zyxel_credentials=dict(default=None, type="dict", options=credentials_spec),
        api_context=dict(type="dict"),
        zyxel_disable_session_cache_as_fact=dict(default=False, type="bool"),
    )
