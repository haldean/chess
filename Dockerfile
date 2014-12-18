#!/bin/bash

FROM debian:stable
MAINTAINER Haldean Brown <me@haldean.org>

RUN apt-get update && apt-get install -y python python-pip git python-dev

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /chess/

RUN mkdir /var/log/chess

RUN python /chess/load_eco.py

EXPOSE 5000:5000
CMD ["/usr/bin/python", "/chess/start.py", "--redis_host=chess-redis"]
