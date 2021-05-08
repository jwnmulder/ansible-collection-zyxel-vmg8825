#
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The facts class for zyxel
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)
from ..module_utils.network.zyxel_vmg8825.argspec.facts.facts import FactsArgs
from ..module_utils.network.zyxel_vmg8825.facts.static_dhcp.static_dhcp import Static_dhcpFacts

#from ansible_collections.jwnmulder.zyxel_vmg825.plugins.module_utils.network.zyxel_vmg8825.facts.vlans.vlans import VlansFacts

#from ansible_collections.jwnmulder.zyxel_vmg825.plugins.module_utils.network.zyxel_vmg8825.facts.interfaces.interfaces import VlansFacts

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.legacy.base import (
    Default,
    Hardware,
    Interfaces,
    Config,
)

FACT_LEGACY_SUBSETS = dict(
    default=Default, hardware=Hardware, interfaces=Interfaces, config=Config
)

FACT_RESOURCE_SUBSETS = dict(
#    interfaces=InterfacesFacts,
#    vlans=VlansFacts,
    static_dhcp=Static_dhcpFacts
)


class Facts(FactsBase):
    """ The fact class for zyxel
    """

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super().__init__(module)

    def get_facts(
        self, legacy_facts_type=None, resource_facts_type=None, data=None
    ):
        """ Collect the facts for zyxel
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
            self.get_network_legacy_facts(
                FACT_LEGACY_SUBSETS, legacy_facts_type
            )

        return self.ansible_facts, self._warnings
