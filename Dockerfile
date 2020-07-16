# Pull Base Image
FROM ubuntu:latest

RUN apt-get install -y apt-transport-https && apt-get update
RUN apt-get -y install python3-pip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install dependencies
COPY ./src/requirements.txt .
RUN pip3 install -r requirements.txt

# copy code into image and set as working directory
COPY . .
COPY ./src/model/retrained_graph.pb ./src/model/
WORKDIR .
