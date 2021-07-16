#!/bin/bash

echo "Building image"
docker build -t wisuchoi/bookshop-flask .

echo "Saving image to a local file"
docker save wisuchoi/bookshop-flask > bookshop-flask-image.tar

# Or push to Docker Hub or a Container Registry
#echo "Pushing image to Docker Hub"
#docker push <hub-user>/<repo-name>:<tag>
