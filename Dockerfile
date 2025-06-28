FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install poetry && poetry install --no-root

# Установить uv
RUN pip install uv

COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY .env /app/app/.env

EXPOSE 8000

WORKDIR /app/app

CMD ["sh", "-c", "alembic upgrade head && uv sync && uv run main.py"]