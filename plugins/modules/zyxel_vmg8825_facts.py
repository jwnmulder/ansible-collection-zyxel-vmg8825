#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The module file for zyxel_vmg8825_facts
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: zyxel_vmg8825_facts
author: Jan-Willem Mulder (@jwnmulder)
short_description: Get facts about zyxel_vmg8825 devices.
description:
  - Collects facts from network devices running the zyxel_vmg8825 operating
    system. This module places the facts gathered in the fact tree keyed by the
    respective resource name.  The facts module will always collect a
    base set of facts from the device and can enable or disable
    collection of additional facts.
version_added: "0.1.0"
options:
  gather_subset:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset. Possible values for this argument include
        all, min, hardware, config, legacy, and interfaces. Can specify a
        list of values to include a larger subset. Values can also be used
        with an initial C(!) to specify that a specific subset should
        not be collected.
    required: false
    type: list
    elements: str
    default: 'min'
  gather_network_resources:
    description:
      - When supplied, this argument will restrict the facts collected
        to a given subset. Possible values for this argument include
        all and the resources like interfaces, vlans etc.
        Can specify a list of values to include a larger subset. Values
        can also be used with an initial C(!) to specify that a
        specific subset should not be collected.
    required: false
    type: list
    elements: str
    choices:
      - all
      - firewall
      - firewall_acls
      - nat_port_forwards
      - static_dhcp
"""

EXAMPLES = """
# Gather all facts
- zyxel_vmg8825_facts:
    gather_subset: all
    gather_network_resources: all

# Collect only the static_dhcp facts
- zyxel_vmg8825_facts:
    gather_subset:
      - "!all"
      - "!min"
    gather_network_resources:
      - static_dhcp
      - nat_port_forwards

# Do not collect static_dhcp facts
- zyxel_vmg8825_facts:
    gather_network_resources:
      - "!static_dhcp"

# Collect static_dhcp and minimal default facts
- zyxel_vmg8825_facts:
    gather_subset: min
    gather_network_resources: static_dhcp
"""

RETURN = """
# See the respective resource module parameters for the tree.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.facts.facts import (
    FactsArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.facts import (
    Facts,
)


def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """
    module = AnsibleModule(
        argument_spec=FactsArgs.argument_spec, supports_check_mode=True
    )
    warnings = [
        # "default value for `gather_subset` "
        # "will be changed to `min` from `!config` v2.11 onwards"
    ]

    result = Facts(module).get_facts()

    ansible_facts, additional_warnings = result
    warnings.extend(additional_warnings)

    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == "__main__":
    main()
