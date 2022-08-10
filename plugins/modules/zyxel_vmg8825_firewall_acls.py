#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for zyxel_vmg8825_firewall_acls
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: zyxel_vmg8825_firewall_acls
short_description: 'Manages firewall ACL entries of zyxel_vmg8825'
description: 'Manages firewall ACL entries of zyxel_vmg8825'
version_added: '0.3.0'
author: Jan-Willem Mulder (@jwnmulder)
notes:
  - Tested against Zyxel VMG8825-T50
options:
  config:
    description: The provided configuration
    type: list
    elements: dict
    suboptions:
      index:
        description:
          - Index of the entry
        type: int
        required: false
      name:
        description:
          - Name
        type: str
        required: true
      order:
        description:
          - Order
        type: int
        required: true
      protocol:
        description:
          - Protocol
        type: str
        choices:
          - ALL
          - TCP
          - UDP
          - TCPUDP
          - ICMP
          - ICMPv6
        required: true
      source_port:
        description:
          - SourcePort
        type: int
        default: -1
      source_port_range_max:
        description:
        - SourcePortRangeMax
        type: int
        default: -1
      dest_port:
        description:
          - DestPort
        type: int
        default: -1
      dest_port_range_max:
        description:
        - DestPortRangeMax
        type: int
        default: -1
      direction:
        description:
          - Direction
        type: str
        choices:
          - WAN_TO_LAN
          - LAN_TO_WAN
          - WAN_TO_ROUTER
          - LAN_TO_ROUTER
        required: true
      ip_version:
        description:
        - IPVersion
        type: int
        choices:
          - 4  # IPv4
          - 6  # IPv6
        required: true
      limit_rate:
        description:
          - LimitRate
        type: int
        default: 0
      limit_rate_unit:
        description:
          - LimitRateUnit
        type: str
        choices:
          - minute
          - second
        required: false
      source_ip:
        description:
          - SourceIP
        type: str
        required: true
      source_mask:
        description:
          - SourceMask
          - in case of 192.168.0.0/24 the mask would be '24'
        type: str
        required: true
      dest_ip:
        description:
          - DestIP
        type: str
        required: true
      dest_mask:
        description:
          - DestMask
          - in case of 192.168.0.0/24 the mask would be '24'
        type: str
        required: true
      icmp_type:
        description:
          - ICMPType
        type: int
        required: false
      icmp_type_code:
        description:
          - ICMPTypeCode
        type: int
        required: false
      target:
        description:
          - Target
        type: str
        choices:
          - Accept
          - Drop
          - Reject
        required: true
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
    - rendered
    - parsed
    default: merged
"""

EXAMPLES = """

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
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.firewall_acls.firewall_acls import (
    Firewall_aclsArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.config.firewall_acls.firewall_acls import (
    Firewall_acls,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Firewall_aclsArgs.argument_spec,
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

    result = Firewall_acls(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
