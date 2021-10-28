# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)


__metaclass__ = type

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_ping,
)
from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_ping

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

        set_module_args({})
        result = self.execute_module(changed=False)

        self.assertEqual(result.get("result"), "ZCFG_SUCCESS")
        self.assertIsNotNone(result.get("obj"))

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=PINGTEST")


# TODO Test that Zyxel reponses with a non SUCCESS result get logged in the module output
# For example a failing logout
