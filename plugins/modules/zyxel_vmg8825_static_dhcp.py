#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for zyxel_vmg8825_static_dhcp
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: zyxel_vmg8825_static_dhcp
short_description: 'Manages static_dhcp entries of zyxel_vmg8825'
description: 'Manages static_dhcp entries of zyxel_vmg8825'
version_added: '1.0.0'
author: Jan-Willem Mulder (@jwnmulder)
notes:
  - Tested against Zyxel VMG8825-T50
  - Configuration is merged using the 'mac_addr' value and not the 'index' value
options:
  config:
    description: The provided configuration
    type: list
    elements: dict
    suboptions:
      index:
        description:
        - Index of the entry. Note that this field has no use in updating configuration.
          Entries are updated based on their mac_addr
        type: int
      br_wan:
        description:
        - BrWan
        type: str
        default: Default
      enable:
        description:
        - True is the entry should be active
        type: bool
      mac_addr:
        description:
        - MAC address. This is also used as the primary key for updating entries in the device.
          Changing a MAC address will result in deleting the old entry and adding a new one
        type: str
      ip_addr:
        description:
        - IP address
        type: str
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
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
    default: merged
"""

EXAMPLES = """
# Using replaced

# Before state:
# -------------
#
# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.1"
#   },
# ]

- name: Configure static_dhcp
  zyxel_vmg8825_static_dhcp:
    config:
      - br_wan: Default
        enable: True
        mac_addr: "01:01:01:01:01:01"
        ip_addr: "192.168.0.2"
    state: replaced

# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.2"
#   },
# ]

# Using deleted

# Before state:
# -------------
#
# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.1"
#   },
# ]

- name: Configure static_dhcp
  zyxel_vmg8825_static_dhcp:
    state: deleted

# DAL?oid=static_dhcp
# [
# ]

# Using merged

# Before state:
# -------------
#
# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.1"
#   },
# ]

- name: Configure static_dhcp
  zyxel_vmg8825_static_dhcp:
    config:
      - br_wan: Default
        enable: True
        mac_addr: "01:01:01:01:01:02"
        ip_addr: "192.168.0.2"
    state: merged

# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.1"
#   },
#   {
#     "Index": 2,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:02",
#     "IPAddr": "192.168.0.2"
#   },
# ]

# Using overridden

# Before state:
# -------------
#
# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:01",
#     "IPAddr": "192.168.0.1"
#   },
# ]

- name: Configure static_dhcp
  zyxel_vmg8825_static_dhcp:
    config:
      - br_wan: Default
        enable: True
        mac_addr: "01:01:01:01:01:02"
        ip_addr: "192.168.0.2"
    state: replaced

# DAL?oid=static_dhcp
# [
#   {
#     "Index": 1,
#     "BrWan": "Default",
#     "Enable": true,
#     "MACAddr": "01:01:01:01:01:02",
#     "IPAddr": "192.168.0.2"
#   },
# ]
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
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
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
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
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Static_dhcp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
