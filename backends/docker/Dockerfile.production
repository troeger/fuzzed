# Dockerfile for ORE backend

FROM ubuntu:xenial

RUN apt-get update \
    && apt-get install -y texlive \
    && rm -rf /var/lib/apt/lists/* 

RUN apt-get update \
    && apt-get install -y python python-pip  libboost-dev libboost-graph-dev libboost-date-time-dev libboost-system-dev libboost-filesystem-dev libboost-program-options-dev libxerces-c-dev xsdcxx \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install requests

COPY backends/docker/startup.sh /ore-back/startup.sh
COPY backends/daemon.py /ore-back/daemon.py
COPY backends/daemon.ini /ore-back/daemon.ini
COPY backends/lib /ore-back/lib
COPY backends/rendering /ore-back/rendering

EXPOSE 8000
CMD ["bash", "/ore-back/startup.sh"]
