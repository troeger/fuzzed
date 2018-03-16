# Dockerfile for ORE web application (developer)

FROM ubuntu

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev phantomjs node-less \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip

COPY requirements.txt /install/
RUN pip3 install -r /install/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION Dev
EXPOSE 8000