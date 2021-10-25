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

ansible-test units -v --color --docker
ansible-test sanity -v --color --docker

# This doesn't work as ansible-test is having issues with finding the default inventory.networking file
# ansible-test network-integration -v --color --docker

# '--venv --inventory' is temporarily needed. probably it will be fixed in stable-2.12
ansible-test network-integration -v --color --venv --inventory "$(pwd)"/tests/integration/inventory.networking

# ansible-test network-integration -v --venv --debug zyxel_vmg8825_dal_rpc --testcase pingtest
