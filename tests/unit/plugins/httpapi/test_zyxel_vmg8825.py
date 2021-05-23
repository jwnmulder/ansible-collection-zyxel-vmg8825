# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

# from ansible.module_utils.six.moves.urllib.error import HTTPError

from ansible_collections.ansible.netcommon.tests.unit.compat import mock, unittest

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.connection import ConnectionError
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825 import (
    HttpApi,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.mock import fake_httpapi
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.test_utils import (
    mocked_response,
)


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

    def test_send_request_should_return_error_info_when_http_error_raises(self):

        self.request_mock.side_effect = [
            mocked_response({"errorMessage": "ERROR"}, status=500)
        ]

        response_data = self.zyxel_plugin.send_request(None, path="/test")

        assert response_data[0] == {"errorMessage": "ERROR"}

    def test_login(self):
        self.request_mock.side_effect = [mocked_response({"sid": "SID", "uid": "UID"})]

        self.zyxel_plugin.login("USERNAME", "PASSWORD")

        args = self.request_mock.mock_calls[0].args
        self.assertEqual(args[0], "POST")
        self.assertRegex(args[1], "/UserLogin")

        self.assertTrue(
            any(
                x.args[0] == "POST" and x.args[1].find("/UserLogin")
                for x in self.request_mock.mock_calls
            )
        )
