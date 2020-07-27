# Pull Base Image
#FROM ubuntu:latest
FROM nvcr.io/nvidia/l4t-base:r32.3

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#RUN apt-get install -y apt-transport-https && apt-get update
RUN apt update && apt install -y --fix-missing \ 
    make \
    g++ \
    gfortran \
    build-essential \
    hdf5-tools \
    libatlas-base-dev \
    libhdf5-100 \
    libhdf5-dev \
    liblapack-dev \
    libopenblas-dev \
    python3-pip \
    pkg-config
     
# install dependencies
RUN pip3 install -U cython
RUN pip3 install -U numpy==1.19.1 
RUN pip3 install -U grpcio h5py
COPY ./src/requirements.txt .
#grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta
RUN pip3 install -U -r requirements.txt
RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow==1.15.2+nv20.3

# copy code into image and set as working directory
COPY . .
WORKDIR /src/
