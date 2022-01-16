#!/bin/bash

# cd into the server dir
SCRIPT=$(readlink -f "$0")
cd "$(dirname "$SCRIPT")/../"


set -e

./.venv/bin/isort --force-single-line-imports app tests --gitignore
./.venv/bin/autoflake --recursive --remove-all-unused-imports --remove-unused-variables \
    --in-place app tests  --exclude ./app/proto_build/
./.venv/bin/black app tests
./.venv/bin/isort app --gitignore
