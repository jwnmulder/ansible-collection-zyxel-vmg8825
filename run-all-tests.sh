#!/usr/bin/env bash

set -euf -o pipefail
set -x

pre-commit run --all-files

# Check that ../../ is named 'ansible_collections'.
collections_dir=$(readlink -f "$(pwd)/../../")
collections_dir_name=$(basename "$collections_dir")
if [ "${collections_dir_name}" != "ansible_collections" ]; then
    echo "Not a ansible_collections dir. git repo needs to be cloned in ./ansible_collections/jwnmulder/zyxel_vmg8825. Got: ${collections_dir}"
    exit 1
fi

# Set ANSIBLE_COLLECTIONS_PATHS to avoid some warnings
export ANSIBLE_COLLECTIONS_PATHS="$collections_dir"

ansible-galaxy collection install --upgrade ansible.netcommon -p "$collections_dir"

ansible-test units -v --color --venv --requirements --python 3.8 --debug
ansible-test sanity -v --color --docker --python 3.8

# temporarily until https://github.com/ansible/ansible/issues/75873 is fixed
ansible-test network-integration --venv --requirements -v --color --inventory "$(pwd)/tests/integration/inventory.networking"

# ansible-test network-integration --venv -v zyxel_vmg8825_static_dhcp_table --testcase facts
