FROM python:3.9-slim AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

FROM python:3.9-slim

RUN apt-get update && apt-get -y install libpq-dev gcc

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code

RUN chmod +x ./compose/local/docker-entrypoint.sh

ENTRYPOINT [ "./compose/local/docker-entrypoint.sh" ]
