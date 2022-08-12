from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest

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
        data["ipv4_enabled"] = "false"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})

        commands = [
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {"ipv4_enable": True},
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

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")
        self.mock_dal_request("firewall", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[0]["protocol"] = "TCP"
        data.pop(1)  # remove an entry

        # without index, Index will be determined based on 'name'
        del data[0]["index"]

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "overridden"})
        commands = [
            {"oid": "firewall", "method": "DELETE", "oid_index": 2},
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {
                    "Index": 1,
                    "Name": "Name-1",
                    "Order": 1,
                    "Protocol": "TCP",
                    "Direction": "LAN_TO_WAN",
                    "IPVersion": "IPv4",
                    "SourceIP": "192.168.0.0",
                    "SourceMask": "24",
                    "DestIP": "1.0.0.1",
                    "DestMask": "32",
                    "Target": "Reject",
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

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # state=replaced will only update the provided subsections
        # we test this by removing one entry
        data.pop(1)

        # update data
        data[0]["protocol"] = "TCP_UDP"

        # without index, Index will be determined based on 'name'
        del data[0]["index"]

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "replaced"})
        commands = [
            {
                "oid": "firewall",
                "method": "PUT",
                "data": {
                    "Index": 1,
                    "Name": "Name-1",
                    "Order": 1,
                    "Protocol": "TCPUDP",
                    "Direction": "LAN_TO_WAN",
                    "IPVersion": "IPv4",
                    "SourceIP": "192.168.0.0",
                    "SourceMask": "24",
                    "DestIP": "1.0.0.1",
                    "DestMask": "32",
                    "Target": "Reject",
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

        # state=replaced will only update the provided subsections
        # we test this by removing one entry
        data.pop(0)

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "replaced"})
        self.execute_module(changed=False, commands=[])

    def test_firewall_deleted(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "DELETE")

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
            {"oid": "firewall", "method": "DELETE", "oid_index": 2},
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_firewall_rendered(self):

        data = [
            {
                "index": 1,
                "name": "Name-1",
                "order": 1,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.1",
                "dest_mask": "32",
                "target": "Reject",
                # "source_port": -1,
                # "source_port_range_max": -1,
                # "dest_port": -1,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
            {
                "index": 2,
                "name": "Name-2",
                "order": 2,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.2",
                "dest_mask": "32",
                "target": "Reject",
                # "source_port": -1,
                # "source_port_range_max": -1,
                # "dest_port": -1,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
        ]
        set_module_args({"config": data, "state": "rendered"})
        expected = [
            {
                "Index": 1,
                "Name": "Name-1",
                "Order": 1,
                "Protocol": "ALL",
                "Direction": "LAN_TO_WAN",
                "IPVersion": "IPv4",
                "SourceIP": "192.168.0.0",
                "SourceMask": "24",
                "DestIP": "1.0.0.1",
                "DestMask": "32",
                "Target": "Reject",
            },
            {
                "Index": 2,
                "Name": "Name-2",
                "Order": 2,
                "Protocol": "ALL",
                "Direction": "LAN_TO_WAN",
                "IPVersion": "IPv4",
                "SourceIP": "192.168.0.0",
                "SourceMask": "24",
                "DestIP": "1.0.0.2",
                "DestMask": "32",
                "Target": "Reject",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], expected, result["rendered"])

    def test_firewall_parsed(self):
        commands = [
            {
                "Index": 1,
                "Name": "Name-1",
                "Order": 1,
                "Protocol": "ALL",
                "Direction": "LAN_TO_WAN",
                "IPVersion": 4,
                "SourceIP": "192.168.0.0",
                "SourceMask": "24",
                "DestIP": "1.0.0.1",
                "DestMask": "32",
                "Target": "Reject",
            },
            {
                "Index": 2,
                "Name": "Name-2",
                "Order": 2,
                "Protocol": "ALL",
                "Direction": "LAN_TO_WAN",
                "IPVersion": 4,
                "SourceIP": "192.168.0.0",
                "SourceMask": "24",
                "DestIP": "1.0.0.2",
                "DestMask": "32",
                "Target": "Reject",
            },
        ]
        parsed_str = json.dumps(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)

        parsed_list = [
            {
                "index": 1,
                "name": "Name-1",
                "order": 1,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.1",
                "dest_mask": "32",
                "target": "Reject",
                # "source_port": -1,
                # "source_port_range_max": -1,
                # "dest_port": -1,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
            {
                "index": 2,
                "name": "Name-2",
                "order": 2,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.2",
                "dest_mask": "32",
                "target": "Reject",
                # "source_port": -1,
                # "source_port_range_max": -1,
                # "dest_port": -1,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_firewall_gathered(self):

        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        gather_list = [
            {
                "index": 1,
                "name": "Name-1",
                "order": 1,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.1",
                "dest_mask": "32",
                "target": "Reject",
                # "source_port": -1,
                # "source_port_range_max": -1,
                # "dest_port": -1,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
            {
                "index": 2,
                "name": "Name-2",
                "order": 2,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.2",
                "dest_mask": "32",
                "target": "Reject",
                "source_port": 53,
                # "source_port_range_max": -1,
                "dest_port": 53,
                # "dest_port_range_max": -1,
                # "limit_rate": 0,
            },
        ]

        self.assertEqual(gather_list, result["gathered"])

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

    def test_overridden_with_same_info_no_index_specified(self):

        self.mock_dal_request("firewall", "GET")

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
        http_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET",
                self.connection.send_request.call_args_list,
            )
        )

        # no PUT/POST/DELETE
        self.assertEqual(len(http_calls), 0)

    def test_add_entry(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "POST")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        data.append(
            {
                "name": "Name-3",
                "order": 3,
                "protocol": "ALL",
                "direction": "LAN_TO_WAN",
                "ip_version": "IPv4",
                "source_ip": "192.168.0.0",
                "source_mask": "24",
                "dest_ip": "1.0.0.3",
                "dest_mask": "32",
                "target": "Reject",
            }
        )

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
        self.assertEqual(http_calls[0][1]["method"], "POST")

    def test_delete_entry(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "DELETE")

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
        http_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=firewall") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(http_calls), 1)
        self.assertEqual(http_calls[0][1]["method"], "DELETE")

    def test_delete_multiple_entries_should_occur_backwards(self):

        self.mock_dal_request("firewall", "GET", variant="deleteorder")
        self.mock_dal_request("firewall", "DELETE")

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
        http_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=firewall") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        # self.assertEqual(len(http_calls), 2)
        self.assertEqual(http_calls[0][1]["method"], "DELETE")
        self.assertEqual(http_calls[1][1]["method"], "DELETE")
        self.assertEqual(http_calls[2][1]["method"], "DELETE")

        # If deletes would start at index=1, index=2 will not exist anymore on the remote device.
        # Assert that deletes happen form the higest index to the lowest
        self.assertEqual(http_calls[0][1]["path"], "/cgi-bin/DAL?oid=firewall&Index=4")
        self.assertEqual(http_calls[1][1]["path"], "/cgi-bin/DAL?oid=firewall&Index=2")
        self.assertEqual(http_calls[2][1]["path"], "/cgi-bin/DAL?oid=firewall&Index=1")

    def test_update_entry(self):

        self.mock_dal_request("firewall", "GET")
        self.mock_dal_request("firewall", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["protocol"] = "TCP"

        # without index, Index will be determined based on 'name'
        del data[1]["index"]

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

        request_data = http_calls[0][0][0]
        self.assertEqual(request_data["Protocol"], "TCP")

    def test_no_order_noop(self):
        """
        Test the no update is done if order is not provided
        """
        self.mock_dal_request("firewall", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]
        del data[0]["order"]
        del data[1]["order"]

        # update device with new the same config but no order
        # config should not have changed
        set_module_args({"config": data, "state": "overridden"})
        self.execute_module(changed=False, commands=[])

    @pytest.mark.skip(
        reason=(
            "not sure how to implement a workaround for this behavior while at the"
            " same time keeping input validation enabled for the resource module."
        )
    )
    def test_update_with_incomplete_entry_in_response(self):

        self.mock_dal_request("firewall", "GET", variant="incomplete_data")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with the same incomplete config
        set_module_args({"config": data})
        self.execute_module(changed=False)
