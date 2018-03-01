# Dockerfile for ORE web application

FROM ubuntu

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y ansible \
    && rm -rf /var/lib/apt/lists/* 

COPY ansible /ansible

# Install dependencies via Ansible
RUN ansible-playbook -i /ansible/inventories/localhost /ansible/dev.yml 

ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION Dev
EXPOSE 8000

