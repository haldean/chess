FROM debian:stable
MAINTAINER Haldean Brown <me@haldean.org>
RUN apt-get update && apt-get install -y python python-pip git python-dev
RUN git clone https://github.com/haldean/chess /chess
RUN cd /chess
RUN pip install -r /chess/requirements.txt
ADD api_keys.py /chess/api_keys.py
