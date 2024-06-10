# Dockerfile for ORE backend

FROM ubuntu:xenial

RUN apt-get update \
    && apt-get install -y texlive \
    && rm -rf /var/lib/apt/lists/* 

    RUN apt-get update \
    && apt-get install -y libpq-dev python python-pip libboost-dev libboost-graph-dev libboost-date-time-dev libboost-system-dev libboost-filesystem-dev libboost-program-options-dev cmake gcc libxerces-c-dev xsdcxx \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install requests==2.23.0 certifi==2020.6.20

WORKDIR /ore-back/
COPY backends/ /ore-back/
COPY common/ /ore-common/

RUN cmake .
RUN make -j

EXPOSE 8000
CMD ["python", "daemon.py"]
