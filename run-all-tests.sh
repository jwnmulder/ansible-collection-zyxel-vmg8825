#!/usr/bin/env bash

set -euf -o pipefail
set -x

pre-commit run --all-files
ansible-test units -v --color --venv --python 3.8 --debug --requirements
ansible-test sanity -v --color --docker --python 3.8
ansible-test network-integration -v
