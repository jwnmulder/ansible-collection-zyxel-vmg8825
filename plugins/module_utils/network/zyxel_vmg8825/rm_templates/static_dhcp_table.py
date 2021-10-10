# -*- coding: utf-8 -*-
# Copyright 2021
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Static_dhcp_table parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Static_dhcp_tableTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Static_dhcp_tableTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        # {
        #     "name": "key_a",
        #     "getval": re.compile(
        #         r"""
        #         ^key_a\s(?P<key_a>\S+)
        #         $""", re.VERBOSE),
        #     "setval": "",
        #     "result": {
        #     },
        #     "shared": True
        # },
        # {
        #     "name": "static_dhcp",
        #     "getval": re.compile(
        #         r"""
        #         (\s+vrf\s(?P<vrf>\b(?!all\b)\S+))?
        #         (?P<address_family>\s+address-family\s(?P<afi>\S+)\s(?P<safi>\S+))
        #         $""", re.VERBOSE
        #     ),
        #     "setval": "address-family {{ afi}} {{safi}}",
        #     "result": {
        #         "address_family": {
        #             '{{"address_family_" + afi + "_" + safi + "_vrf_" + vrf|d() }}': {
        #                 "afi": "{{ afi}}",
        #                 "safi": "{{safi}}",
        #                 "vrf": "{{ vrf }}"
        #             }
        #         }
        #     },
        #     "shared": True,
        # },
        {
            "name": "mac_addr",
            # "getval": re.compile(
            #     r"""
            #     \s*neighbor
            #     \s+(?P<peer>\S+)
            #     \s+route-map
            #     \s+(?P<name>\S+)
            #     \s+(?P<dir>in|out)
            #     *$""",
            #     re.VERBOSE,
            # ),
            # "setval": _tmplt_bgp_neighbor,
            "compval": "mac_addr",
            # "result": {
            #     "address_family": {
            #         '{{ afi + "_" + vrf|d() }}': {
            #             "neighbor": {
            #                 "{{ peer }}": {
            #                     "peer": "{{ peer }}",
            #                     "route_map": {
            #                         "name": "{{ name }}",
            #                         "direction": "{{ dir }}"
            #                     }
            #                 }
            #             }
            #         }
            #     }
            # },
        },
    ]
    # fmt: on


def oid():
    return "static_dhcp"


def from_dal_object(dal_object):
    return {
        "index": dal_object.get("Index"),
        "br_wan": dal_object.get("BrWan"),
        "enable": dal_object.get("Enable"),
        "mac_addr": dal_object.get("MACAddr"),
        "ip_addr": dal_object.get("IPAddr"),
    }


def to_dal_object(ansible_object):
    return {
        "Index": ansible_object.get("index"),
        "BrWan": ansible_object.get("br_wan"),
        "Enable": ansible_object.get("enable"),
        "MACAddr": ansible_object.get("mac_addr"),
        "IPAddr": ansible_object.get("ip_addr"),
    }
