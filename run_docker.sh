#!/usr/bin/env bash

echo killing old docker processes
docker-compose rm -fs

echo building docker containers
docker-compose up --build -d

until docker exec feature /bin/bash -c "python3 manage.py db upgrade"
do
    echo "Waiting for postgres ready..."
    sleep 2
done

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
