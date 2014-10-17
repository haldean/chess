#!/bin/bash

cat << EOF > Dockerfile
FROM debian:stable
MAINTAINER Haldean Brown <me@haldean.org>
RUN apt-get update && apt-get install -y python python-pip git python-dev
RUN git clone https://github.com/haldean/chess /chess
RUN cd /chess
RUN pip install -r /chess/requirements.txt
EOF
# This is a bit of a hack; we do this after the initial clone and pip install to
# let us use the cache from the installation earlier; for new images, the git
# pull will be a no-op; for cached builds, this speeds everything up
# considerably.
echo "RUN echo Building for git commit $(git rev-parse HEAD)" >> Dockerfile
cat << EOF >> Dockerfile
RUN git pull origin master
RUN mkdir /var/log/chess
RUN python /chess/load_eco.py
ADD api_keys.py /chess/api_keys.py
EOF

sudo docker build -t haldean/chess-frontend .
