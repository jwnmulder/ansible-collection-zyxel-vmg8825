#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for zyxel_vmg8825_static_dhcp
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: zyxel_vmg8825_static_dhcp
author: Jan-Willem Mulder (@jwnmulder)
version_added: '1.0.0'
short_description: 'This module configures and manages static_dhcp entries on Zyxel VMG8825 routers'
description: 'This module configures and manages static_dhcp entries on Zyxel VMG8825 routers'
notes:
  - 'Tested against <network_os> <version>'
options:
  config:
    description: The provided configuration
    type: list
    elements: dict
    suboptions:
      index:
        description:
        - Index
        type: int
      br_wan:
        description:
        - BrWan
        type: str
        default: Default
      enable:
        description:
        - Enable
        type: bool
      mac_addr:
        description:
        - MACAddr
        type: str
      ip_addr:
        description:
        - IPAddr
        type: str
  state:
    description:
    - The state the configuration should be left in
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - rendered
    - parsed
    default: merged
"""

EXAMPLES = """

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when state is I(merged), I(replaced), I(overridden), I(deleted) or I(purged)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when state is I(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when state is I(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when state is I(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.static_dhcp.static_dhcp import (
    Static_dhcpArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.config.static_dhcp.static_dhcp import (
    Static_dhcp,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Static_dhcpArgs.argument_spec,
        # mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            # ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Static_dhcp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
