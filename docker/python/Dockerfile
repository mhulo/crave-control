FROM python:3.9-buster

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
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

# run main server
CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
