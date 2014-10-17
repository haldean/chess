#!/bin/bash

sudo docker run -d -p 5000:5000 --link chess-redis:chess-redis \
    --name chess-frontend haldean/chess-frontend \
    python /chess/start.py --redis_host chess-redis
