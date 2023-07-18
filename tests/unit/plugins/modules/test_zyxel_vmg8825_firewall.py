from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_firewall,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_firewall

    def test_firewall_merged(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data["dos_enabled"] = "false"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})

        commands = [
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {
                    "IPv4_Enable": True,
                    "IPv6_Enable": True,
                    "Level_GUI": "Low",
                    "enableDos": False,
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_firewall_merged_idempotent(self):

        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "merged"})
        self.execute_module(changed=False, commands=[])

    def test_firewall_overridden(self):
        """
        for the firewall resource module, overridden should behave in
        the same as way as merged
        """
        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data["dos_enabled"] = "false"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "overridden"})

        commands = [
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {
                    "IPv4_Enable": True,
                    "IPv6_Enable": True,
                    "Level_GUI": "Low",
                    "enableDos": False,
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_firewall_overridden_idempotent(self):

        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "overridden"})
        self.execute_module(changed=False, commands=[])

    def test_firewall_replaced(self):
        """
        for the firewall resource module, replaced should behave in
        the same as way as merged
        """
        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data["dos_enabled"] = "false"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "replaced"})

        commands = [
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {
                    "IPv4_Enable": True,
                    "IPv6_Enable": True,
                    "Level_GUI": "Low",
                    "enableDos": False,
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_firewall_replaced_idempotent(self):

        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "replaced"})
        self.execute_module(changed=False, commands=[])

    def test_firewall_rendered(self):

        data = {
            "ipv4_enabled": True,
            "ipv6_enabled": True,
            "dos_enabled": True,
            "level": "High",
        }

        set_module_args({"config": data, "state": "rendered"})
        expected = [
            {
                "IPv4_Enable": True,
                "IPv6_Enable": True,
                "enableDos": True,
                "Level_GUI": "High",
            }
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], expected, result["rendered"])

    def test_firewall_parsed(self):
        commands = [
            {
                "IPv4_Enable": True,
                "IPv6_Enable": True,
                "enableDos": True,
                "Level_GUI": "High",
            },
        ]
        parsed_str = json.dumps(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)

        parsed = {
            "ipv4_enabled": True,
            "ipv6_enabled": True,
            "dos_enabled": True,
            "level": "High",
        }

        self.assertEqual(parsed, result["parsed"])

    def test_firewall_gathered(self):

        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        gather = {
            "ipv4_enabled": True,
            "ipv6_enabled": True,
            "dos_enabled": True,
            "level": "Low",
        }

        self.assertEqual(gather, result["gathered"])

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=firewall")

    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.execute_module(failed=True)

    def test_403_failure(self):

        self.mock_http_request(
            method="GET", uri="/cgi-bin/DAL?oid=firewall", status=403
        )

        set_module_args({"state": "gathered"})
        result = self.execute_module(failed=True)

        self.assertIn("Server returned error response, code=403", result["msg"])

    def test_update_entry(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data["level"] = "Off"

        # update device with new config
        # config should have changed
        set_module_args({"config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        http_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=firewall") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(http_calls), 1)
        self.assertEqual(http_calls[0][1]["method"], "PUT")

        request_data = http_calls[0][1]["data"]
        self.assertEqual(request_data["Level_GUI"], "Off")
