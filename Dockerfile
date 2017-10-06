FROM ubuntu:xenial

RUN apt-get update --fix-missing && apt-get install --no-install-recommends -y \
    vim nano \
    build-essential cmake g++ libboost-all-dev libxerces-c-dev xsdcxx \
    ansible python-django python-pip python-setuptools

ENV HOME /root
USER root
WORKDIR /root
