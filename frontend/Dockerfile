# Dockerfile for ORE web application

FROM ubuntu:bionic

ENV DJANGO_CONFIGURATION=Production
ENV DEBIANFRONTEND=nointeractive

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y python python-pip git nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN pip install PyXB==1.2.6 defusedxml==0.7.1 psycopg2-binary==2.8.6 django==1.8.18 python-social-auth==0.2.21 python-openid==2.2.5 python-oauth2==1.1.1 django-require==1.0.11 django-robots==3.1.0 django-configurations==2.0 requests_oauthlib==1.1.0 uwsgi==2.0.18

RUN pip install git+https://github.com/django-tastypie/django-tastypie.git@256ebe1de9a78dfb5d4d6e938b813cf4c5c4ac1b

WORKDIR /ore-front
COPY frontend/ /ore-front

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
CMD sh -c '/ore-front/manage.py collectstatic -v3 --noinput && /ore-front/manage.py migrate && uwsgi --http 0.0.0.0:8000 --wsgi-file ore/wsgi.py --static-map /static/=/ore-front/ore/static-release/'
