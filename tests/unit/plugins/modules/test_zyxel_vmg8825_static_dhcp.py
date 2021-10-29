# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_static_dhcp,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_static_dhcp

    def test_static_dhcp_merged(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "PUT")
        self.mock_dal_request("static_dhcp", "POST")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["ip_addr"] = "192.168.0.3"
        data.append(
            {
                "br_wan": "Default",
                "enable": True,
                "ip_addr": "192.168.0.4",
                "mac_addr": "01:02:03:04:05:06:04",
            }
        )

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})

        commands = [
            {
                "oid": "static_dhcp",
                "method": "PUT",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.0.3",
                    "Index": 2,
                    "MACAddr": "01:02:03:04:05:06:02",
                },
            },
            {
                "oid": "static_dhcp",
                "method": "POST",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.0.4",
                    "Index": None,
                    "MACAddr": "01:02:03:04:05:06:04",
                },
            },
        ]
        self.execute_module(changed=True, commands=commands, sort=False)

    def test_static_dhcp_merged_idempotent(self):

        self.mock_dal_request("static_dhcp", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "merged"})
        self.execute_module(changed=False, commands=[])

    def test_static_dhcp_overridden(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "PUT")
        self.mock_dal_request("static_dhcp", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[0]["ip_addr"] = "192.168.0.4"  # update entry
        data.pop(1)  # remove an entry

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "overridden"})
        commands = [
            {"oid": "static_dhcp", "method": "DELETE", "oid_index": 2},
            {
                "oid": "static_dhcp",
                "method": "PUT",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.0.4",
                    "Index": 1,
                    "MACAddr": "01:02:03:04:05:06:01",
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_static_dhcp_overridden_idempotent(self):

        self.mock_dal_request("static_dhcp", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "overridden"})
        self.execute_module(changed=False, commands=[])

    def test_static_dhcp_replaced(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # state=replaced will only update the provided subsections
        # we test this by removing one entry
        data.pop(1)

        # update data
        data[0]["ip_addr"] = "192.168.0.4"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "replaced"})
        commands = [
            {
                "oid": "static_dhcp",
                "method": "PUT",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.0.4",
                    "Index": 1,
                    "MACAddr": "01:02:03:04:05:06:01",
                },
            }
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_static_dhcp_replaced_idempotent(self):

        self.mock_dal_request("static_dhcp", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # state=replaced will only update the provided subsections
        # we test this by removing one entry
        data.pop(0)

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "replaced"})
        self.execute_module(changed=False, commands=[])

    def test_static_dhcp_deleted(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # delete an entry
        data.pop(0)

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "deleted"})
        commands = [
            {"oid": "static_dhcp", "method": "DELETE", "oid_index": 2},
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_static_dhcp_rendered(self):

        data = [
            {
                "br_wan": "Default",
                "enable": True,
                "index": 1,
                "ip_addr": "192.168.0.1",
                "mac_addr": "01:02:03:04:05:06:01",
            },
            {
                "br_wan": "Default",
                "enable": True,
                "index": 2,
                "ip_addr": "192.168.02",
                "mac_addr": "01:02:03:04:05:06:02",
            },
        ]
        set_module_args({"config": data, "state": "rendered"})
        commands = [
            {
                "oid": "static_dhcp",
                "method": "POST",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.0.1",
                    "Index": 1,
                    "MACAddr": "01:02:03:04:05:06:01",
                },
            },
            {
                "oid": "static_dhcp",
                "method": "POST",
                "data": {
                    "BrWan": "Default",
                    "Enable": True,
                    "IPAddr": "192.168.02",
                    "Index": 2,
                    "MACAddr": "01:02:03:04:05:06:02",
                },
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands, result["rendered"])

    def test_static_dhcp_parsed(self):
        commands = [
            {
                "BrWan": "Default",
                "Enable": True,
                "IPAddr": "192.168.0.1",
                "Index": 1,
                "MACAddr": "01:02:03:04:05:06:01",
            },
            {
                "BrWan": "Default",
                "Enable": True,
                "IPAddr": "192.168.02",
                "Index": 2,
                "MACAddr": "01:02:03:04:05:06:02",
            },
        ]
        parsed_str = json.dumps(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)

        parsed_list = [
            {
                "br_wan": "Default",
                "enable": True,
                "index": 1,
                "ip_addr": "192.168.0.1",
                "mac_addr": "01:02:03:04:05:06:01",
            },
            {
                "br_wan": "Default",
                "enable": True,
                "index": 2,
                "ip_addr": "192.168.02",
                "mac_addr": "01:02:03:04:05:06:02",
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_static_dhcp_gathered(self):

        self.mock_dal_request("static_dhcp", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        gather_list = [
            {
                "br_wan": "Default",
                "enable": True,
                "ip_addr": "192.168.0.1",
                "index": 1,
                "mac_addr": "01:02:03:04:05:06:01",
            },
            {
                "br_wan": "Default",
                "enable": True,
                "ip_addr": "192.168.0.2",
                "index": 2,
                "mac_addr": "01:02:03:04:05:06:02",
            },
        ]

        self.assertEqual(gather_list, result["gathered"])

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=static_dhcp")

    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.execute_module(failed=True)

    def test_403_failure(self):

        self.mock_http_request(
            method="GET", uri="/cgi-bin/DAL?oid=static_dhcp", status=403
        )

        set_module_args({"state": "gathered"})
        result = self.execute_module(failed=True)

        self.assertIn("Server returned error response, code=403", result["msg"])

    def test_overridden_with_same_info_no_index_specified(self):

        self.mock_dal_request("static_dhcp", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]
        del data[0]["index"]

        # update with same config
        # config should not have changed as it is exactly the same
        set_module_args({"state": "overridden", "config": data})
        result = self.execute_module(changed=False)

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET",
                self.connection.send_request.call_args_list,
            )
        )

        # no PUT/POST/DELETE
        self.assertEqual(len(static_dhcp_calls), 0)

    def test_add_entry(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "POST")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        data.append(
            {
                "enable": True,
                "br_wan": "Default",
                "mac_addr": "01:02:03:04:05:06:03",
                "ip_addr": "192.168.0.3",
            }
        )

        # update device with new config
        # config should have changed
        set_module_args({"config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0][1]["method"], "POST")

    def test_delete_entry(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # remove first item
        data.pop(0)

        # update device with new config
        # config should have changed
        set_module_args({"state": "overridden", "config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0][1]["method"], "DELETE")

    def test_delete_multiple_entries_should_occur_backwards(self):

        self.mock_dal_request("static_dhcp", "GET", variant="deleteorder")
        self.mock_dal_request("static_dhcp", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # remove first two items
        data.pop(0)
        data.pop(0)
        data.pop(0)

        # delete all entries
        # config should have changed
        set_module_args({"state": "overridden", "config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        # self.assertEqual(len(static_dhcp_calls), 2)
        self.assertEqual(static_dhcp_calls[0][1]["method"], "DELETE")
        self.assertEqual(static_dhcp_calls[1][1]["method"], "DELETE")
        self.assertEqual(static_dhcp_calls[2][1]["method"], "DELETE")

        # If deletes would start at index=1, index=2 will not exist anymore on the remote device.
        # Assert that deletes happen form the higest index to the lowest
        self.assertEqual(
            static_dhcp_calls[0][1]["path"], "/cgi-bin/DAL?oid=static_dhcp&Index=4"
        )
        self.assertEqual(
            static_dhcp_calls[1][1]["path"], "/cgi-bin/DAL?oid=static_dhcp&Index=2"
        )
        self.assertEqual(
            static_dhcp_calls[2][1]["path"], "/cgi-bin/DAL?oid=static_dhcp&Index=1"
        )

    def test_update_entry(self):

        self.mock_dal_request("static_dhcp", "GET")
        self.mock_dal_request("static_dhcp", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["ip_addr"] = "192.168.0.3"

        # update device with new config
        # config should have changed
        set_module_args({"config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0][1]["method"], "PUT")

        request_data = static_dhcp_calls[0][0][0]
        self.assertEqual(request_data["IPAddr"], "192.168.0.3")

    def test_update_with_incomplete_entry_in_response(self):

        self.mock_dal_request("static_dhcp", "GET", variant="incomplete_data")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        set_module_args({"config": data})
        self.execute_module(changed=False)
