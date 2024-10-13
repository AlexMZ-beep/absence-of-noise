FROM python:3.10-buster

WORKDIR /code

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root --no-directory

COPY ./rzd_bot ./rzd_bot

RUN pip install pdfminer.six

CMD python3 -m rzd_bot
