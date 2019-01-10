# Dockerfile for ORE web application

FROM ubuntu

ENV ORE_MODE development

RUN apt-get update \
    && apt-get install -y python-dev python-pip scons npm git netcat \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install PyXB defusedxml psycopg2-binary django==1.8.18 python-social-auth==0.2.21 python-openid python-oauth2 django-require django-robots django-configurations requests_oauthlib

RUN pip install git+git://github.com/django-tastypie/django-tastypie.git@256ebe1de9a78dfb5d4d6e938b813cf4c5c4ac1b

RUN npm install -g less mocha-phantomjs

COPY frontend/docker/startup.sh /startup.sh

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD ["bash", "/startup.sh"]
