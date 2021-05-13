# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import responses

# from ansible.module_utils import basic
# from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
#     patch,
#     MagicMock,
# )
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_static_dhcp,
)


class TestZyxelModule(ModuleTestCase):

    module = zyxel_static_dhcp

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @responses.activate
    def test_ensure_command_called_local(self):

        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
                responses.GET,
                "https://127.0.0.1/cgi-bin/DAL?oid=static_dhcp",
                status=200,
                json={
                    "result": "ZCFG_SUCCESS",
                    "ReplyMsg": "DNSServer",
                    "ReplyMsgMultiLang": "",
                    "Object": [{"DiagnosticsState": "None"}],
                },
            )

            set_module_args(
                {
                    "url": "https://127.0.0.1",
                    "username": "username",
                    "password": "password",
                }
            )

            with self.assertRaises(AnsibleExitJson) as result:
                self.module.main()

            self.assertFalse(result.exception.args[0]["changed"])
