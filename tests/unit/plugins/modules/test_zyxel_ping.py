# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import httpretty

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_ping
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.test_utils import (
    ZyxelModuleTestCase,
)


class TestZyxelModuleLocal(ZyxelModuleTestCase):

    module = zyxel_ping

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_ensure_command_called_local(self):

        self.register_uri(
            method="GET",
            uri="/cgi-bin/DAL?oid=PINGTEST",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        set_module_args(
            {
                "url": self.mock_http_url,
                "username": "username",
                "password": "fakepassword",
            }
        )

        with self.assertRaises(AnsibleExitJson) as result:
            self.module.main()

        self.assertFalse(result.exception.args[0]["changed"])

        self.assertEqual(len(httpretty.latest_requests()), 1)
        self.assertEqual(
            httpretty.last_request().url,
            f"{self.mock_http_url}/cgi-bin/DAL?oid=PINGTEST",
        )


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_ping

    def setUp(self):
        super().setUp(connection_type="httpapi")

    def tearDown(self):
        super().tearDown()

    # @pytest.mark.skip(reason="not working yet")
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_ensure_command_called_httpapi(self):

        self.register_uri(
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
