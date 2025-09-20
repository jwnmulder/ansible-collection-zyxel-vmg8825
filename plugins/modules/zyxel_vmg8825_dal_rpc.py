# Copyright: (c) 2021, Jan-Willem Mulder (@jwnmulder)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_vmg8825_dal_rpc
author: Jan-Willem Mulder (@jwnmulder)
short_description: Zyxel Module for interacting with the Zyxel DAL API
description:
  - This module can be used to send dal cfg commands to the Zyxel router
version_added: "0.1.0"
options:
  oid:
    type: str
    description: oid
    required: True
  method:
    description: HTTP method
    required: false
    type: str
    default: GET
    choices:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE
  index:
    type: int
    description: index for deleting entries, required when method=delete
  data:
    type: dict
    description: data, required when method=post,put
"""

EXAMPLES = """

"""


RETURN = """
result:
    description: Result code
    returned: ZCFG_SUCCES, ZCFG_FAILURE
    type: str
response:
    description: Zyxel REST resource
    returned: success, changed
    type: dict
"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils.network.zyxel_vmg8825.utils.utils import (
    ansible_zyxel_dal_request,
)


def main():
    argument_specs = dict(
        oid=dict(type="str", required=True),
        method=dict(
            type="str",
            required=False,
            choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
            default="GET",
        ),
        index=dict(type="int", required=False),
        data=dict(type="dict", required=False),
    )

    required_if = [
        ["method", "POST", ["data"]],
        ["method", "PUT", ["data"]],
        ["method", "PATCH", ["data"]],
        ["method", "DELETE", ["index"]],
    ]

    module = AnsibleModule(
        argument_spec=argument_specs,
        required_if=required_if,
        supports_check_mode=False,
    )

    oid = module.params.get("oid")
    index = module.params.get("index")
    method = module.params.get("method")
    data = module.params.get("data")

    return ansible_zyxel_dal_request(
        module, oid=oid, method=method, data=data, oid_index=index
    )


if __name__ == "__main__":
    main()
