#!/bin/bash

sudo docker stop chess-redis && sudo docker rm chess-redis
sudo docker run \
    --name chess-redis -v `pwd`/local-data/redis/:/data -d \
    redis:2.8 redis-server --appendonly yes
