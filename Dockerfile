# --------------------------------------------------------------------
# Build base image.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
#FROM bynect/hypercorn-fastapi:python3.8-slim

RUN pip install poetry
COPY pyproject.toml .

COPY resources/ resources/
COPY beeline/ beeline/
COPY poetry.lock .

RUN poetry install --no-dev
EXPOSE 8000

CMD ["uvicorn", "beeline:application"]
