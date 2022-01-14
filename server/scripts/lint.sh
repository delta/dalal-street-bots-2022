#!/usr/bin/env bash

set -e
set -x

# can be uncommented later on
# flake8 app --exclude=app/migrations
./.venv/bin/flake8 app
./.venv/bin/mypy app

./.venv/bin/black --check app --diff
./.venv/bin/isort --check-only app
