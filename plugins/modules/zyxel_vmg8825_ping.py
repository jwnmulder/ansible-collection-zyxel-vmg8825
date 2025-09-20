from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_vmg8825_ping
author: Jan-Willem Mulder (@jwnmulder)
short_description: Zyxel Module for sending PINGTEST
description:
  - Send a PINGTEST dal command
"""

EXAMPLES = """

"""


RETURN = """

"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils.network.zyxel_vmg8825.utils.utils import (
    ansible_zyxel_dal_request,
)


def main():

    argument_specs = {}

    module = AnsibleModule(argument_spec=argument_specs, supports_check_mode=False)

    return ansible_zyxel_dal_request(module, oid="PINGTEST", method="GET")


if __name__ == "__main__":
    main()
