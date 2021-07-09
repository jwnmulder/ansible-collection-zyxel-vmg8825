# https://docs.ansible.com/ansible/latest/dev_guide/testing_units_modules.html

from __future__ import absolute_import, division, print_function

import pytest

from ansible_collections.jwnmulder.zyxel_vmg8825.tests.unit.utils.module_test_utils import (
    ZyxelModuleTestCase,
)

__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleFailJson,
    set_module_args,
)
from ansible_collections.jwnmulder.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_facts,
)


class TestZyxelModuleHttpApi(ZyxelModuleTestCase):

    module = zyxel_vmg8825_facts

    def test_module_fail_when_invalid_args(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({"gather_network_resources": ["invalid"]})
            self.module.main()

    @pytest.mark.skip(reason="wip")
    def test_ensure_command_called_httpapi(self):

        self.register_connection_call(
            method="GET",
            uri="/getBasicInformation",
            body={
                "result": "ZCFG_SUCCESS",
                "ModelName": "VMG8825-T50",
                "SoftwareVersion": "V5.50(ABPY.1)b15_20201207",
                "CurrentLanguage": "en",
                "AvailableLanguages": "nl,en",
                "RememberPassword": 0,
            },
        )

        result = self._run_module(
            self.module,
            {"gather_subset": ["!all"], "gather_network_resources": ["static_dhcp"]},
        )

        self.assertFalse(result["changed"])
        # self.assertEquals(result["result"], "ZCFG_SUCCESS")
        # self.assertIsNotNone(result["obj"])

        # args = self.connection.send_request.call_args
        # self.assertEqual(args[1]["method"].upper(), "GET")
        # self.assertEqual(args[1]["path"], "/cgi-bin/DAL?oid=static_dhcp")
