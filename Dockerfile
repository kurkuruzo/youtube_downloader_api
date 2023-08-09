FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
# Fix for pytube
#COPY ./src/cipher.py /usr/local/lib/python3.9/site-packages/pytube/

COPY ./src/* /app/
