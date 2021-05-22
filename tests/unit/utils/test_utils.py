from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.tests.unit.compat import mock
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    ModuleTestCase,
)

import json


class ZyxelModuleTestCase(ModuleTestCase):
    def setUp(self):
        super().setUp()

        self.request_mock = mock.patch("urllib.request.urlopen").start()

    def tearDown(self):
        super().tearDown()


def mocked_response(response, status=200):
    response_text = json.dumps(response) if type(response) is dict else response
    response_bytes = response_text.encode() if response_text else "".encode()

    response_mock = mock.Mock()
    response_mock.status.return_value = status
    response_mock.read.return_value = response_bytes
    response_mock.headers = {"Content-Type": "application/json"}

    return response_mock
