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

    set_when_not_none(result, "ipv4_enabled", dal_object.get("IPv4_Enable"))
    set_when_not_none(result, "ipv6_enabled", dal_object.get("IPv6_Enable"))
    set_when_not_none(result, "dos_enabled", dal_object.get("enableDos"))
    set_when_not_empty(result, "level", dal_object.get("Level_GUI"))

    return result


def to_dal_object(ansible_object):

    result = {}

    set_when_not_none(result, "IPv4_Enable", ansible_object.get("ipv4_enabled"))
    set_when_not_none(result, "IPv6_Enable", ansible_object.get("ipv6_enabled"))
    set_when_not_none(result, "enableDos", ansible_object.get("dos_enabled"))
    set_when_not_empty(result, "Level_GUI", ansible_object.get("level"))

    return result


def set_when_not_none(d, key, value):
    if value is not None:
        d[key] = value


def set_when_not_empty(d, key, value):
    if value is not None and len(value) > 0:
        d[key] = value
