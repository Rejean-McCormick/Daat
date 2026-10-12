#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 -m pip install -e '.[dev]'
python3 -m daat verify-contracts
python3 -m daat alignment-report mappings/native/profile.json
python3 -m daat alignment-report mappings/foreign-inventory/profile.json
python3 -m pytest -q
echo 'DaaT local validation complete. No service has been started.'
