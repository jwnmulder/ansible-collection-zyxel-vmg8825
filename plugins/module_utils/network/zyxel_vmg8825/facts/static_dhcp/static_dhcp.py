# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
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


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates.static_dhcp import (
    Static_dhcpTemplate,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.static_dhcp.static_dhcp import (
    Static_dhcpArgs,
)


class Static_dhcpFacts(object):
    """The zyxel_vmg8825 static_dhcp facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Static_dhcpArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Static_dhcp network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            # data = connection.get()
            data = connection.get_device_info()

        # parse native config using the Static_dhcp template
        static_dhcp_parser = Static_dhcpTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = list(static_dhcp_parser.parse().values())

        # objs = list()
        # for conf in data:
        #     if conf:
        #         obj = self.render_config(self.generated_spec, conf)
        #         if obj:
        #             objs.append(obj)

        ansible_facts["ansible_network_resources"].pop("static_dhcp", None)

        params = utils.remove_empties(
            static_dhcp_parser.validate_config(
                self.argument_spec, {"config": objs}, redact=True
            )
        )

        facts["static_dhcp"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
