# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Firewall parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class FirewallTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(FirewallTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
    ]
    # fmt: on


def oid():
    return "firewall"


def from_dal_object(dal_object):

    result = {}

    ip_version = dal_object.get("IPVersion")
    if ip_version is not None:

        # Workaround for invalid Zyxel ACL router entries
        ip_version = ip_version if ip_version >= 0 else 4

        ip_version = str(ip_version).replace("IPv", "")
        ip_version = f"IPv{ip_version}"
        result["ip_version"] = ip_version

    return result


def to_dal_object(ansible_object):

    result = {}

    ip_version = ansible_object.get("ip_version")
    if ip_version is not None:
        result["IPVersion"] = ip_version

    return result
