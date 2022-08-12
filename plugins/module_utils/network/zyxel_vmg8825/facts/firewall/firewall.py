# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825 firewall fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates.firewall import (
    FirewallTemplate,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.firewall.firewall import (
    FirewallArgs,
)


class FirewallFacts(object):
    """The zyxel_vmg8825 firewall facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = FirewallArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Firewall network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get()

        # parse native config using the Firewall template
        firewall_parser = FirewallTemplate(lines=data.splitlines(), module=self._module)
        objs = list(firewall_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("firewall", None)

        params = utils.remove_empties(
            firewall_parser.validate_config(
                self.argument_spec, {"config": objs}, redact=True
            )
        )

        facts["firewall"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
