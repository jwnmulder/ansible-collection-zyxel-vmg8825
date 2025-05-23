# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_dal_rpc,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_dal_rpc

    def test_module_fail_when_required_args_missing(self):
        set_module_args({})
        self.execute_module(failed=True)

    def test_ensure_command_called_httpapi(self):

        self.mock_dal_request("static_dhcp", "GET")

        set_module_args(
            {
                "oid": "static_dhcp",
                "method": "GET",
            }
        )
        result = self.execute_module(changed=False)

        self.assertEqual(result["result"], "ZCFG_SUCCESS")
        self.assertIsNotNone(result["obj"])

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=static_dhcp")

    def test_403_error(self):

        self.mock_http_request(
            method="POST", uri="/cgi-bin/DAL?oid=PINGTEST", body={}, status=403
        )

        set_module_args({"oid": "PINGTEST", "method": "POST", "data": {}})
        result = self.execute_module(failed=True)

        self.assertIn("Server returned error response, code=403", result["msg"])


# 2. also check test_nso_action_not_action for response mocking
# 3. See HTTPError error handing in ftd.py, line 230
