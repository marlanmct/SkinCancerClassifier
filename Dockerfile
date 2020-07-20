# Pull Base Image
#FROM ubuntu:latest
FROM nvcr.io/nvidia/l4t-base:r32.3

RUN apt-get install -y apt-transport-https && apt-get update
RUN apt update && apt install -y --fix-missing make g++
RUN apt update && apt install -y --fix-missing python3-pip libhdf5-serial-dev hdf5-tools
RUN apt update && apt install -y python3-h5py
#RUN apt-get -y install python3-pip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# install dependencies
COPY ./src/requirements.txt .

#RUN pip3 install --pre --no-cache-dir --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu
RUN pip3 install -r requirements.txt
RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow
#RUN pip3 install -r requirements.txt
#RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow

# copy code into image and set as working directory
COPY . .
COPY ./src/model/retrained_graph.pb ./src/model/
WORKDIR .
