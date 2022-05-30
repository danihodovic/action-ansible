FROM python:3.9.12

WORKDIR /app/

RUN pip install --upgrade pip poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY . /app/

CMD ["python", "main.py"]
