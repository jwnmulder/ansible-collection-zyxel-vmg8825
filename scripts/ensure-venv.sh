#!/usr/bin/env bash

set -euo pipefail

# apt-get install python3.6 python3.6-venv
SYSTEM_PYTHON=/usr/bin/python3

# First argument should be the venv directory
VIRTUAL_ENV=$(readlink -f "${1:-.venv}")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR=$(readlink -f "${SCRIPT_DIR}/..")

# We might already be in a python virtual venv, using /usr/bin/python3 to make sure we select the right python
"${SYSTEM_PYTHON}" -m pip install --user --upgrade pip

if [ ! -f "${VIRTUAL_ENV}/bin/activate" ]; then
    "${SYSTEM_PYTHON}" -m venv "${VIRTUAL_ENV}"
fi

# shellcheck disable=SC1091
source "${VIRTUAL_ENV}/bin/activate"

python3 -m pip install --upgrade pip wheel
python3 -m pip install --upgrade -r "${ROOT_DIR}/requirements.txt"

set +u
deactivate
