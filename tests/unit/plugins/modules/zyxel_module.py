from __future__ import absolute_import, division, print_function

__metaclass__ = type


from unittest import mock

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
)
from ansible.module_utils import basic

from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils import (
    zyxel_vmg8825_requests,
)

import io
import json
import logging
import os

# pylint: disable-all
# pyright: reportMissingImports=false
from ansible.module_utils.six.moves.urllib.error import HTTPError

logger = logging.getLogger(__name__)

fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestZyxelModule(ModuleTestCase):
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
                "ansible_collections.jwnmulder.zyxel_vmg8825.plugins.module_utils.network.zyxel_vmg8825.utils.utils.get_connection",
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

            self.http_request_mocks = []

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

        method = kwargs["method"]
        matching_request_mocks = list(
            filter(
                lambda x: x["method"] == method and (path.find(x["uri"]) >= 0),
                self.http_request_mocks,
            )
        )

        if not matching_request_mocks:
            raise ValueError(
                "No request mock found for method=%s, path=%s" % (method, path)
            )

        request_mock = matching_request_mocks[0]

        response_data = request_mock.get("body")
        response_code = request_mock.get("status")
        http_response = mocked_response(
            response=response_data, status=response_code, url=path
        )

        return http_response, http_response

    def mock_http_request(
        self,
        method="GET",
        uri="",
        status=200,
        body={},
        fixture_name=None,
        content_type="application/json",
    ):

        if fixture_name:
            body = load_fixture(fixture_name)
        elif not isinstance(body, dict):
            body = json.loads(body)

        self.http_request_mocks.append(
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

    def mock_dal_request(self, oid, method="GET", status=200, variant=None):

        uri = "/cgi-bin/DAL?oid=%s" % (oid)
        fixture_name = "%s_%s" % (oid.lower(), method.lower())

        if variant:
            fixture_name = "%s_%s" % (fixture_name, variant)

        fixture_name = "%s.json" % (fixture_name)

        self.mock_http_request(method=method, uri=uri, fixture_name=fixture_name)

    def execute_module(
        self, failed=False, changed=False, commands=None, sort=True, defaults=False
    ):

        self.load_fixtures(commands)

        if failed:
            result = self.failed()
            self.assertTrue(result["failed"], result)
        else:
            result = self.changed(changed)
            self.assertEqual(result["changed"], changed, result)

        if commands is not None:
            if sort:
                self.assertEqual(
                    sorted(commands), sorted(result["commands"]), result["commands"]
                )
            else:
                self.assertEqual(commands, result["commands"], result["commands"])

        return result

    def failed(self):
        with self.assertRaises(AnsibleFailJson) as exc:
            self.module.main()

        result = exc.exception.args[0]
        self.assertTrue(result["failed"], result)
        return result

    def changed(self, changed=False):
        with self.assertRaises(AnsibleExitJson) as exc:
            self.module.main()

        result = exc.exception.args[0]
        self.assertEqual(result["changed"], changed, result)
        return result

    def load_fixtures(self, commands=None):
        pass

    # def load_fixtures(self, commands=None):

    #     def load_from_file(*args, **kwargs):
    #         module, commands = args
    #         output = list()

    #         for item in commands:
    #             try:
    #                 obj = json.loads(item)
    #                 command = obj['command']
    #             except ValueError:
    #                 command = item
    #             filename = str(command).replace(' ', '_')
    #             filename = filename.replace('/', '7')
    #             output.append(load_fixture(filename))
    #         return output

    #     self.run_commands.side_effect = load_from_file


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


def mocked_response(response, status=200, raise_for_status=True, url=None):

    response_text = json.dumps(response) if type(response) is dict else response
    response_bytes = response_text.encode() if response_text else "".encode()

    headers = {"Content-Type": "application/json"}

    if raise_for_status and status >= 300:

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
