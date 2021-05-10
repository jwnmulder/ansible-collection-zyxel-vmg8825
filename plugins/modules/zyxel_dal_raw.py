#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_dal_raw
author: Jan-Willem Mulder (@jwnmulder) (@jwnmulder)
short_description: Zyxel Module
description:
    - This module can be used to send dal commands to the Zyxel router
requirements: [ zyxelclient_vmg8825 ]
options: {}
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
    description: Zyxel REST resource
    returned: success, changed
    type: dict
"""

import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

ZYXEL_LIB_ERR = None
try:
    from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.zyxel import (
        ZYXEL_LIB_ERR,
        zyxel_ansible_api,
        zyxel_common_argument_spec,
    )
except ImportError:
    ZYXEL_LIB_ERR = traceback.format_exc()


def main():

    argument_specs = dict(
        api_oid=dict(type="str", required=True),
        api_method=dict(type="str", required=True),
        data=dict(type="dict", required=False),
    )
    argument_specs.update(zyxel_common_argument_spec())

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=False)

    if ZYXEL_LIB_ERR:
        return module.fail_json(
            msg=missing_required_lib("zyxel"), exception=ZYXEL_LIB_ERR
        )

    api_oid = module.params.get("api_oid")
    api_method = module.params.get("api_method")
    data = module.params.get("data")

    return zyxel_ansible_api(module, api_oid, api_method, request_data=data)


if __name__ == "__main__":
    main()
