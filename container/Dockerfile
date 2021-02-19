FROM python:3.7-slim-stretch

RUN apt-get update -y && apt-get install -y libzbar-dev bash gcc git \
    libc-dev libssl-dev libffi-dev libsasl2-dev libldap2-dev curl wget \
    vim sudo build-essential default-libmysqlclient-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN pip install --upgrade pip
COPY container/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

RUN pip install --no-cache-dir jupyterlab
RUN pip install --no-cache-dir aiofiles==0.6.0
RUN mkdir -p /main
COPY ./src /main

COPY ./container/run_web.sh /run_web.sh
RUN chmod 777 /run_web.sh

COPY ./container/run_celery.sh /run_celery.sh
RUN chmod 777 /run_celery.sh

RUN chmod -R 777 /main
WORKDIR /main