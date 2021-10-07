# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_ping
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_ping

    def test_ensure_command_called_httpapi(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=PINGTEST",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        result = self._run_module(self.module, {})

        self.assertFalse(result["changed"])
        # self.assertEquals(result["response"]["result"], "ZCFG_SUCCESS")
        # self.assertIsNotNone(result["response"]["Object"])
        self.assertEqual(result["result"], "ZCFG_SUCCESS")
        self.assertIsNotNone(result["obj"])

        args = self.connection.send_request.call_args
        self.assertEqual(args[1]["method"].upper(), "GET")
        self.assertEqual(args[1]["path"], "/cgi-bin/DAL?oid=PINGTEST")


# TODO Test that Zyxel reponses with a non SUCCESS result get logge in the module output
# For example a failing logout
