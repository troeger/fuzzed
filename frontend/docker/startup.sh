# Assumes "frontend" directory to be mounted at /ore-front

cd /ore-front
scons 
./manage.py migrate auth
./manage.py migrate
./manage.py runserver 0.0.0.0:8000