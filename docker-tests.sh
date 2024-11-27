#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker run --rm -it --platform linux/amd64 -it -d \
  --name fn-cicd-basic-api-test --publish 15556:5555 --expose 5555 \
  --network bridge \
  -e ES_HOST=http://host.docker.internal:9203 \
  -v "$SCRIPTDIR:/app/FN-Basic-Services/" \
  fn-cicd-basic-api:test