# Feature Request
A platform for adding new feature that will be added onto an existing piece of software. 

## Setup and installation
Pull the github repo
```bash
git clone https://github.com/cosmic-byte/feature-request.git
```
Create a virtual environment to store project's Python requirements
```bash
cd feature-request
virtualenv venv
source venv/bin/activate
```
Setup database and environment variables

Create a postgres database
```bash
sudo -i -u postgres psql
create database feature;
grant all PRIVILEGES on database feature to postgres;

```
Export environment variables: in your terminal execute the following commands
```bash
 export DATABASE_URL='postgresql://postgres:postgres@localhost/feature'
 export SECRET_KEY='your-preferred-secret-key'

```

## Run without Docker 
Install python requirements
```bash
cd main/
make install #initial installation
```

Run database migrations
```bash
python manage.py db upgrade
```
Seed initial fixture data
```bash
python manage.py loaddata
python manage.py create_admin 

```
Run

```bash
make tests  #run tests
make run   #run the app
make all   #run all commands (clean install tests run)

```
Launch your browser and access the app with `localhost:5000`, Login with email `admin@wip.com` 
and password `password123`

## Run with Docker (Development Environment)
Note: make sure docker and docker-compose is installed

```bash
sh deploy_dev.sh
```
Launch your browser and access the app with `localhost:8001`, Login with email `admin@wip.com` 
and password `password123`

## Run with Docker (Production Environment)
Note: make sure docker and docker-compose is installed on your server

SSH into you linux server `ssh user@host`, 
Create a project directory `mkdir directoryName`,
clone github repo `git clone https://github.com/cosmic-byte/feature-request.git`,
execute the following commands:

```bash
cd feature-request/
sh deploy_prod.sh
```

Confirm the docker containers are running using `docker ps`,
Launch your browser and access the running app with your hostname and port `8001`
Login with email `admin@wip.com` and password `password123`