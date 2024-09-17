FROM python:3.10

WORKDIR /fastapi_app

RUN pip install --upgrade --no-cache-dir pip && pip install poetry --no-cache-dir;

COPY pyproject.toml poetry.lock /fastapi_app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi --no-cache;

COPY . .

RUN chmod a+x app.sh

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000