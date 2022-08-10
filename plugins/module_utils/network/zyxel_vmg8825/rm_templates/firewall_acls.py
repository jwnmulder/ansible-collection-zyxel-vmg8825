# -*- coding: utf-8 -*-
# Copyright 2022
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Firewall_acls parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Firewall_aclsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Firewall_aclsTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
    ]
    # fmt: on


def oid():
    return "firewall_acl"


def field_map():

    return {
        "index": "Index",
        "name": "Name",
        "order": "Order",
        "protocol": "Protocol",
        #   "source_port": "SourcePort",
        #   "source_port_range_max": "SourcePortRangeMax",
        #   "dest_port": "DestPort",
        #   "dest_port_range_max": "DestPortRangeMax",
        "direction": "Direction",
        "ip_version": "IPVersion",
        #   "limit_rate": "LimitRate",
        #   "limit_rate_unit": "LimitRateUnit",
        "source_ip": "SourceIP",
        "source_mask": "SourceMask",
        "dest_ip": "DestIP",
        "dest_mask": "DestMask",
        #   "icmp_type": "ICMPType",
        #   "icmp_type_code": "ICMPTypeCode",
        "target": "Target",
    }


def from_dal_object(dal_object):
    result = {}
    for key, value in field_map().items():
        result[key] = dal_object.get(value)
    return result


def to_dal_object(ansible_object):
    result = {}
    for key, value in field_map().items():
        result[value] = ansible_object.get(key)
    return result
