#!/usr/bin/env bash

echo "killing old docker processes"

# clean up dangling docker images
docker rmi $(docker images --filter dangling=true --quiet)

echo "pulling latest code from git repository..."

# pull latest from git repo
git pull origin master

# build and deploy docker image
docker-compose rm -fs
docker-compose build
docker-compose up -d

# Run new migrations if any.
until docker exec feature /bin/bash -c "python3 manage.py db upgrade"
do
    echo "Waiting for postgres ready..."
    sleep 2
done

# Block: Run this block once to load initial data and remove for subsequent deployments
until docker exec feature /bin/bash -c "python3 manage.py loaddata"
do
    echo "Waiting for postgres upgrade ready..."
    sleep 2
done

until docker exec feature /bin/bash -c "python3 manage.py create_admin"
do
    echo "Waiting for postgres loaddata ready..."
    sleep 2
done

# Block end.

echo "cleaning up dangling docker volumes..."

# clean up dangling docker volumes
sleep 5
docker volume rm $(docker volume ls -qf dangling=true --quiet)

echo "Feature request successfully updated!"