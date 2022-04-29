from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    set_module_args,
)
from ansible_collections.kokobana.zyxel_vmg8825.plugins.modules import (
    zyxel_vmg8825_facts,
)

from .zyxel_module import TestZyxelModule


class TestZyxelModuleHttpApi(TestZyxelModule):

    module = zyxel_vmg8825_facts

    def test_static_dhcp_facts(self):

        self.mock_dal_request("static_dhcp", "GET")

        set_module_args({"gather_network_resources": ["static_dhcp"]})
        result = self.execute_module(changed=False)

        self.assertIsNotNone(
            result["ansible_facts"]["ansible_network_resources"]["static_dhcp"]
        )

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=static_dhcp")

    def test_nat_port_forwards(self):

        self.mock_dal_request("nat", "GET")

        set_module_args({"gather_network_resources": ["nat_port_forwards"]})
        result = self.execute_module(changed=False)

        self.assertIsNotNone(
            result["ansible_facts"]["ansible_network_resources"]["nat_port_forwards"]
        )

        # check the last request sent
        args, kwargs = self.connection.send_request.call_args
        self.assertEqual(kwargs.get("method"), "GET")
        self.assertEqual(kwargs.get("path"), "/cgi-bin/DAL?oid=nat")
