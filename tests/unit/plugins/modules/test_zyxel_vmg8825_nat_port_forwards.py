from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_nat_port_forwards,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_nat_port_forwards

    def test_nat_port_forwards_merged(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "PUT")
        self.mock_dal_request("nat", "POST")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["description"] = "updated service name"
        data.append(
            {
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 21",
                "interface": "IP.Interface.7",
                "external_port_start": 21,
                "external_port_end": 21,
                "internal_port_start": 21,
                "internal_port_end": 21,
                "internal_client": "192.168.0.2",
            }
        )

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})

        commands = [
            {
                "oid": "nat",
                "method": "PUT",
                "data": {
                    "Index": 2,
                    "Enable": True,
                    "Protocol": "TCP",
                    "Description": "updated service name",
                    "Interface": "IP.Interface.7",
                    "ExternalPortStart": 80,
                    "ExternalPortEnd": 80,
                    "InternalPortStart": 80,
                    "InternalPortEnd": 80,
                    "InternalClient": "192.168.0.2",
                    "OriginatingIpAddress": None,
                },
            },
            {
                "oid": "nat",
                "method": "POST",
                "data": {
                    "Index": None,
                    "Enable": True,
                    "Protocol": "TCP",
                    "Description": "app forward port 21",
                    "Interface": "IP.Interface.7",
                    "ExternalPortStart": 21,
                    "ExternalPortEnd": 21,
                    "InternalPortStart": 21,
                    "InternalPortEnd": 21,
                    "InternalClient": "192.168.0.2",
                    "OriginatingIpAddress": None,
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_nat_port_forwards_merged_idempotent(self):

        self.mock_dal_request("nat", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "merged"})
        self.execute_module(changed=False, commands=[])

    def test_nat_port_forwards_overridden(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "PUT")
        self.mock_dal_request("nat", "DELETE")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[0]["description"] = "updated service name"
        data.pop(1)  # remove an entry

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "overridden"})
        commands = [
            {"oid": "nat", "method": "DELETE", "oid_index": 2},
            {
                "oid": "nat",
                "method": "PUT",
                "data": {
                    "Index": 1,
                    "Enable": True,
                    "Protocol": "TCP",
                    "Description": "updated service name",
                    "Interface": "IP.Interface.7",
                    "ExternalPortStart": 443,
                    "ExternalPortEnd": 443,
                    "InternalPortStart": 443,
                    "InternalPortEnd": 443,
                    "InternalClient": "192.168.0.2",
                    "OriginatingIpAddress": "192.168.0.1",
                    # TODO, missing X_ZYXEL_AutoDetectWanStatus, not sure if this is an issue
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_nat_port_forwards_overridden_idempotent(self):

        self.mock_dal_request("nat", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should not have changed
        set_module_args({"config": data, "state": "overridden"})
        self.execute_module(changed=False, commands=[])

    def test_nat_port_forwards_replaced(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # state=replaced will only update the provided subsections
        # we test this by removing one entry
        data.pop(1)

        # update data
        data[0]["description"] = "updated service name"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "replaced"})
        commands = [
            {
                "oid": "nat",
                "method": "PUT",
                "data": {
                    "Index": 1,
                    "Enable": True,
                    "Protocol": "TCP",
                    "Description": "updated service name",
                    "Interface": "IP.Interface.7",
                    "ExternalPortStart": 443,
                    "ExternalPortEnd": 443,
                    "InternalPortStart": 443,
                    "InternalPortEnd": 443,
                    "InternalClient": "192.168.0.2",
                    "OriginatingIpAddress": "192.168.0.1",
                },
            },
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_nat_port_forwards_replaced_idempotent(self):

        self.mock_dal_request("nat", "GET")

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

    def test_nat_port_forwards_deleted(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "DELETE")

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
            {"oid": "nat", "method": "DELETE", "oid_index": 2},
        ]

        self.execute_module(changed=True, commands=commands, sort=False)

    def test_nat_port_forwards_rendered(self):

        data = [
            {
                "index": 1,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 443",
                "interface": "IP.Interface.7",
                "external_port_start": 443,
                "external_port_end": 443,
                "internal_port_start": 443,
                "internal_port_end": 443,
                "internal_client": "192.168.0.2",
                "originating_ip_address": "192.168.0.1",
            },
            {
                "index": 2,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 80",
                "interface": "IP.Interface.7",
                "external_port_start": 80,
                "external_port_end": 80,
                "internal_port_start": 80,
                "internal_port_end": 80,
                "internal_client": "192.168.0.2",
            },
        ]
        set_module_args({"config": data, "state": "rendered"})
        expected = [
            {
                "Index": 1,
                "Enable": True,
                "Protocol": "TCP",
                "Description": "app forward port 443",
                "Interface": "IP.Interface.7",
                "ExternalPortStart": 443,
                "ExternalPortEnd": 443,
                "InternalPortStart": 443,
                "InternalPortEnd": 443,
                "InternalClient": "192.168.0.2",
                "OriginatingIpAddress": "192.168.0.1",
            },
            {
                "Index": 2,
                "Enable": True,
                "Protocol": "TCP",
                "Description": "app forward port 80",
                "Interface": "IP.Interface.7",
                "ExternalPortStart": 80,
                "ExternalPortEnd": 80,
                "InternalPortStart": 80,
                "InternalPortEnd": 80,
                "InternalClient": "192.168.0.2",
                "OriginatingIpAddress": None,
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], expected, result["rendered"])

    def test_nat_port_forwards_parsed(self):
        commands = [
            {
                "Index": 1,
                "Enable": True,
                "Protocol": "TCP",
                "Description": "app forward port 443",
                "Interface": "IP.Interface.7",
                "ExternalPortStart": 443,
                "ExternalPortEnd": 443,
                "InternalPortStart": 443,
                "InternalPortEnd": 443,
                "InternalClient": "192.168.0.2",
                "OriginatingIpAddress": None,
            },
            {
                "Index": 2,
                "Enable": True,
                "Protocol": "TCP",
                "Description": "app forward port 80",
                "Interface": "IP.Interface.7",
                "ExternalPortStart": 80,
                "ExternalPortEnd": 80,
                "InternalPortStart": 80,
                "InternalPortEnd": 80,
                "InternalClient": "192.168.0.2",
                "OriginatingIpAddress": None,
            },
        ]
        parsed_str = json.dumps(commands)
        set_module_args(dict(running_config=parsed_str, state="parsed"))
        result = self.execute_module(changed=False)

        parsed_list = [
            {
                "index": 1,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 443",
                "interface": "IP.Interface.7",
                "external_port_start": 443,
                "external_port_end": 443,
                "internal_port_start": 443,
                "internal_port_end": 443,
                "internal_client": "192.168.0.2",
            },
            {
                "index": 2,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 80",
                "interface": "IP.Interface.7",
                "external_port_start": 80,
                "external_port_end": 80,
                "internal_port_start": 80,
                "internal_port_end": 80,
                "internal_client": "192.168.0.2",
            },
        ]
        self.assertEqual(parsed_list, result["parsed"])

    def test_nat_port_forwards_gathered(self):

        self.mock_dal_request("nat", "GET")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        gather_list = [
            {
                "index": 1,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 443",
                "interface": "IP.Interface.7",
                "external_port_start": 443,
                "external_port_end": 443,
                "internal_port_start": 443,
                "internal_port_end": 443,
                "internal_client": "192.168.0.2",
                "originating_ip_address": "192.168.0.1",
            },
            {
                "index": 2,
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 80",
                "interface": "IP.Interface.7",
                "external_port_start": 80,
                "external_port_end": 80,
                "internal_port_start": 80,
                "internal_port_end": 80,
                "internal_client": "192.168.0.2",
            },
        ]

        self.assertEqual(gather_list, result["gathered"])

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=nat")

    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.execute_module(failed=True)

    def test_403_failure(self):

        self.mock_http_request(method="GET", uri="/cgi-bin/DAL?oid=nat", status=403)

        set_module_args({"state": "gathered"})
        result = self.execute_module(failed=True)

        self.assertIn("Server returned error response, code=403", result["msg"])

    def test_overridden_with_same_info_no_index_specified(self):

        self.mock_dal_request("nat", "GET")

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

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "POST")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        data.append(
            {
                "enable": True,
                "protocol": "TCP",
                "description": "app forward port 21",
                "interface": "IP.Interface.7",
                "external_port_start": 21,
                "external_port_end": 21,
                "internal_port_start": 21,
                "internal_port_end": 21,
                "internal_client": "192.168.0.2",
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
                and (x[1]["path"].find("/cgi-bin/DAL?oid=nat") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(http_calls), 1)
        self.assertEqual(http_calls[0][1]["method"], "POST")

    def test_delete_entry(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "DELETE")

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
                and (x[1]["path"].find("/cgi-bin/DAL?oid=nat") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(http_calls), 1)
        self.assertEqual(http_calls[0][1]["method"], "DELETE")

    def test_delete_multiple_entries_should_occur_backwards(self):

        self.mock_dal_request("nat", "GET", variant="deleteorder")
        self.mock_dal_request("nat", "DELETE")

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
                and (x[1]["path"].find("/cgi-bin/DAL?oid=nat") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        # self.assertEqual(len(http_calls), 2)
        self.assertEqual(http_calls[0][1]["method"], "DELETE")
        self.assertEqual(http_calls[1][1]["method"], "DELETE")
        self.assertEqual(http_calls[2][1]["method"], "DELETE")

        # If deletes would start at index=1, index=2 will not exist anymore on the remote device.
        # Assert that deletes happen form the higest index to the lowest
        self.assertEqual(http_calls[0][1]["path"], "/cgi-bin/DAL?oid=nat&Index=4")
        self.assertEqual(http_calls[1][1]["path"], "/cgi-bin/DAL?oid=nat&Index=2")
        self.assertEqual(http_calls[2][1]["path"], "/cgi-bin/DAL?oid=nat&Index=1")

    def test_update_entry(self):

        self.mock_dal_request("nat", "GET")
        self.mock_dal_request("nat", "PUT")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["description"] = "updated service name"

        # update device with new config
        # config should have changed
        set_module_args({"config": data})
        result = self.execute_module(changed=True)

        # check requests that have been sent
        http_calls = list(
            filter(
                lambda x: x[1]["method"] != "GET"
                and (x[1]["path"].find("/cgi-bin/DAL?oid=nat") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(http_calls), 1)
        self.assertEqual(http_calls[0][1]["method"], "PUT")

        request_data = http_calls[0][0][0]
        self.assertEqual(request_data["Description"], "updated service name")

    def test_update_with_incomplete_entry_in_response(self):

        self.mock_dal_request("nat", "GET", variant="incomplete_data")

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        set_module_args({"config": data})
        self.execute_module(changed=False)
