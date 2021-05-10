#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_ping
author: Jan-Willem Mulder (@jwnmulder)
short_description: Zyxel Module
description:
  - Zyxel module
requirements:
  - zyxelclient_vmg8825
options:
  url:
    type: str
    description: url
  username:
    type: str
    description: username
  password:
    type: str
    description: password
  zyxel_credentials:
    type: dict
    description: zyxel credentials
    suboptions:
      url:
        type: str
        description: url
      username:
        type: str
        description: username
      password:
        type: str
        description: password
  api_context:
    type: dict
    description: api context
  zyxel_disable_session_cache_as_fact:
    type: bool
    description: zyxel_disable_session_cache_as_fact
    default: False
"""

EXAMPLES = """
  - name: Get AVI API version
    community.network.avi_api_version:
      controller: ""
      username: ""
      password: ""
      tenant: ""
    register: avi_controller_version
"""


RETURN = """
obj:
    description: Avi REST resource
    returned: success, changed
    type: dict
"""

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

# from ansible.module_utils.connection import Connection

ZYXEL_LIB_ERR = None
try:
    from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.zyxel import (
        ZYXEL_LIB_ERR,
        zyxel_ansible_api,
        zyxel_common_argument_spec,
        #        ansible_return,
    )
except ImportError:
    ZYXEL_LIB_ERR = traceback.format_exc()

# try:
#     from zyxel_api_vmg8825.client import ZyxelResponse

#     # from ansible.module_utils.zyxel_api.client_factory import ClientFactory
# except ImportError:
#     ZYXEL_LIB_ERR = traceback.format_exc()


def main():

    argument_specs = dict()
    argument_specs.update(zyxel_common_argument_spec())

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=False)

    if ZYXEL_LIB_ERR:
        return module.fail_json(
            msg=missing_required_lib("zyxel"), exception=ZYXEL_LIB_ERR
        )

    return zyxel_ansible_api(module, "PINGTEST", "get")

    # # module is your AnsibleModule instance.
    # connection = Connection(module._socket_path)
    # print([connection])
    # http_response, response_data = connection.send_request(
    #     data=None, path="/cgi-bin/DAL?oid=PINGTEST"
    # )

    # print(http_response)
    # response = ZyxelResponse(http_response, response_data)

    # return ansible_return(module, response, False, None, existing_obj=None)


if __name__ == "__main__":
    main()
