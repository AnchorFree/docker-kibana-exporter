FROM alpine:3.5


RUN set -ex \
    && apk upgrade --update-cache \
    && apk add python3=3.5.2-r9

RUN pip3.5 install --upgrade pip \
    && pip3.5 install prometheus_client requests

ADD bin/s.py /usr/bin/s.py
RUN chmod +x /usr/bin/s.py

CMD ["python3.5", "/usr/bin/s.py"]
