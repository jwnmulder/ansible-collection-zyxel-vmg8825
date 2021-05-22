# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825 import (
    HttpApi,
)

__metaclass__ = type

import json
import responses
import pytest

from ansible.module_utils.six import BytesIO
from ansible.module_utils import basic
from ansible_collections.ansible.netcommon.tests.unit.compat import (
    mock,
)
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.community.network.tests.unit.compat.mock import PropertyMock
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_ping
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.test_utils import (
    ZyxelModuleTestCase,
    mocked_response,
)


class TestZyxelModuleLocal(ZyxelModuleTestCase):

    module = zyxel_ping

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @responses.activate
    def test_ensure_command_called_local(self):

        self.request_mock.side_effect = [
            mocked_response(
                {
                    "result": "ZCFG_SUCCESS",
                    "ReplyMsg": "DNSServer",
                    "ReplyMsgMultiLang": "",
                    "Object": [{"DiagnosticsState": "None"}],
                }
            )
        ]
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(
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
                {
                    "url": "https://127.0.0.1",
                    "username": "username",
                    "password": "fakepassword",
                }
            )

            with self.assertRaises(AnsibleExitJson) as result:
                self.module.main()

            self.assertFalse(result.exception.args[0]["changed"])
            # self.request_mock.assert_called_once_with(Attrs(selector=('/UserLogin')), Any(), Any())


class FakeZyxelHttpApi(HttpApi):
    def __init__(self, conn):
        super().__init__(conn)
        self.hostvars = {
            # 'token_path': '/testLoginUrl',
            # 'spec_path': '/testSpecUrl'
        }

    def get_option(self, var):
        return self.hostvars[var]

    def set_option(self, var, val):
        self.hostvars[var] = val


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_ping

    def setUp(self):
        super().setUp()
        self.connection_mock = mock.Mock()
        self.zyxelhttp_plugin = FakeZyxelHttpApi(self.connection_mock)
        self.zyxelhttp_plugin._load_name = "httpapi"

    def tearDown(self):
        super().tearDown()

    # test_ftpd_install.py
    @pytest.fixture(autouse=True)
    def module_mock(self, mocker):
        mocker.patch.object(
            basic.AnsibleModule,
            "_socket_path",
            new_callable=PropertyMock,
            create=True,
            return_value=mocker.MagicMock(),
        )

    @pytest.fixture(autouse=True)
    def connection_mock(self, mocker):
        connection_class_mock = mocker.patch(
            "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.ansible_utils.Connection"
        )
        return connection_class_mock.return_value

    @staticmethod
    def _connection_response(response, status=200):
        response_mock = mock.Mock()
        response_mock.getcode.return_value = status
        response_text = json.dumps(response) if type(response) is dict else response
        response_data = BytesIO(
            response_text.encode() if response_text else "".encode()
        )
        return response_mock, response_data

    @pytest.mark.skip(reason="not working yet")
    def test_ensure_command_called_httpapi(self):

        self.request_mock.side_effect = [
            mocked_response(
                {
                    "result": "ZCFG_SUCCESS",
                    "ReplyMsg": "DNSServer",
                    "ReplyMsgMultiLang": "",
                    "Object": [{"DiagnosticsState": "None"}],
                }
            )
        ]

        with self.assertRaises(AnsibleExitJson) as result:
            self.module.main()

        self.assertFalse(result.exception.args[0]["changed"])
