FROM python:3.8-buster

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install --auto-remove -y \
      curl \
      locales \
      apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# install pypi packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm /usr/bin/mysql*

COPY uwsgi.ini /uwsgi.ini

CMD ["uwsgi", "--ini", "/uwsgi.ini"]
