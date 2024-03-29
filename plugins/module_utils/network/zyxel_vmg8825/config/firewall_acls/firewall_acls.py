#
# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The zyxel_vmg8825_firewall_acls config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import logging

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.facts.facts import (
    Facts,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.rm_templates.firewall_acls import (
    Firewall_aclsTemplate,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.utils import (
    equal_dicts,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825 import (
    rm_templates,
)

logger = logging.getLogger(__name__)


class Firewall_acls(ResourceModule):
    """
    The zyxel_vmg8825_firewall_acls config class
    """

    def __init__(self, module):
        super(Firewall_acls, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="firewall_acls",
            tmplt=Firewall_aclsTemplate(),
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
        # If name is empty, it means we got an empty string back from our device.
        # This does happen sometimes after an invalid entry was sent.
        wantd = {entry.get("name") or entry.get("index"): entry for entry in self.want}
        haved = {entry.get("name") or entry.get("index"): entry for entry in self.have}

        # populate 'index' and 'order' based on haved if not set in wantd
        for key, value in wantd.items():
            have = haved.get(key)

            have_index = have.get("index") if have else None
            if have_index and not value.get("index"):
                value["index"] = have_index

            have_order = have.get("order") if have else None
            if have_order and not value.get("order"):
                value["order"] = have_order

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
        for the Firewall_acls network resource.
        """
        # logger.debug("compare, want=%s, have=%s", want, have)

        # if both 'have' and 'want' are set, they have the same PK
        # if dict values differ, an update is needed
        if want and have and not equal_dicts(want, have, ["index", "order"]):
            self.add_zyxel_dal_command(
                "PUT", rm_templates.firewall_acls.to_dal_object(want)
            )

        # if only 'have' is set, delete based on index
        if not want and have:
            self.add_zyxel_dal_command("DELETE", oid_index=have["index"])

        # if only 'want' is set, inset new
        if want and not have:
            self.add_zyxel_dal_command(
                "POST", rm_templates.firewall_acls.to_dal_object(want)
            )

    def add_zyxel_dal_command(self, method, data=None, oid_index=None):

        if self.state == "rendered":
            self.commands.append(data)

        else:

            request = {
                "oid": rm_templates.firewall_acls.oid(),
                "method": method,
            }

            if data:
                request["data"] = data

            if oid_index:
                request["oid_index"] = oid_index

            if self.commands and method == "DELETE":
                # deletes must happen first and in reverse orde
                # higest indexes are to be deleted first as indexes
                # keep changing while adding or deleting entries on a Zyxel device
                closests_higher = None
                for x in self.commands:
                    if x["method"] == "DELETE":
                        index = x["oid_index"]
                        if index > oid_index:
                            closests_higher = x

                index = 0
                if closests_higher:
                    index = self.commands.index(closests_higher) + 1
                self.commands.insert(index, request)
            else:
                self.commands.append(request)
