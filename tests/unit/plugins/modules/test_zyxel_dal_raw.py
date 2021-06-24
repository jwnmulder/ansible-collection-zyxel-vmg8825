# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import responses

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_dal_raw

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_dal_raw

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @responses.activate
    def test_ensure_command_called_local(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=static_dhcp",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        result = self._run_module(
            self.module,
            {
                "api_oid": "PINGTEST",
                "api_method": "get",
            },
        )

        self.assertFalse(result["changed"])

    # @httpretty.activate(verbose=True, allow_net_connect=False)
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

        result = self._run_module(
            self.module,
            {
                "api_oid": "static_dhcp",
                "api_method": "get",
            },
        )

        self.assertFalse(result["changed"])
        self.assertFalse(result["changed"])
        self.assertEquals(result["response"]["result"], "ZCFG_SUCCESS")
        self.assertIsNotNone(result["response"]["Object"])
        self.assertEquals(result["result"], "ZCFG_SUCCESS")
        self.assertIsNotNone(result["obj"])
