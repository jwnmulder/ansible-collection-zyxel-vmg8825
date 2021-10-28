# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_static_dhcp,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_static_dhcp

    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.execute_module(failed=True)

    def test_403_failure(self):

        self.register_connection_call(
            method="GET", uri="/cgi-bin/DAL?oid=static_dhcp", status=403
        )

        set_module_args({"state": "gathered"})
        result = self.execute_module(failed=True)

        self.assertIn("Server returned error response, code=403", result["msg"])

    def test_ensure_command_called_httpapi(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    }
                ],
            },
        )

        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        self.assertIsNotNone(result.get("gathered"))

        data = result.get("gathered")[0]

        self.assertEqual(data.get("index"), 1)
        self.assertEqual(data.get("br_wan"), "Default")
        self.assertEqual(data.get("enable"), True)
        self.assertEqual(data.get("mac_addr"), "01:02:03:04:05:06:01")
        self.assertEqual(data.get("ip_addr"), "192.168.0.1")

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=static_dhcp")

    def test_update_with_same_info(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    }
                ],
            },
        )

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        self.assertEqual(data[0]["index"], 1)

        # update with same config
        # config should not have changed as it is exactly the same
        set_module_args({"config": data})
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

    def test_override_with_same_info_no_index_specified(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    }
                ],
            },
        )

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

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    }
                ],
            },
        )

        # {"Index":0,"BrWan":"Default","Enable":true,"MACAddr": "01:02:03:04:05:06:02","IPAddr":"192.168.0.2"}
        # {"result":"ZCFG_SUCCESS","ReplyMsg":"BrWan","ReplyMsgMultiLang":"","sessionkey":991640825}
        self.register_connection_call(
            method="POST",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["index"], 1)

        data.append(
            {
                # "Index": 1,
                "enable": True,
                "br_wan": "Default",
                "mac_addr": "01:02:03:04:05:06:02",
                "ip_addr": "192.168.0.2",
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

        # TODO: data: null can be removed
        # {
        #     "data": null,
        #     "method": "DELETE",
        #     "oid": "static_dhcp",
        #     "oid_index": 2
        # },
        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:02",
                        "IPAddr": "192.168.0.2",
                    },
                ],
            },
        )

        self.register_connection_call(
            method="DELETE",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

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

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 4,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:02",
                        "IPAddr": "192.168.0.2",
                    },
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:03",
                        "IPAddr": "192.168.0.3",
                    },
                    {
                        "Index": 3,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:04",
                        "IPAddr": "192.168.0.4",
                    },
                ],
            },
        )

        self.register_connection_call(
            method="DELETE",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

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

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:02",
                        "IPAddr": "192.168.0.2",
                    },
                ],
            },
        )

        self.register_connection_call(
            method="PUT",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

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

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": False,
                        "MACAddr": "",
                        "IPAddr": "",
                    },
                    {
                        "Index": 3,
                        "BrWan": "Default",
                        "Enable": False,
                        "MACAddr": "",
                        "IPAddr": "",
                    },
                ],
            },
        )

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        set_module_args({"config": data})
        result = self.execute_module(changed=False)

    def test_static_dhcp_merged(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:02",
                        "IPAddr": "192.168.0.2",
                    },
                ],
            },
        )

        self.register_connection_call(
            method="PUT",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update data
        data[1]["ip_addr"] = "192.168.0.3"

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})
        result = self.execute_module(changed=True)

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
            }
        ]
        self.execute_module(changed=True, commands=commands)

    def test_static_dhcp_merged_idempotent(self):
        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "Object": [
                    {
                        "Index": 1,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:01",
                        "IPAddr": "192.168.0.1",
                    },
                    {
                        "Index": 2,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:02",
                        "IPAddr": "192.168.0.2",
                    },
                ],
            },
        )

        self.register_connection_call(
            method="PUT",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "BrWan",
                "ReplyMsgMultiLang": "",
                "sessionkey": "100000001",
            },
        )

        # get current config
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)

        data = result["gathered"]

        # update device with new config
        # config should have changed
        set_module_args({"config": data, "state": "merged"})
        self.execute_module(changed=False, commands=[])

    # def test_eos_l3_interfaces_overridden(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet2",
    #                     ipv4=[dict(address="203.0.113.27/24")],
    #                 ),
    #                 dict(
    #                     name="Management1",
    #                     ipv4=[dict(address="dhcp")],
    #                     ipv6=[dict(address="auto-config")],
    #                 ),
    #             ],
    #             state="overridden",
    #         )
    #     )
    #     commands = [
    #         "interface Ethernet2",
    #         "no ipv6 address 2001:db8::1/64",
    #         "ip address 203.0.113.27/24",
    #         "interface Ethernet1",
    #         "no ip address",
    #         "interface Vlan100",
    #         "no ip address",
    #         "interface Loopback99",
    #         "no ip address",
    #     ]
    #     self.execute_module(changed=True, commands=commands)

    # def test_eos_l3_interfaces_overridden_idempotent(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
    #                 ),
    #                 dict(
    #                     name="Ethernet1",
    #                     ipv4=[
    #                         dict(address="192.0.2.12/24"),
    #                         dict(address="192.87.33.4/24", secondary=True),
    #                     ],
    #                 ),
    #                 dict(
    #                     name="Management1",
    #                     ipv4=[dict(address="dhcp")],
    #                     ipv6=[dict(address="auto-config")],
    #                 ),
    #                 dict(
    #                     name="Vlan100",
    #                     ipv4=[dict(address="192.13.45.12/24", virtual=True)],
    #                 ),
    #                 dict(name="Loopback99", ipv4=[dict(address="1.1.1.1/24")]),
    #             ],
    #             state="overridden",
    #         )
    #     )
    #     self.execute_module(changed=False, commands=[])

    # def test_eos_l3_interfaces_replaced(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet2",
    #                     ipv4=[dict(address="203.0.113.27/24")],
    #                 )
    #             ],
    #             state="replaced",
    #         )
    #     )
    #     commands = [
    #         "interface Ethernet2",
    #         "ip address 203.0.113.27/24",
    #         "no ipv6 address 2001:db8::1/64",
    #     ]
    #     self.execute_module(changed=True, commands=commands)

    # def test_eos_l3_interfaces_replaced_idempotent(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
    #                 ),
    #                 dict(
    #                     name="Ethernet1",
    #                     ipv4=[
    #                         dict(address="192.0.2.12/24"),
    #                         dict(address="192.87.33.4/24", secondary=True),
    #                     ],
    #                 ),
    #                 dict(
    #                     name="Management1",
    #                     ipv4=[dict(address="dhcp")],
    #                     ipv6=[dict(address="auto-config")],
    #                 ),
    #                 dict(
    #                     name="Vlan100",
    #                     ipv4=[dict(address="192.13.45.12/24", virtual=True)],
    #                 ),
    #                 dict(name="Loopback99", ipv4=[dict(address="1.1.1.1/24")]),
    #             ],
    #             state="replaced",
    #         )
    #     )
    #     self.execute_module(changed=False, commands=[])

    # def test_eos_l3_interfaces_deleted(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet2", ipv6=[dict(address="2001:db8::1/64")]
    #                 ),
    #                 dict(name="lo99", ipv4=[dict(address="1.1.1.1/24")]),
    #             ],
    #             state="deleted",
    #         )
    #     )
    #     commands = [
    #         "interface Ethernet2",
    #         "no ipv6 address 2001:db8::1/64",
    #         "interface Loopback99",
    #         "no ip address",
    #     ]
    #     self.execute_module(changed=True, commands=commands)

    # def test_eos_l3_interfaces_rendered(self):
    #     set_module_args(
    #         dict(
    #             config=[
    #                 dict(
    #                     name="Ethernet1",
    #                     ipv4=[dict(address="198.51.100.14/24")],
    #                 ),
    #                 dict(
    #                     name="Ethernet2",
    #                     ipv4=[dict(address="203.0.113.27/24")],
    #                 ),
    #             ],
    #             state="rendered",
    #         )
    #     )
    #     commands = [
    #         "interface Ethernet1",
    #         "ip address 198.51.100.14/24",
    #         "interface Ethernet2",
    #         "ip address 203.0.113.27/24",
    #     ]
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(
    #         sorted(result["rendered"]), sorted(commands), result["rendered"]
    #     )

    # def test_eos_l3_interfaces_parsed(self):
    #     commands = [
    #         "interface Ethernet1",
    #         "ip address 198.51.100.14/24",
    #         "interface Ethernet2",
    #         "ip address 203.0.113.27/24",
    #     ]
    #     parsed_str = "\n".join(commands)
    #     set_module_args(dict(running_config=parsed_str, state="parsed"))
    #     result = self.execute_module(changed=False)
    #     parsed_list = [
    #         {"name": "Ethernet1", "ipv4": [{"address": "198.51.100.14/24"}]},
    #         {"name": "Ethernet2", "ipv4": [{"address": "203.0.113.27/24"}]},
    #     ]
    #     self.assertEqual(parsed_list, result["parsed"])

    # def test_eos_l3_interfaces_gathered(self):
    #     set_module_args(dict(state="gathered"))
    #     result = self.execute_module(changed=False)
    #     gather_list = [
    #         {
    #             "name": "Ethernet1",
    #             "ipv4": [
    #                 {"address": "192.0.2.12/24"},
    #                 {"address": "192.87.33.4/24", "secondary": True},
    #             ],
    #         },
    #         {"name": "Ethernet2", "ipv6": [{"address": "2001:db8::1/64"}]},
    #         {
    #             "name": "Management1",
    #             "ipv4": [{"address": "dhcp"}],
    #             "ipv6": [{"address": "auto-config"}],
    #         },
    #         {
    #             "ipv4": [{"address": "192.13.45.12/24", "virtual": True}],
    #             "name": "Vlan100",
    #         },
    #         {"ipv4": [{"address": "1.1.1.1/24"}], "name": "Loopback99"},
    #     ]
    #     self.assertEqual(gather_list, result["gathered"])
