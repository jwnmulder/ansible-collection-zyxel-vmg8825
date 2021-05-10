#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: avi_api_version
author: Vilian Atmadzhov (@vivobg) <vilian.atmadzhov@paddypowerbetfair.com>
short_description: Avi API Version Module
description:
    - This module can be used to obtain the version of the Avi REST API. U(https://avinetworks.com/)
requirements: [ avisdk ]
options: {}
extends_documentation_fragment:
- community.network.avi
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

ZYXEL_LIB_ERR = None
try:
    from ..module_utils.network.zyxel_vmg8825.utils.zyxel import (
        ZYXEL_LIB_ERR,
        zyxel_common_argument_spec,
        zyxel_get_client,
        ansible_return,
    )
except ImportError:
    ZYXEL_LIB_ERR = traceback.format_exc()


def main():

    argument_specs = dict()
    argument_specs.update(zyxel_common_argument_spec())

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=True)

    if ZYXEL_LIB_ERR:
        return module.fail_json(
            msg=missing_required_lib("zyxel"), exception=ZYXEL_LIB_ERR
        )

    check_mode = module.check_mode

    api = zyxel_get_client(module)

    # changed = api.sessionkey is None

    response = None
    if not api.sessionkey and not check_mode:
        response = api.perform_login()

    return ansible_return(
        module, response, False, None, existing_obj=None, api_context=api.get_context()
    )


if __name__ == "__main__":
    main()
