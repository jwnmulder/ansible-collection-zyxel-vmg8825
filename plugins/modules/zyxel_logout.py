#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_logout
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


from ansible.module_utils.basic import AnsibleModule, missing_required_lib

from ..module_utils.network.zyxel_vmg8825.utils.ansible_utils import (
    ZYXEL_LIB_NAME,
    ZYXEL_LIB_ERR,
    zyxel_common_argument_spec,
    zyxel_get_client,
    ansible_return,
)


def main():

    argument_specs = dict()
    argument_specs.update(zyxel_common_argument_spec())

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=True)

    if ZYXEL_LIB_ERR:
        return module.fail_json(
            msg=missing_required_lib(ZYXEL_LIB_NAME), exception=ZYXEL_LIB_ERR
        )

    # check_mode = module.check_mode

    api = zyxel_get_client(module)

    changed = False  # api.sessionkey is not None

    response = None
    # if api.sessionkey and not check_mode:
    response = api.perform_logout().json()

    return ansible_return(
        module,
        None,
        changed,
        None,
        existing_obj=response,
        api_context=api.get_context(),
    )


if __name__ == "__main__":
    main()
