# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)

__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_static_dhcp_table,
)


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_vmg8825_static_dhcp_table

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

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

        result = self._run_module(self.module, {"state": "gathered"})

        self.assertFalse(result["changed"])
        self.assertIsNotNone(result["gathered"])

        data = result["gathered"][0]

        self.assertFalse(result["changed"])
        self.assertEqual(data["index"], 1)
        self.assertEqual(data["br_wan"], "Default")
        self.assertEqual(data["enable"], True)
        self.assertEqual(data["mac_addr"], "01:02:03:04:05:06:01")
        self.assertEqual(data["ip_addr"], "192.168.0.1")

        args = self.connection.send_request.call_args
        self.assertEqual(args[1]["method"].upper(), "GET")
        self.assertEqual(args[1]["path"], "/cgi-bin/DAL?oid=static_dhcp")

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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        self.assertFalse(result["changed"])
        self.assertEqual(data[0]["index"], 1)

        # update with same config
        result = self._run_module(self.module, {"config": data})

        # config should not have changed as it is exactly the same
        self.assertFalse(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET",
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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]
        del data[0]["index"]

        # update with same config
        result = self._run_module(self.module, {"state": "overridden", "config": data})

        # config should not have changed as it is exactly the same
        self.assertFalse(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET",
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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        self.assertFalse(result["changed"])
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
        result = self._run_module(self.module, {"config": data})

        # config should have changed
        self.assertTrue(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET"
                and (x.kwargs["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0].kwargs["method"], "POST")

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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        # remove first item
        data.pop(0)

        # update device with new config
        result = self._run_module(self.module, {"state": "overridden", "config": data})

        # config should have changed
        self.assertTrue(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET"
                and (x.kwargs["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0].kwargs["method"], "DELETE")

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
                    {
                        "Index": 3,
                        "BrWan": "Default",
                        "Enable": True,
                        "MACAddr": "01:02:03:04:05:06:03",
                        "IPAddr": "192.168.0.3",
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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        # remove first two items
        data.pop(0)
        data.pop(0)

        # delete all entries
        result = self._run_module(self.module, {"state": "overridden", "config": data})

        # config should have changed
        self.assertTrue(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET"
                and (x.kwargs["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 2)
        self.assertEqual(static_dhcp_calls[0].kwargs["method"], "DELETE")
        self.assertEqual(static_dhcp_calls[1].kwargs["method"], "DELETE")
        self.assertEqual(
            static_dhcp_calls[0].kwargs["path"], "/cgi-bin/DAL?oid=static_dhcp&Index=2"
        )
        self.assertEqual(
            static_dhcp_calls[1].kwargs["path"], "/cgi-bin/DAL?oid=static_dhcp&Index=1"
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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        # update data
        data[1]["ip_addr"] = "192.168.0.3"

        # update device with new config
        result = self._run_module(self.module, {"config": data})

        # config should have changed
        self.assertTrue(result["changed"])

        # check requests that have been sent
        static_dhcp_calls = list(
            filter(
                lambda x: x.kwargs["method"] != "GET"
                and (x.kwargs["path"].find("/cgi-bin/DAL?oid=static_dhcp") >= 0),
                self.connection.send_request.call_args_list,
            )
        )

        self.assertEqual(len(static_dhcp_calls), 1)
        self.assertEqual(static_dhcp_calls[0].kwargs["method"], "PUT")

        request_data = static_dhcp_calls[0].args[0]
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
        result = self._run_module(self.module, {"state": "gathered"})

        data = result["gathered"]

        # update device with new config
        result = self._run_module(self.module, {"config": data})
