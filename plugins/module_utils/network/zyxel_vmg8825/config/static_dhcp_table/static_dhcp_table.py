#
# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

from ansible.module_utils.six import iteritems

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates.static_dhcp_table import (
    Static_dhcp_tableTemplate,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.utils import (
    equal_dicts,
)


__metaclass__ = type

"""
The zyxel_vmg8825_static_dhcp_table config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import logging

logger = logging.getLogger(__name__)

# from ansible.module_utils.six import iteritems

# from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
#     dict_merge,
# )
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.facts import (
    Facts,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates import (
    static_dhcp_table,
)


class Static_dhcp_table(ResourceModule):
    """
    The zyxel_vmg8825_static_dhcp_table config class
    """

    def __init__(self, module):
        super(Static_dhcp_table, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="static_dhcp_table",
            tmplt=Static_dhcp_tableTemplate(),
        )
        # self.parsers = ["mac_addr"]

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        logger.debug("execute_module")
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        logger.debug("generate_commands")

        # If mac_addr is empty, it means we got an empty string back from our device.
        # This does happen sometimes after an invalid entry was sent.
        wantd = {
            entry.get("mac_addr") or entry.get("index"): entry for entry in self.want
        }
        haved = {
            entry.get("mac_addr") or entry.get("index"): entry for entry in self.have
        }

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Static_dhcp_table network resource.
        """
        logger.debug("compare, want=%s, have=%s", want, have)

        # if both 'have' and 'want' are set, they have the same PK
        # if dict values differ, an update is needed
        if want and have and not equal_dicts(want, have, ["index"]):
            self.add_zyxel_dal_command("PUT", static_dhcp_table.to_dal_object(want))

        # if only 'have' is set, delete based on index
        if not want and have:
            self.add_zyxel_dal_command("DELETE", oid_index=have["index"])

        # if only 'want' is set, inset new
        if want and not have:
            self.add_zyxel_dal_command("POST", static_dhcp_table.to_dal_object(want))

    def add_zyxel_dal_command(self, method, data=None, oid_index=None):
        request = {
            "oid": static_dhcp_table.oid(),
            "method": method,
            "data": data,
        }

        if oid_index:
            request["oid_index"] = oid_index

        self.commands.append(request)
