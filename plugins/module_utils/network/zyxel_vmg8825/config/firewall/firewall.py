from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825_firewall config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import logging

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.facts import (
    Facts,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates.firewall import (
    FirewallTemplate,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.utils import (
    equal_dicts,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825 import (
    rm_templates,
)

logger = logging.getLogger(__name__)


class Firewall(ResourceModule):
    """
    The zyxel_vmg8825_firewall config class
    """

    def __init__(self, module):
        super(Firewall, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="firewall",
            tmplt=FirewallTemplate(),
        )
        self.parsers = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()

        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """

        # Only full configuration updates are supported by the Zyxel router
        # to support only updating one setting at a time, we merge the existing
        # on router config first
        wanted = dict_merge(self.have, self.want)

        if self.state == "rendered":
            data = rm_templates.firewall.to_dal_object(wanted)
            self.commands.append(data)
        else:
            self._compare(want=wanted, have=self.have)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Firewall network resource.
        """
        # logger.debug("compare, want=%s, have=%s", want, have)

        # if both 'have' and 'want' are set, they have the same PK
        # if dict values differ, an update is needed
        if want and have and not equal_dicts(want, have, []):
            self.add_zyxel_dal_command("PUT", rm_templates.firewall.to_dal_object(want))

    def add_zyxel_dal_command(self, method, data):
        request = {
            "oid": rm_templates.firewall.oid(),
            "method": method,
            "data": data,
        }

        self.commands.append(request)
