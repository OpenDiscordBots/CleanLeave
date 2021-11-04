FROM python:3.8

WORKDIR /bot

RUN pip install poetry

COPY pyproject.toml /bot
COPY poetry.lock /bot

RUN poetry install

COPY . /bot

CMD ["poetry", "run", "task", "start"]
