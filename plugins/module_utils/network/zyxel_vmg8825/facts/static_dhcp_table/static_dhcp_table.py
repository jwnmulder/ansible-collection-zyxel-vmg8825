# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825 static_dhcp_table fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""


# from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.static_dhcp_table.static_dhcp_table import (
    Static_dhcp_tableArgs,
)


class Static_dhcp_tableFacts(object):
    """The zyxel_vmg8825 static_dhcp_table facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Static_dhcp_tableArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Static_dhcp_table network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = connection.dal_get(oid="static_dhcp")

        objs = list(
            map(
                lambda s: {
                    "index": s.get("Index"),
                    "br_wan": s.get("BrWan"),
                    "enable": s.get("Enable"),
                    "mac_addr": s.get("MACAddr"),
                    "ip_addr": s.get("IPAddr"),
                },
                data,
            )
        )

        ansible_facts["ansible_network_resources"].pop("static_dhcp_table", None)

        facts = {}
        if objs:
            facts["static_dhcp_table"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for entry in params["config"]:
                facts["static_dhcp_table"].append(utils.remove_empties(entry))

        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
