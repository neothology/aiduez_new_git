FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt-get update -yq \
 && apt-get install -yq --no-install-recommends \
    wget \
    vim \
    python3-pip

RUN pip install --upgrade pip \
 && pip install -r requirements.txt
