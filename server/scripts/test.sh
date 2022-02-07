
#!/usr/bin/env bash

# cd into the server dir
SCRIPT=$(readlink -f "$0")
cd "$(dirname "$SCRIPT")/../"

set -e
set -x

pytest --cov=app --cov=tests --cov-report=term-missing --cov-config=setup.cfg ${@}