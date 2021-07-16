#!/bin/bash

# echo "Loading an image" # Alternative is to pull from a registry
# docker load < bookshop-flask-image.tar

# CURRENT_ENV="dev" # From CD tool

echo "Run docker container"
docker run \
--name my-flask-app \
-p 5005:5000 \
--rm \
-d \
--env-file="./deployment/${CURRENT_ENV}.env" \
wisuchoi/bookshop-flask