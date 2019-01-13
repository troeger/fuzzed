# Dockerfile for ORE web application

FROM ubuntu

ENV ORE_MODE production

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y python python-pip apache2 libapache2-mod-wsgi git netcat \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install PyXB defusedxml psycopg2-binary django==1.8.18 python-social-auth==0.2.21 python-openid python-oauth2 django-require django-robots django-configurations requests_oauthlib

RUN pip install git+git://github.com/django-tastypie/django-tastypie.git@256ebe1de9a78dfb5d4d6e938b813cf4c5c4ac1b

RUN rm /etc/apache2/sites-enabled/000-default.conf
COPY frontend/docker/httpd.conf /etc/apache2/sites-enabled/ore.conf

RUN a2enmod wsgi

RUN apache2ctl configtest

COPY frontend/docker/startup.sh /startup.sh
COPY frontend/manage.py /var/www/
COPY frontend/ore  /var/www/ore 
RUN rm -r /var/www/ore/fixtures /var/www/ore/static /var/www/ore/tests

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["bash", "/startup.sh"]

