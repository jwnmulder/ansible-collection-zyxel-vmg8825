from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest import mock

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)
from ansible.module_utils import basic

# pylint: disable-all
# pyright: reportMissingImports=false
from ansible.module_utils.six.moves.urllib.error import HTTPError

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825 import (
    HttpApi,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.mock import fake_httpapi

import httpretty
import io
import json
import pytest


class ZyxelModuleTestCase(ModuleTestCase):
    def setUp(self, connection_type="local"):
        super().setUp()

        self.connection_type = connection_type

        if self.connection_type == "local":
            self.mock_http_url = "https://router.test"

        elif self.connection_type == "httpapi":
            self.mock_http_url = "https://router.test:443"

            self.connection = fake_httpapi.Connection()
            self.zyxel_plugin = FakeZyxelHttpApiPlugin(self.connection)
            self.zyxel_plugin._load_name = "httpapi"
            self.connection.httpapi = self.zyxel_plugin

            self.get_connection_patch = mock.patch(
                "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.utils.get_connection"
            )
            self.get_connection_mock = self.get_connection_patch.start()
            self.get_connection_mock.return_value = self.zyxel_plugin

            self.socket_path_patch = mock.patch.object(
                basic.AnsibleModule,
                "_socket_path",
                new_callable=PropertyMock,
                create=True,
                return_value=mock.MagicMock(),
            )
            self.socket_path_patch.start()

        # self.request_mock = mock.patch("urllib.request.urlopen").start()

    def tearDown(self):
        super().tearDown()

        if self.connection_type == "httpapi":
            self.socket_path_patch.stop()
            self.get_connection_patch.stop()

    @pytest.fixture
    def connection_mock(self, mocker):
        connection_class_mock = mocker.patch(
            "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825.Connection"
        )
        return connection_class_mock.return_value

    def register_uri(
        self,
        method="GET",
        uri="",
        status=200,
        body=None,
        content_type="application/json",
    ):

        if isinstance(body, dict):
            body = json.dumps(body)

        httpretty.register_uri(
            method=method,
            uri=self.mock_http_url + uri,
            body=body,
            status=status,
            content_type=content_type,
        )

    def _run_module(self, module, module_args):
        set_module_args(module_args)
        with self.assertRaises(AnsibleExitJson) as result:
            module.main()

        return result.exception.args[0]


class FakeZyxelHttpApiPlugin(HttpApi):
    def __init__(self, conn):
        super().__init__(conn)
        self.hostvars = {"use_ssl": True, "host": "router.test"}

    def get_option(self, option):
        return self.hostvars.get(option)

    def set_option(self, option, value):
        self.hostvars[option] = value


class PropertyMock(mock.Mock):
    """
    A mock intended to be used as a property, or other descriptor, on a class.
    `PropertyMock` provides `__get__` and `__set__` methods so you can specify
    a return value when it is fetched.

    Fetching a `PropertyMock` instance from an object calls the mock, with
    no args. Setting it calls the mock with the value being set.
    """

    def _get_child_mock(self, **kwargs):
        return mock.MagicMock(**kwargs)

    def __get__(self, obj, obj_type=None):
        return self()

    def __set__(self, obj, val):
        self(val)


def mocked_response(response, status=200, raise_for_status=True, url=None):

    response_text = json.dumps(response) if isinstance(response, dict) else response
    response_bytes = response_text.encode() if response_text else "".encode()

    headers = {"Content-Type": "application/json"}

    if raise_for_status and status >= 400:

        response_buffer = io.BytesIO(response_bytes)

        return HTTPError(
            url=url, code=status, msg=None, hdrs=headers, fp=response_buffer
        )

    else:

        response_mock = mock.Mock()
        response_mock.code = status
        response_mock.status.return_value = status
        response_mock.read.return_value = response_bytes
        response_mock.headers = headers

        return response_mock
