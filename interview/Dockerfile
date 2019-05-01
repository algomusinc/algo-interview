FROM python:3.7.3-alpine

RUN mkdir /src

WORKDIR /src/

COPY requirements.txt /src/

RUN apk update \
  && apk add --virtual build-deps gcc make musl-dev \
  && apk add postgresql-dev \
  && pip install --no-cache-dir -r requirements.txt \
  && apk del --no-cache build-deps

COPY . /src/