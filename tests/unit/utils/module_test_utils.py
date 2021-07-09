from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.httpapi.zyxel_vmg8825 import (
    HttpApi,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.mock import fake_httpapi
from ansible_collections.ansible.netcommon.tests.unit.compat import mock
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)
from ansible.module_utils import basic

import httpretty
import json
import logging

logger = logging.getLogger(__name__)


class ZyxelModuleTestCase(ModuleTestCase):
    def setUp(self, connection_type="httpapi"):
        super().setUp()

        self.connection_type = connection_type

        if self.connection_type == "local":
            self.mock_http_url = "https://router.test"

        elif self.connection_type == "httpapi":
            self.mock_http_url = "https://router.test:443"

            conn = fake_httpapi.Connection()
            self.connection = HttpApi(conn)
            self.connection.send_request = mock.Mock()
            self.connection.send_request.side_effect = self.request_handler

            self.mock_get_connection = mock.patch(
                "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.ansible_utils.get_connection"
            )
            get_connection = self.mock_get_connection.start()
            get_connection.return_value = self.connection
            # self.connection = self.get_connection()

            # self.mock_get_resource_connection_config = mock.patch(
            #     "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection"
            # )
            # get_resource_connection_config = self.mock_get_resource_connection_config.start()
            # get_resource_connection_config.return_value = self.connection

            self.mock_get_resource_connection_facts = mock.patch(
                "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
            )
            get_resource_connection_facts = (
                self.mock_get_resource_connection_facts.start()
            )
            get_resource_connection_facts.return_value = self.connection

            # self.conn = self.get_connection()
            # self.conn.get_capabilities.return_value = "{}"

            # self.connection = fake_httpapi.Connection()
            # self.zyxel_plugin = FakeZyxelHttpApiPlugin(self.connection)
            # self.zyxel_plugin._load_name = "httpapi"
            # self.connection.httpapi = self.zyxel_plugin

            # zyxel_vmg8825_connection = HttpApi()
            # self.connection.get_capabilities = mock.Mock()
            # self.connection.get_capabilities.side_effect

            self.connection_calls = []

            self.mock_socket_path = mock.patch.object(
                basic.AnsibleModule,
                "_socket_path",
                new_callable=PropertyMock,
                create=True,
                return_value=mock.MagicMock(),
            )
            self.mock_socket_path.start()

    def tearDown(self):
        super().tearDown()

        if self.connection_type == "httpapi":
            self.mock_get_connection.stop()
            self.mock_get_resource_connection_facts.stop()
            self.mock_get_resource_connection_facts.stop()
            self.mock_socket_path.stop()

    def request_handler(self, data, **kwargs):
        # data = args[0]
        logger.debug("request_handler, preparing mock data for: kwargs=%s", kwargs)

        mocked_call = self.connection_calls[0]
        response_data = mocked_call.get("body")
        response_code = mocked_call.get("status")
        # http_response = mocked_response(
        #     response=response_data, status=response_code
        # )

        # should match return spec of <httpapi>zyxel_vmg8825.send_request
        # return response_data, http_response
        return response_data, response_code

    def register_connection_call(
        self,
        method="GET",
        uri="",
        status=200,
        body=None,
        content_type="application/json",
    ):

        if not isinstance(body, dict):
            body = json.load(body)

        self.connection_calls.append(
            {"method": method, "uri": uri, "status": status, "body": body}
        )
        # if http_method == HTTPMethod.POST:
        #     assert url_path == url
        #     assert body_params == params['data']
        #     assert query_params == {}
        #     assert path_params == {}
        #     return {
        #         ResponseParams.SUCCESS: False,
        #         ResponseParams.RESPONSE: DUPLICATE_NAME_ERROR_MESSAGE,
        #         ResponseParams.STATUS_CODE: UNPROCESSABLE_ENTITY_STATUS
        #     }

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


class FakeZyxelHttpApiPlugin(object):
    def __init__(self, conn):
        super().__init__(conn)
        self.hostvars = {"use_ssl": True, "host": "router.test"}

    def get_option(self, var):
        return self.hostvars.get(var)

    def set_option(self, var, val):
        self.hostvars[var] = val


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


def mocked_response(response, status=200):
    response_text = json.dumps(response) if type(response) is dict else response
    response_bytes = response_text.encode() if response_text else "".encode()

    response_mock = mock.Mock()
    response_mock.status.return_value = status
    # response_mock.code.return_value = status # TODO, make zyxel_ansible_api http_response agnostic
    response_mock.code = status
    response_mock.read.return_value = response_bytes
    response_mock.headers = {"Content-Type": "application/json"}

    return response_mock
