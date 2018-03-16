# Dockerfile for ORE backend applications (developer)

FROM ubuntu

# Prepare Ansible environment
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev libxerces-c-dev xsdcxx cmake gcc \
                          texlive libboost-dev libboost-graph-dev libboost-date-time-dev \
                          libboost-system-dev libboost-filesystem-dev \
                          libboost-program-options-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip

COPY requirements.txt /install/
RUN pip3 install -r /install/requirements.txt

ENV PYTHONUNBUFFERED 1
EXPOSE 8001
