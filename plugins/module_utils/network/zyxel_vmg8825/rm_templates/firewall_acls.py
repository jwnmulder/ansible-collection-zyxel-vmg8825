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
    result = {
        "index": dal_object.get("Index"),
        "name": dal_object.get("Name"),
        "order": dal_object.get("Order"),
        "direction": dal_object.get("Direction"),
        "target": dal_object.get("Target"),
        "ip_version": dal_object.get("IPVersion"),
        "source_ip": dal_object.get("SourceIP"),
        "source_mask": dal_object.get("SourceMask"),
        "dest_ip": dal_object.get("DestIP"),
        "dest_mask": dal_object.get("DestMask"),
    }

    protocol = dal_object.get("Protocol")
    if protocol is not None:
        protocol = protocol.replace("TCP/UDP", "TCP_UDP")
        result["protocol"] = protocol

    source_port = dal_object.get("SourcePort")
    if source_port is not None and source_port >= 0:
        result["source_port"] = source_port

    source_port_range_max = dal_object.get("SourcePortRangeMax")
    if source_port_range_max is not None and source_port_range_max >= 0:
        result["source_port_range_max"] = source_port_range_max

    dest_port = dal_object.get("DestPort")
    if dest_port is not None and dest_port >= 0:
        result["dest_port"] = dest_port

    dest_port_range_max = dal_object.get("DestPortRangeMax")
    if dest_port_range_max is not None and dest_port_range_max >= 0:
        result["dest_port_range_max"] = dest_port_range_max

    limit_rate = dal_object.get("LimitRate")
    if limit_rate is not None and limit_rate >= 1:
        result["limit_rate"] = limit_rate

    limit_rate_unit = dal_object.get("LimitRateUnit")
    if limit_rate_unit is not None and len(limit_rate_unit) > 0:
        result["limit_rate_unit"] = limit_rate_unit

    return result


def to_dal_object(ansible_object):

    result = {
        "Index": ansible_object.get("index"),
        "Name": ansible_object.get("name"),
        "Order": ansible_object.get("order"),
        "Direction": ansible_object.get("direction"),
        "Target": ansible_object.get("target"),
        "IPVersion": ansible_object.get("ip_version"),
        "SourceIP": ansible_object.get("source_ip"),
        "SourceMask": ansible_object.get("source_mask"),
        "DestIP": ansible_object.get("dest_ip"),
        "DestMask": ansible_object.get("dest_mask"),
    }

    protocol = ansible_object.get("protocol")
    if protocol is not None:
        protocol = protocol.replace("TCP_UDP", "TCP/UDP")
        result["Protocol"] = protocol

    source_port = ansible_object.get("source_port")
    if source_port is not None and source_port >= 0:
        result["SourcePort"] = source_port

    source_port_range_max = ansible_object.get("source_port_range_max")
    if source_port_range_max is not None and source_port_range_max >= 0:
        result["SourcePortRangeMax"] = source_port_range_max

    dest_port = ansible_object.get("dest_port")
    if dest_port is not None and dest_port >= 0:
        result["DestPort"] = dest_port

    dest_port_range_max = ansible_object.get("dest_port_range_max")
    if dest_port_range_max is not None and dest_port_range_max >= 0:
        result["DestPortRangeMax"] = dest_port_range_max

    limit_rate = ansible_object.get("limit_rate")
    if limit_rate is not None and limit_rate >= 1:
        result["LimitRate"] = limit_rate

    limit_rate_unit = ansible_object.get("limit_rate_unit")
    if limit_rate_unit is not None and len(limit_rate_unit) > 0:
        result["LimitRateUnit"] = limit_rate_unit

    return result


# def from_dal_object(dal_object):
#     result = {}
#     for key, value in field_map().items():
#         result[key] = dal_object.get(value)
#     return result


# def to_dal_object(ansible_object):
#     result = {}
#     for key, value in field_map().items():
#         result[value] = ansible_object.get(key)
#     return result
