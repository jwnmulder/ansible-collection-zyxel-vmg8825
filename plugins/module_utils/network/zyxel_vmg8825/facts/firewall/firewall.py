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

import json

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.firewall.firewall import (
    FirewallArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates import (
    firewall,
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

        if not data:
            data = connection.dal_get(oid=firewall.oid())

        if isinstance(data, str):
            data = json.loads(data)

        obj = firewall.from_dal_object(dal_object=data[0])

        ansible_facts["ansible_network_resources"].pop("firewall", None)

        facts = {}
        if obj:
            facts["firewall"] = {}
            params = utils.validate_config(self.argument_spec, {"config": obj})
            config = params["config"]
            facts["firewall"] = config

        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
