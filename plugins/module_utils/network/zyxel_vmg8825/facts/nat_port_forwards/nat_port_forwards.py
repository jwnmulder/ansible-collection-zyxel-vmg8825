from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825 nat_port_forwards fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import json

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.nat_port_forwards.nat_port_forwards import (
    Nat_port_forwardsArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates import (
    nat_port_forwards,
)


class Nat_port_forwardsFacts:
    """The zyxel_vmg8825 nat_port_forwards facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Nat_port_forwardsArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for static_dhcp network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = connection.dal_get(oid=nat_port_forwards.oid())

        if isinstance(data, str):
            data = json.loads(data)

        objs = list(map(nat_port_forwards.from_dal_object, data))

        ansible_facts["ansible_network_resources"].pop("nat_port_forwards", None)

        facts = {}
        if objs:
            facts["nat_port_forwards"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for entry in params["config"]:
                facts["nat_port_forwards"].append(utils.remove_empties(entry))

        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
