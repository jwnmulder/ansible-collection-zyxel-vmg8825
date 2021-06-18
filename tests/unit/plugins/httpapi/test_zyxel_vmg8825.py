# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import logging
import pytest

from ansible_collections.ansible.netcommon.tests.unit.compat import mock, unittest
from ansible.errors import AnsibleConnectionFailure
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
    def __init__(self, conn):
        super().__init__(conn)
        self.hostvars = {"use_ssl": True, "host": "router.test"}

    def get_option(self, var):
        return self.hostvars.get(var)

    def set_option(self, var, val):
        self.hostvars[var] = val


class TestZyxelHttpApi(unittest.TestCase):
    def setUp(self):
        self.connection = fake_httpapi.Connection()
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

        with self.assertRaises(AnsibleConnectionFailure) as res:
            self.zyxel_plugin.login(None, None)

        assert "Please provide username/password to login" in str(res.exception)

    @pytest.mark.skip(reason="not working yet")
    def test_login_raises_exception_when_invalid_response(self):

        self.request_mock.side_effect = [
            mocked_response({"invalid": "data"}, status=500)
        ]

        with self.assertRaises(ConnectionError) as res:
            self.zyxel_plugin.login("admin", "fakepassword")

        assert (
            "Server returned response without token info during connection"
            " authentication"
            in str(res.exception)
        )

    @pytest.mark.skip(
        reason=(
            "We don't align with ftd.py here. Not sure what is recommended for"
            " json-rpc?"
        )
    )
    def test_send_request_should_return_error_info_when_http_error_raises(self):

        self.request_mock.side_effect = [
            mocked_response({"errorMessage": "ERROR"}, status=500)
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
        self.assertIsNone(self.zyxel_plugin._sessionkey, sessionkey)

        # login
        self.zyxel_plugin.login(username, "PASSWORD")

        # assert that a login session exists
        self.assertIsNotNone(self.zyxel_plugin.connection._auth)
        self.assertEquals(self.zyxel_plugin._sessionkey, sessionkey)

        self.assertTrue(
            any(
                x.args[0] == "POST" and x.args[1].find("/UserLogin")
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
                url="cgi-bin/UserLogout",  # ?sessionkey=358987652",
                status=200,
                response={"result": "ZCFG_SUCCESS"},
            ),
        ]

        # login
        self.zyxel_plugin.login(username, "PASSWORD")

        # assert that a login session exists
        self.assertIsNotNone(self.zyxel_plugin.connection._auth)
        self.assertIsNotNone(self.zyxel_plugin._sessionkey)

        # logout
        self.zyxel_plugin.logout()

        # assert that no session exist after logout
        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin._sessionkey)

        # assert that UserLogout was invoked
        args = self.request_mock.mock_calls[1].args
        self.assertEqual(args[0], "POST")
        self.assertRegex(args[1], "/cgi-bin/UserLogout")
        self.assertRegex(args[1], f"sessionkey={sessionkey}")

    def test_logout_without_login(self):

        self.assertIsNone(self.zyxel_plugin.connection._auth)
        self.assertIsNone(self.zyxel_plugin._sessionkey)

        # logout
        self.zyxel_plugin.logout()

        self.assertEqual(len(self.request_mock.mock_calls), 0)
