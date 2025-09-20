from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nat_port_forwards parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Nat_port_forwardsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Nat_port_forwardsTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [

    ]
    # fmt: on


def oid():
    return "nat"


def field_map():

    return {
        "index": "Index",
        "enable": "Enable",
        "protocol": "Protocol",
        "description": "Description",
        "interface": "Interface",
        "external_port_start": "ExternalPortStart",
        "external_port_end": "ExternalPortEnd",
        "internal_port_start": "InternalPortStart",
        "internal_port_end": "InternalPortEnd",
        "internal_client": "InternalClient",
        # "set_originating_ip": "SetOriginatingIP",
        "originating_ip_address": "OriginatingIpAddress",  # Add to test case
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
