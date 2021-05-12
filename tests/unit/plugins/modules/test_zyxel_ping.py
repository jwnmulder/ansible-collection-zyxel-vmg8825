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
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_ping


class TestZyxelPing(ModuleTestCase):

    module = zyxel_ping

    def setUp(self):
        super().setUp()

        # self.mock_connection = patch(
        #     "ansible_collections.ansible.netcommon.plugins.modules.cli_config.Connection"
        # )
        # self.get_connection = self.mock_connection.start()

        # self.conn = self.get_connection()
        # self.conn.get_capabilities.return_value = "{}"

    def tearDown(self):
        super().tearDown()

        # self.mock_connection.stop()

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @responses.activate
    def test_ensure_command_called_local(self):

        responses.add(
            responses.GET,
            "https://127.0.0.1/cgi-bin/DAL?oid=PINGTEST",
            status=200,
            json={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        set_module_args(
            {"url": "https://127.0.0.1", "username": "username", "password": "password"}
        )

        # with patch.object(httpclient, 'run_command') as mock_run_command:
        #     stdout = 'configuration updated'
        #     stderr = ''
        #     rc = 0
        #     mock_run_command.return_value = rc, stdout, stderr  # successful execution

        with self.assertRaises(AnsibleExitJson) as result:
            self.module.main()
        # self.assertFalse(result.exception.args[0]['faidled']) # ensure result is changed
        self.assertFalse(
            result.exception.args[0]["changed"]
        )  # ensure result is changed
        # mock_run_command.assert_called_once_with('/usr/bin/my_command --value 10 --name test')
