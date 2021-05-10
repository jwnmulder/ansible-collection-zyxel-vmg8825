#
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The zyxel static_dhcp fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ..module_utils.network.zyxel_vmg8825.argspec.static_dhcp.static_dhcp import (
    Static_dhcpArgs,
)


class Static_dhcpFacts:
    """The zyxel static_dhcp fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Static_dhcpArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for static_dhcp
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        if not data:
            # typically data is populated from the current device configuration
            # data = connection.get('show running-config | section ^interface')
            # using mock data instead
            data = connection.get_device_info()

        ansible_facts["ansible_network_resources"].pop("static_dhcp", None)
        facts = {}
        facts["static_dhcp"] = data

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
