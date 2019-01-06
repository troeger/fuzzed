# Assumes host directory to be mounted at /ore-front
cd /ore-front
scons 
./manage.py migrate
./manage.py runserver