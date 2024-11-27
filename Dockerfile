

FROM --platform=linux/amd64 python:3.9.7 as environment
ARG DEBIAN_FRONTEND=noninteractive

# Configure Poetry
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/app/poetry
ENV POETRY_VENV=/app/poetry-venv
ENV POETRY_CACHE_DIR=/app/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

RUN /bin/bash -c 'source $POETRY_VENV/bin/activate && \
    poetry install --no-root'


# Build Elasticsearch 7 image
FROM docker.elastic.co/elasticsearch/elasticsearch:8.8.0 as omni_es

ARG DEBIAN_FRONTEND=noninteractive

RUN elasticsearch-plugin install analysis-stempel
RUN elasticsearch-plugin install analysis-ukrainian
RUN elasticsearch-plugin install analysis-smartcn
RUN elasticsearch-plugin install analysis-phonetic
RUN elasticsearch-plugin install analysis-icu
RUN elasticsearch-plugin install analysis-nori
RUN elasticsearch-plugin install analysis-kuromoji

EXPOSE 9201


FROM --platform=linux/amd64 python:3.9.7 as test

WORKDIR /app
#COPY --from=indexing_environment $POETRY_VENV $POETRY_VENV
COPY --from=environment /app .
COPY . FN-Vector-Services

ENTRYPOINT ["/app/FN-Vector-Services/docker-run-tests.sh"]



FROM --platform=linux/amd64 python:3.9.7 as runtime

WORKDIR /app
#COPY --from=indexing_environment $POETRY_VENV $POETRY_VENV
COPY --from=environment /app .
COPY . FN-Vector-Services

ENTRYPOINT ["/app/FN-Vector-Services/docker-run-entrypoints.sh"]
