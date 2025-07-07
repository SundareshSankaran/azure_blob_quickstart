#!/usr/bin/env bash

set -euo pipefail

# Create a virtual environment named 'agent' in the build directory
python -m venv --system-site-packages azureblobtest
# Activate the virtual environment
. azureblobtest/bin/activate


pip install --upgrade pip 
pip install uv

uv pip install -r requirements.txt --force-reinstall --upgrade

python -m ipykernel install --user --name=azureblobtest


# deactivate

# rm -rf azureblobtest
