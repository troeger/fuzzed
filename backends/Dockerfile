# Dockerfile for ORE backend

FROM ubuntu

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y ansible \
    && rm -rf /var/lib/apt/lists/* 

COPY ansible /ansible

# Install dependencies via Ansible
RUN ansible-playbook -i /ansible/inventories/localhost /ansible/dev_be.yml 
