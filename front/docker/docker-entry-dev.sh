#!/bin/bash
set -e

# Docker image startup script

echo "Waiting for database ..."

# Wait for postgres to come up
while ! nc -z $FUZZED_DATABASE_HOST $FUZZED_DATABASE_PORT 
do
    let elapsed=elapsed+1
    if [ "$elapsed" -gt 90 ] 
    then
        echo "Could not connect to database container."
        exit 1
    fi  
    sleep 1;
    echo "... still waiting ..."
done
echo "Database is up."

cd /ore/front

# generate neccessary files
make

# perform relevant database migrations
./manage.py migrate

# Start dev server
./manage.py runserver
