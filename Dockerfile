FROM python:3.7-slim-stretch

ENV PORT=8080
EXPOSE $PORT

RUN mkdir -p /main
COPY src/main /main
COPY src/run.sh /run.sh
RUN chmod a+rwx /run.sh && chmod -R a+rwx /main

COPY src/requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

WORKDIR /main
ENTRYPOINT ["/run.sh"]