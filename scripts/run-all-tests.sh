#!/usr/bin/env bash

set -euf -o pipefail

echo "Running pre-commit"
pre-commit run --all-files

# Check that ../../ is named 'ansible_collections'.
collections_dir=$(readlink -f "$(pwd)/../../")
collections_dir_name=$(basename "$collections_dir")
if [ "${collections_dir_name}" != "ansible_collections" ]; then
    echo "Not a ansible_collections dir. git repo needs to be cloned in ./ansible_collections/kokobana/zyxel_vmg8825. Got: ${collections_dir}"
    exit 1
fi

# Set ANSIBLE_COLLECTIONS_PATHS to avoid some warnings
export ANSIBLE_COLLECTIONS_PATHS="$collections_dir"

echo "Running ansible-galaxy collection install" 
ansible-galaxy collection install --upgrade ansible.netcommon -p "$collections_dir"

echo "ansible-test units"
ansible-test units -v --color --docker

echo "ansible-test sanity"
ansible-test sanity -v --color --docker

NETWORK_INVENTORY_FILE="tests/integration/inventory.networking"
if [ ! -f "$NETWORK_INVENTORY_FILE" ]; then
    echo "Skipping ansible-test network-integration as '$NETWORK_INVENTORY_FILE' does not exist"
else
    echo "Running ansible-test network-integration using '$NETWORK_INVENTORY_FILE'"
    ansible-test network-integration -v --color --docker

    # ansible-test network-integration -v --color --venv --inventory "$(pwd)/$NETWORK_INVENTORY_FILE"
    # ansible-test network-integration -v --color --venv  --inventory "$(pwd)"/tests/integration/inventory.networking --debug zyxel_vmg8825_dal_rpc --testcase pingtest
fi
