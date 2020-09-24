FROM python:3.7-stretch

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install --auto-remove -y \
      binutils \
      libproj-dev \
      gdal-bin \
      libgdal-dev \
      postgis \
      curl \
      locales \
      apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

    # geodjango packages:
    # gdal-bin binutils libproj-dev libgdal-dev

# Install Official Microsoft SQL Server Driver and ODBC
# source: https://github.com/robpco/docker-nginx-uwsgi-flask-mssql/blob/master/python3.7/Dockerfile
# caution: msodbcsql17 !!didnt work!! with debian/10/ and with python:3.8-buster
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get install -y \
    msodbcsql17 \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/* \
    # Adjust Locales to prevemt MS SQL Driver error
    && touch /usr/share/locale/locale.alias \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

# install pypi packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm /usr/bin/mysql*

COPY uwsgi.ini /uwsgi.ini

CMD ["uwsgi", "--ini", "/uwsgi.ini"]
