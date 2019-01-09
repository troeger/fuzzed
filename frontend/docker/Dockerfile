# Dockerfile for ORE web application

FROM ubuntu

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y ansible \
    && rm -rf /var/lib/apt/lists/* 

# Copy ansible script instead of mounting, so that
# changes in the roles trigger an docker image rebuilt
COPY ansible /ansible

# Install dependencies via Ansible
RUN ansible-playbook -i /ansible/inventories/localhost /ansible/dev_fe.yml 

COPY frontend/docker/startup.sh /startup.sh

ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION Dev
EXPOSE 8000
CMD ["bash", "/startup.sh"]
