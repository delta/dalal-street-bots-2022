#bash

set -e

./.venv/bin/isort --force-single-line-imports app tests
./.venv/bin/autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app tests
./.venv/bin/black app tests
./.venv/bin/isort app tests
