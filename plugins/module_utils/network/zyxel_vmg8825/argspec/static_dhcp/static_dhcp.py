#
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The arg spec for the zyxel_static_dhcp module
"""


class Static_dhcpArgs:  # pylint: disable=R0903
    """The arg spec for the zyxel_static_dhcp module"""

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "elements": "dict",
            "options": {
                "br_wan": {"default": "Default", "type": "string"},
                "enable": {"type": "bool"},
                "index": {"type": "int"},
                "ip_addr": {"type": "string"},
                "mac_addr": {"type": "string"},
            },
            "type": "list",
        },
        "state": {
            "choices": ["merged", "replaced", "overridden", "deleted"],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
