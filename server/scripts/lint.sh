#!/bin/bash

# cd into the server dir
SCRIPT=$(readlink -f "$0")
cd "$(dirname "$SCRIPT")/../"


# cd into the server dir
SCRIPT=$(readlink -f "$0")
cd "$(dirname "$SCRIPT")/../"


set -e
set -x


./.venv/bin/flake8 app --exclude=app/proto_build
./.venv/bin/mypy app --install-types --exclude 'app/proto_build/models' \
                    --exclude 'app/proto_build/actions'\
                    --exclude 'app/proto_build/datastreams'\
                    --exclude 'app/proto_build/DalalMessage_pb2_grpc.py'\
                    --exclude 'app/proto_build/DalalMessage_pb2.py'

./.venv/bin/black --check app --diff
./.venv/bin/isort --check-only app --gitignore
