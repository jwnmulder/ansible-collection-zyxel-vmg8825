# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import logging
import pytest
import textwrap
import unittest

from unittest import mock

from ansible.module_utils.connection import ConnectionError
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825 import (
    HttpApi,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.mock import fake_httpapi
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.controller_test_utils import (
    # mocked_httperror,
    mocked_response,
)

logger = logging.getLogger(__name__)


class FakeZyxelHttpApiPlugin(HttpApi):
    def __init__(self, connection):

        self.hostvars = {"use_ssl": True, "host": "router.test"}
        super().__init__(connection)

        self.context.encrypted_payloads = False
        self._device_info = {
            "network_os": "zyxel",
            "network_os_version": "V5.50(ABPY.1)b16_20210525",
        }

    def get_option(self, option):
        return self.hostvars.get(option)

    def set_option(self, option, value):
        self.hostvars[option] = value


class TestZyxelHttpApi(unittest.TestCase):
    def setUp(self):
        self.connection = fake_httpapi.Connection()
        self.connection.hostvars["use_ssl"] = True

        self.zyxel_plugin = FakeZyxelHttpApiPlugin(self.connection)
        self.zyxel_plugin._load_name = "httpapi"
        self.connection.httpapi = self.zyxel_plugin

        self.request_patch = mock.patch("ansible.module_utils.urls.Request.open")
        self.request_mock = self.request_patch.start()
        # self.request_patch = mock.patch("urllib.request.urlopen") # use the above instead?
        # self.request_mock = self.request_patch.start()

    def tearDown(self):
        self.request_patch.stop()

    def test_login_raises_exception_when_username_and_password_are_not_provided(self):

        with self.assertRaises(ValueError) as res:
            self.zyxel_plugin.login(None, None)

        assert "Please provide username/password to login" in str(res.exception)

    @pytest.mark.skip(reason="not working yet")
    def test_login_raises_exception_when_invalid_response(self):

        self.request_mock.side_effect = [
            mocked_response(response={"invalid": "data"}, status=500)
        ]

        with self.assertRaises(ConnectionError) as res:
            self.zyxel_plugin.login("admin", "fakepassword")

        assert (
            "Server returned response without token info during connection"
            " authentication" in str(res.exception)
        )

    def test_detect_encryption_mode_enabled(self):

        self.request_mock.side_effect = [
            mocked_response(
                response={
                    "result": "ZCFG_SUCCESS",
                    "ModelName": "VMG8825-T50",
                    "SoftwareVersion": "V5.50(ABPY.1)b21_20230112",
                    "CurrentLanguage": "en",
                    "AvailableLanguages": "en",
                    "RememberPassword": 0,
                    "DebugMode": False,
                    "RemoAddr_Type": "WAN",
                },
                status=200,
            )
        ]

        self.zyxel_plugin.context.encrypted_payloads = None
        self.zyxel_plugin._device_info = None

        self.zyxel_plugin.detect_router_api_capabilities()
        device_info = self.zyxel_plugin.get_device_info()

        assert device_info["network_os_version"] == "V5.50(ABPY.1)b21_20230112"
        assert self.zyxel_plugin.context.encrypted_payloads is True

    def test_detect_encryption_mode_disabled(self):

        self.request_mock.side_effect = [
            mocked_response(
                response={
                    "result": "ZCFG_SUCCESS",
                    "ModelName": "VMG8825-T50",
                    "SoftwareVersion": "V5.50(ABPY.1)b16_20210525",
                    "CurrentLanguage": "en",
                    "AvailableLanguages": "en",
                    "RememberPassword": 0,
                    "DebugMode": False,
                    "RemoAddr_Type": "WAN",
                },
                status=200,
            )
        ]

        self.zyxel_plugin.context.encrypted_payloads = None
        self.zyxel_plugin._device_info = None

        self.zyxel_plugin.detect_router_api_capabilities()
        device_info = self.zyxel_plugin.get_device_info()

        assert device_info["network_os_version"] == "V5.50(ABPY.1)b16_20210525"
        assert self.zyxel_plugin.context.encrypted_payloads is False

    @pytest.mark.skip(
        reason=(
            "We don't align with ftd.py here. Not sure what is recommended for"
            " json-rpc?"
        )
    )
    def test_send_request_should_return_error_info_when_http_error_raises(self):

        self.request_mock.side_effect = [
            mocked_response(response={"errorMessage": "ERROR"}, status=500)
        ]

        response_data = self.zyxel_plugin.send_request(None, path="/test")

        assert response_data[0] == {"errorMessage": "ERROR"}

    def test_login_max_nr_reached_error(self):

        self.request_mock.side_effect = [
            mocked_response(
                response={"result": "Maxium number of login account has reached"},
                status=401,
                # msg="Unauthorized",
                # url="/UserLogin",
            )
        ]

        with self.assertRaises(ConnectionError) as res:
            self.zyxel_plugin.login("USERNAME", "PASSWORD")

        assert "Maxium number of login account has reached" in str(res.exception)

    def test_login(self):

        username = "admin"
        sessionkey = "358987652"

        self.request_mock.side_effect = [
            mocked_response(
                url="/UserLogin",
                status=200,
                response={
                    "sessionkey": sessionkey,
                    "ThemeColor": "blue",
                    "changePw": False,
                    "showSkipBtn": False,
                    "quickStart": True,
                    "loginAccount": username,
                    "loginLevel": "medium",
                    "result": "ZCFG_SUCCESS",
                },
            ),
        ]

        # no session should exist yet
        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin.context.sessionkey, sessionkey)

        # login
        self.zyxel_plugin.login(username, "PASSWORD")

        # assert that a login session exists
        self.assertIsNotNone(self.zyxel_plugin.connection._auth)
        self.assertEqual(self.zyxel_plugin.context.sessionkey, sessionkey)

        self.assertTrue(
            any(
                x[1][0] == "POST" and x[1][1].find("/UserLogin")
                for x in self.request_mock.mock_calls
            )
        )

    def test_login_with_encryption(self):

        username = "admin"
        sessionkey = "358987652"

        self.request_mock.side_effect = [
            mocked_response(
                url="/getRSAPublicKey",
                status=200,
                response={
                    "RSAPublicKey": textwrap.dedent(
                        """
                        -----BEGIN PUBLIC KEY-----
                        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9+84erHfPJ9qCVnfD6SwFuPlP
                        gK6C4bH3z7+aWg0IGyKnhZ8vcef7Rl8vn4qLeM0AfXeI58ndHzwWvklLFow1IQtg
                        HhoaVnIYKSrGw7CcDLYjbP3e2mbj\\/sWxlyUick8asD0qwGXiXMsvfneyiU71Ye0w
                        +CSrIJUJLCco18CBqQIDAQAB
                        -----END PUBLIC KEY-----
                        """
                    ),
                    "result": "ZCFG_SUCCESS",
                },
            ),
            mocked_response(
                url="/UserLogin",
                status=200,
                response={
                    "sessionkey": sessionkey,
                    "ThemeColor": "blue",
                    "changePw": False,
                    "showSkipBtn": False,
                    "quickStart": True,
                    "loginAccount": username,
                    "loginLevel": "medium",
                    "result": "ZCFG_SUCCESS",
                },
            ),
        ]

        # no session should exist yet
        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin.context.sessionkey, sessionkey)

        self.zyxel_plugin.context.encrypted_payloads = True

        # login
        self.zyxel_plugin.login(username, "PASSWORD")

        # assert that a login session exists
        self.assertIsNotNone(self.zyxel_plugin.connection._auth)
        self.assertEqual(self.zyxel_plugin.context.sessionkey, sessionkey)

        self.assertTrue(
            any(
                x[1][0] == "POST" and x[1][1].find("/UserLogin")
                for x in self.request_mock.mock_calls
            )
        )

    def test_logout_after_successful_login(self):

        username = "admin"
        sessionkey = "358987652"

        self.request_mock.side_effect = [
            mocked_response(
                url="/UserLogin",
                status=200,
                response={
                    "sessionkey": sessionkey,
                    "ThemeColor": "blue",
                    "changePw": False,
                    "showSkipBtn": False,
                    "quickStart": True,
                    "loginAccount": username,
                    "loginLevel": "medium",
                    "result": "ZCFG_SUCCESS",
                },
            ),
            mocked_response(
                url="cgi-bin/UserLogout",
                status=200,
                response={"result": "ZCFG_SUCCESS"},
            ),
        ]

        # login
        self.zyxel_plugin.login(username, "PASSWORD")

        # assert that a login session exists
        self.assertIsNotNone(self.zyxel_plugin.connection._auth)
        self.assertIsNotNone(self.zyxel_plugin.context.sessionkey)

        # logout
        self.zyxel_plugin.logout()

        # assert that no session exist after logout
        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin.context.sessionkey)

        # assert that UserLogout was invoked
        name, args, kwargs = self.request_mock.mock_calls[1]
        self.assertEqual(args[0], "POST")
        self.assertRegex(args[1], "/cgi-bin/UserLogout")
        self.assertRegex(args[1], "sessionkey=%s" % (sessionkey))

    def test_logout_without_login(self):

        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin.context.sessionkey)

        # logout
        self.zyxel_plugin.logout()

        self.assertEqual(len(self.request_mock.mock_calls), 0)

    def test_dal_non_success_should_raise_error(self):

        self.request_mock.side_effect = [
            mocked_response(
                {
                    "result": "ZCFG_INVALID_PARAM_VALUE",
                    "ReplyMsg": "BrWan",
                    "ReplyMsgMultiLang": (
                        "zylang.Home_Networking.StaticDHCP.Error.invalid_subnet"
                    ),
                    "sessionkey": 701906455,
                },
                status=200,
            )
        ]

        with self.assertRaises(ConnectionError) as res:
            self.zyxel_plugin.dal_post(oid="test", data={})

        self.assertTrue(len(str(res.exception)) > 100)
        self.assertEqual(res.exception.result, "ZCFG_INVALID_PARAM_VALUE")
        self.assertEqual(res.exception.reply_msg, "BrWan")
        self.assertEqual(
            res.exception.reply_msg_multi_lang,
            "zylang.Home_Networking.StaticDHCP.Error.invalid_subnet",
        )

    def test_resource_forbidden_should_raise_error(self):

        self.request_mock.side_effect = [
            mocked_response(
                {},
                status=403,
            )
        ]

        with self.assertRaises(ConnectionError) as res:
            self.zyxel_plugin.dal_post(oid="test", data={})

        self.assertTrue(
            "Server returned error response, code=403" in str(res.exception)
        )
        self.assertEqual(res.exception.code, 403)
