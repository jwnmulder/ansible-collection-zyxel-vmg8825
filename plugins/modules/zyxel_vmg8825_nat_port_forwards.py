#!/usr/bin/python
"""
The module file for zyxel_vmg8825_nat_port_forwards
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: zyxel_vmg8825_nat_port_forwards
short_description: 'Manages nat port forward entries of zyxel_vmg8825'
description: 'Manages nat port forward entries of zyxel_vmg8825'
version_added: '0.2.0'
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
      enable:
        description:
        - True is the entry should be active
        type: bool
        default: True
      protocol:
        description:
        - Protocol
        type: str
        choices:
          - TCP
          - UDP
          - ALL  # TCP/UDP
        default: TCP
      description:
        description:
        - Service Name
        type: str
        required: true
      interface:
        description:
        - Wan Interface.
        - Dynamic reference to one of VD_Internet/ETH_Ethernet/ADSL_Internet
        - IP.Interface.7
        type: str
        required: true
      external_port_start:
        description:
        - Start Port
        - This is also used as the primary key for updating entries in the device.
          Changing this value will result in deleting the old entry and adding a new one
        type: int
        required: true
      external_port_end:
        description:
        - End Port. If only one port is to be opened, set this to the same value as Start Port
        type: int
        required: true
      internal_port_start:
        description:
        - Translation Start Port
        type: int
        required: true
      internal_port_end:
        description:
        - Translation End Port
        type: int
        required: true
      internal_client:
        description:
        - Server IP Address. IP address to which traffic should be forwarded
        type: str
        required: true
      originating_ip_address:
        description:
        - Originating IP Address
        type: str
        required: false
      # X_ZYXEL_AutoDetectWanStatus": false
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
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.nat_port_forwards.nat_port_forwards import (
    Nat_port_forwardsArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.config.nat_port_forwards.nat_port_forwards import (
    Nat_port_forwards,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Nat_port_forwardsArgs.argument_spec,
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

    result = Nat_port_forwards(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
