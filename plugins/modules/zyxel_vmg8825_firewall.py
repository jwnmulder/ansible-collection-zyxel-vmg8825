#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for zyxel_vmg8825_firewall
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: zyxel_vmg8825_firewall
short_description: "Manages firewall config of zyxel_vmg8825"
description: "Manages firewall config of zyxel_vmg8825"
version_added: "0.3.0"
author: Jan-Willem Mulder (@jwnmulder)
notes:
  - Tested against Zyxel VMG8825-T50
options:
  config:
    description: The provided configuration
    type: dict
    suboptions:
      ipv4_enabled:
        description:
          - IPv4 Firewall
          - Zyxel parameter - IPv4_Enable
        type: bool
      ipv6_enabled:
        description:
          - IPv6 Firewall
          - Zyxel parameter - IPv6_Enable
        type: bool
      dos_enabled:
        description:
          - Dos Protection Blocking
          - Zyxel parameter - enableDos
        type: bool
      level:
        description:
          - Zyxel Firewall level
          - |
            I(level=Off):
            LAN to WAN - allow access to all internet services,
            WAN to LAN - allow access from other computers on the internet
          - |
            I(level=Low):
            LAN to WAN - allow access to all internet services,
            WAN to LAN - block access from other computers on the internet
          - |
            I(level=High):
            LAN to WAN - block access to all internet services,
            WAN to LAN - block access from other computers on the internet.
            When the security level is set to "High", access to the following services is allowed: Telnet,FTP,HTTP,HTTPS,DNS,IMAP,POP3,SMTP and IPv6 Ping
          - Zyxel parameter - Level_GUI
        type: str
        choices:
          - "Off"
          - "Low"
          - "High"
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
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using replaced

# Before state:
# -------------
#
# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "Low"
# }

- name: Configure firewall
  zyxel_vmg8825_firewall:
    config:
      ipv4_enabled: true
      ipv6_enabled: true
      dos_enabled: true
      level: High
    state: replaced

# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "High"
# }

# Using merged

# Before state:
# -------------
#
# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "Low"
# }

- name: Configure firewall
  zyxel_vmg8825_firewall:
    config:
      ipv4_enabled: true
      ipv6_enabled: true
      dos_enabled: true
      level: High
    state: merged

# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "High"
# }

# Using overridden

# Before state:
# -------------
#
# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "Low"
# }

- name: Configure firewall
  zyxel_vmg8825_firewall:
    config:
      ipv4_enabled: true
      ipv6_enabled: true
      dos_enabled: true
      level: High
    state: overridden

# DAL?oid=firewall
# {
#    "IPv4_Enable": true,
#    "IPv6_Enable": true,
#    "enableDos": true,
#    "Level_GUI": "High"
# }
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
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.firewall.firewall import (
    FirewallArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.config.firewall.firewall import (
    Firewall,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=FirewallArgs.argument_spec,
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

    result = Firewall(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
