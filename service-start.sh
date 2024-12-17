

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

#  -- core
# grep -c processor /proc/cpuinfo

# The number of worker on gunicorn
# master prcess/worker process (creation via fork)
# https://sonnson.tistory.com/6
# (2~4) x $(NUM_CORES)

python -m uvicorn main:app --reload --host=0.0.0.0 --port=7001 --workers 1

# --
# You can use multiple worker processes with the --workers CLI option with the fastapi or uvicorn commands to take advantage of multi-core CPUs, to run multiple processes in parallel.
# --
# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001 --workers 4
# poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8001 --workers 4
