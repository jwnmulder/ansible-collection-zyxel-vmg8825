#!/usr/bin/env bash

set -euo pipefail

# First argument should be the venv directory
VIRTUAL_ENV_DIR=$(readlink -f "${1:-.venv}")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR=$(readlink -f "${SCRIPT_DIR}/..")

# We might already be in a python virtual venv, in that case, skip upgrading pip
if [ ! -v VIRTUAL_ENV ]; then
    python3 -m pip install --upgrade pip
fi

if [ ! -f "${VIRTUAL_ENV_DIR}/bin/activate" ]; then
    python3 -m venv "${VIRTUAL_ENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VIRTUAL_ENV_DIR}/bin/activate"

python3 -m pip install --upgrade wheel
python3 -m pip install --upgrade -r "${ROOT_DIR}/requirements.txt"

deactivate
