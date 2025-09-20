from __future__ import absolute_import, division, print_function

__metaclass__ = type
"""
The facts class for zyxel_vmg8825
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.static_dhcp.static_dhcp import (
    Static_dhcpFacts,
)

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.nat_port_forwards.nat_port_forwards import (
    Nat_port_forwardsFacts,
)

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.firewall_acls.firewall_acls import (
    Firewall_aclsFacts,
)

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.firewall.firewall import (
    FirewallFacts,
)


FACT_LEGACY_SUBSETS = {}
FACT_RESOURCE_SUBSETS = dict(
    static_dhcp=Static_dhcpFacts,
    nat_port_forwards=Nat_port_forwardsFacts,
    firewall_acls=Firewall_aclsFacts,
    firewall=FirewallFacts,
)


class Facts(FactsBase):
    """The fact class for zyxel_vmg8825"""

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None, resource_facts_type=None, data=None):
        """Collect the facts for zyxel_vmg8825

        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(
                FACT_RESOURCE_SUBSETS, resource_facts_type, data
            )

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS, legacy_facts_type)

        return self.ansible_facts, self._warnings
