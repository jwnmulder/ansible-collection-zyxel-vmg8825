# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825 static_dhcp fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import json

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.static_dhcp.static_dhcp import (
    Static_dhcpArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates import (
    static_dhcp,
)


class Static_dhcpFacts(object):
    """The zyxel_vmg8825 static_dhcp facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Static_dhcpArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for static_dhcp network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = connection.dal_get(oid=static_dhcp.oid())

        if isinstance(data, str):
            data = json.loads(data)

        objs = list(map(static_dhcp.from_dal_object, data))

        ansible_facts["ansible_network_resources"].pop("static_dhcp", None)

        facts = {}
        if objs:
            facts["static_dhcp"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for entry in params["config"]:
                facts["static_dhcp"].append(utils.remove_empties(entry))

        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
