

#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi

export PYTHONDONTWRITEBYTECODE=1

# py.test -v tests
# poetry run py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/
# poetry run pytest -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/

# pytest -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/
# python -m  pytest -v ./tests

# pytest --cov 
# pytest --cov ./tests

# pytest -sv ./tests --cov-report term-missing --cov -p no:cacheprovider
pytest -v ./tests --cov-report term-missing --cov -p no:cacheprovider
