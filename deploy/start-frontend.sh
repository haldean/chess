#!/bin/bash

sudo docker stop chess-frontend && sudo docker rm chess-frontend
sudo docker run -d -p 5000:5000 --link chess-redis:chess-redis \
    --name chess-frontend haldean/chess-frontend
