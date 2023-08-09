FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/
