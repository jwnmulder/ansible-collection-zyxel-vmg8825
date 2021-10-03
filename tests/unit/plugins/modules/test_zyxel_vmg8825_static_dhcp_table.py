# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)

__metaclass__ = type

import pytest

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_static_dhcp_table,
)


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_vmg8825_static_dhcp_table

    @pytest.mark.skip(reason="wip")
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

        result = self._run_module(self.module, {})

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
        result = self._run_module(self.module, {})

        data = result["gathered"]

        self.assertFalse(result["changed"])
        self.assertEqual(data[0]["index"], 1)

        # update with same config
        result = self._run_module(self.module, {"config": data})

        # config should not have changed as it is exactly the same
        self.assertFalse(result["changed"])
