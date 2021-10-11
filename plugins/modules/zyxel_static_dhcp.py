#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_static_dhcp
author: Jan-Willem Mulder (@jwnmulder)
short_description: Zyxel Module
description: Zyxel module
# requirements: [ zyxelclient_vmg8825 ]
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


from ansible.module_utils.basic import AnsibleModule

from ..module_utils.network.zyxel_vmg8825.utils.ansible_utils import (
    zyxel_ansible_api,
)


def main():

    argument_specs = dict()
    # argument_specs.update(zyxel_common_argument_spec())

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=False)

    return zyxel_ansible_api(module, "static_dhcp", "get")


if __name__ == "__main__":
    main()
