
# Wait for postgres to come up
echo "Waiting for database at '$ORE_DB_HOST' ..."
while ! nc -z $ORE_DB_HOST 5432 2>/dev/null
do
    let elapsed=elapsed+1
    if [ "$elapsed" -gt 10 ] 
    then
        echo "Could not connect to database container."
        exit 1
    fi  
    sleep 1;
done
echo "Database is up."

if [ "$ORE_MODE" = "development" ]
then
    # Assumes "frontend" directory to be mounted at /ore-front
    cd /ore-front
    export DJANGO_CONFIGURATION=Dev
    ./manage.py migrate 
    ./manage.py runserver 0.0.0.0:8000
fi

if [ "$ORE_MODE" = "production" ]
then
    cd /var/www
    export DJANGO_CONFIGURATION=Production
    ./manage.py migrate 
    rm -f /var/run/apache2/apache2.pid
    apache2ctl -D FOREGROUND
fi
