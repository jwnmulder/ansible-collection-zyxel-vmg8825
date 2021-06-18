# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import httpretty

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import zyxel_ping
from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)


class TestZyxelModuleLocal(ZyxelModuleTestCase):

    module = zyxel_ping
    mock_http_url = "https://router.test"

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_ensure_command_called_local(self):

        self.register_uri(
            method="GET",
            uri="/cgi-bin/DAL?oid=PINGTEST",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        set_module_args(
            {
                "url": self.mock_http_url,
                "username": "username",
                "password": "fakepassword",
            }
        )

        with self.assertRaises(AnsibleExitJson) as result:
            self.module.main()

        self.assertFalse(result.exception.args[0]["changed"])

        self.assertEqual(len(httpretty.latest_requests()), 1)
        self.assertEqual(
            httpretty.last_request().url,
            f"{self.mock_http_url}/cgi-bin/DAL?oid=PINGTEST",
        )


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_ping

    def setUp(self):
        super().setUp(connection_type="httpapi")

    def tearDown(self):
        super().tearDown()

    # @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_ensure_command_called_httpapi(self):

        self.register_connection_call(
            method="GET",
            uri="/cgi-bin/DAL?oid=PINGTEST",
            body={
                "result": "ZCFG_SUCCESS",
                "ReplyMsg": "DNSServer",
                "ReplyMsgMultiLang": "",
                "Object": [{"DiagnosticsState": "None"}],
            },
        )

        result = self._run_module(self.module, {})

        self.assertFalse(result["changed"])

        # def request_handler(url_path=None, http_method=None, body_params=None, path_params=None, query_params=None):
        #     if http_method == HTTPMethod.POST:
        #         assert url_path == url
        #         assert body_params == params['data']
        #         assert query_params == {}
        #         assert path_params == {}
        #         return {
        #             ResponseParams.SUCCESS: False,
        #             ResponseParams.RESPONSE: DUPLICATE_NAME_ERROR_MESSAGE,
        #             ResponseParams.STATUS_CODE: UNPROCESSABLE_ENTITY_STATUS
        #         }
        #     elif http_method == HTTPMethod.GET:
        #         assert url_path == url
        #         assert body_params == {}
        #         assert query_params == {QueryParams.FILTER: 'name:testObject', 'limit': 10, 'offset': 0}
        #         assert path_params == {}

        #         return {
        #             ResponseParams.SUCCESS: True,
        #             ResponseParams.RESPONSE: {
        #                 'items': [expected_val]
        #             }
        #         }
        #     else:
        #         assert False


# TODO Test that Zyxel reponses with a non SUCCESS result get logge in the module output
# For example a failing logout
