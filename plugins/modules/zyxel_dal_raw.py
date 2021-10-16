#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_dal_raw
author: Jan-Willem Mulder (@jwnmulder)
short_description: Zyxel Module
description:
  - This module can be used to send dal commands to the Zyxel router
options:
  api_oid:
    type: str
    description: api_oid
    required: True
  api_method:
    type: str
    description: api_method
    required: True
  data:
    type: dict
    description: data
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


from ansible.module_utils.basic import AnsibleModule

from ..module_utils.network.zyxel_vmg8825.utils.ansible_utils import (
    zyxel_ansible_api,
)


def main():

    argument_specs = dict(
        api_oid=dict(type="str", required=True),
        api_method=dict(type="str", required=True),
        data=dict(type="dict", required=False),
    )

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=False)

    api_oid = module.params.get("api_oid")
    api_method = module.params.get("api_method")
    data = module.params.get("data")

    return zyxel_ansible_api(module, api_oid, api_method, request_data=data)


if __name__ == "__main__":
    main()
