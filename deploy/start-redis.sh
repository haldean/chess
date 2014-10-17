#!/bin/bash

sudo docker run \
    --name chess-redis -v `pwd`/local-data/redis/:/data -d \
    redis:2.8 redis-server --appendonly yes
