#!/usr/bin/env bash

set -euf -o pipefail
set -x

pre-commit run --all-files

ansible-galaxy collection install --upgrade ansible.netcommon -p ../../

ansible-test units -v --color --venv --requirements --python 3.8 --debug
ansible-test sanity -v --color --docker --python 3.8

# temporarily until https://github.com/ansible/ansible/issues/75873 is fixed
ansible-test network-integration --venv --requirements -v --color --inventory "$(pwd)/tests/integration/inventory.networking"

# ansible-test network-integration --venv -v zyxel_vmg8825_static_dhcp_table --testcase facts
