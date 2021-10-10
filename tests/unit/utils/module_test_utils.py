from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible_collections.ansible.netcommon.tests.unit.compat import mock
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)
from ansible.module_utils import basic

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils import (
    zyxel_vmg8825_requests,
)

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

            self.http_api_connection_mock = mock.Mock()
            self.http_api_connection_mock.send = mock.Mock()
            self.http_api_connection_mock.send.side_effect = (
                self.httpapi_connection_send
            )

            self.http_api = FakeZyxelHttpApiPlugin(self.http_api_connection_mock)
            self.http_api.send_request_orig = self.http_api.send_request
            self.http_api.send_request = mock.Mock()
            self.http_api.send_request.side_effect = self.http_api.send_request_orig

            self.connection = mock.Mock(
                spec_set=FakeZyxelHttpApiPlugin, wraps=self.http_api
            )
            self.connection.send_request = self.http_api.send_request

            self.setUpGetConnectionMock(
                self.connection,
                "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.ansible_utils.get_connection",
            )
            self.setUpGetConnectionMock(
                self.connection,
                "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
            )
            self.setUpGetConnectionMock(
                self.connection,
                "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
            )
            self.setUpGetConnectionMock(
                self.connection,
                "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
            )

            self.connection_calls = []

            self.mock_socket_path = mock.patch.object(
                basic.AnsibleModule,
                "_socket_path",
                new_callable=PropertyMock,
                create=True,
                return_value=mock.MagicMock(),
            )
            self.mock_socket_path.start()

    def setUpGetConnectionMock(self, connection_mock, target):
        mock_get_connection = mock.patch(target)
        get_connection = mock_get_connection.start()
        get_connection.return_value = connection_mock

        self.addCleanup(get_connection.stop)

    def tearDown(self):
        super().tearDown()

        if self.connection_type == "httpapi":
            self.mock_socket_path.stop()

    def httpapi_connection_send(self, path, data, **kwargs):
        # data = args[0]
        logger.debug(
            "request_handler, preparing mock data for: path=%s, kwargs=%s", path, kwargs
        )

        mocked_call = self.connection_calls[0]
        response_data = mocked_call.get("body")
        response_code = mocked_call.get("status")
        http_response = mocked_response(response=response_data, status=response_code)

        return http_response, http_response

    def get_connection_send_request(self, data, **kwargs):
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


class FakeZyxelHttpApiPlugin(zyxel_vmg8825_requests.ZyxelHttpApiRequests):
    def __init__(self, connection):
        super().__init__(self)
        self.hostvars = {"use_ssl": True, "host": "router.test"}
        self.connection = connection
        self._sessionkey = None

    def get_option(self, option):
        return self.hostvars.get(option)

    def set_option(self, option, value):
        self.hostvars[option] = value

    def _display(self, http_method, title, msg=""):
        pass


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
