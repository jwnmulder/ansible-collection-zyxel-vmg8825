from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825 firewall_acls fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import json

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.argspec.firewall_acls.firewall_acls import (
    Firewall_aclsArgs,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates import (
    firewall_acls,
)


class Firewall_aclsFacts:
    """The zyxel_vmg8825 firewall_acls facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Firewall_aclsArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Firewall_acls network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = connection.dal_get(oid=firewall_acls.oid())

        if isinstance(data, str):
            data = json.loads(data)

        objs = list(map(firewall_acls.from_dal_object, data))

        ansible_facts["ansible_network_resources"].pop("firewall_acls", None)

        facts = {}
        if objs:
            facts["firewall_acls"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for entry in params["config"]:
                facts["firewall_acls"].append(utils.remove_empties(entry))

        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
