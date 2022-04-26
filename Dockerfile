ARG REGISTRY_URL=
FROM ${REGISTRY_URL}tensorflow/tensorflow:2.7.1-gpu-jupyter

ENV PIP_INDEX_URL https://nexus.dspace.kt.co.kr/repository/pypi-dspace-group/simple

ENV PIP_TRUSTED_HOST nexus.dspace.kt.co.kr

# Install apt Dependencies
RUN echo 'deb [arch=amd64 trusted=yes] https://nexus.dspace.kt.co.kr/repository/apt-dspace-ubuntu-proxy bionic main restricted universe' > /etc/apt/sources.list && \
    echo 'deb [arch=amd64 trusted=yes] https://nexus.dspace.kt.co.kr/repository/apt-dspace-ubuntu-proxy bionic-updates main restricted universe' >> /etc/apt/sources.list && \
    echo "machine nexus.dspace.kt.co.kr login archilles password aiduez1234!" >> /etc/apt/auth.conf.d/chelsea.conf 

RUN echo "Acquire::http::Verify-Peer \"false\";" >> /etc/apt/apt.conf.d/00proxy && \
    echo "Acquire::https::Verify-Peer \"false\";" >> /etc/apt/apt.conf.d/00proxy

RUN apt-get update -yq \
 && apt-get install -yq --no-install-recommends \
    wget \
    vim \
    python3-pip \
    python3-tk \
    g++ \
    openjdk-8-jdk \
    python3-dev \
    curl

RUN mkdir -p /opt/code/aiduez \
    && mkdir -p /aihub/workspace \
    && mkdir -p /aihub/data \
    && mkdir -p /opt/conda/bin

RUN ln -s /usr/local/bin/jupyter /opt/conda/bin/jupyter

WORKDIR /opt/code/aiduez
COPY . /opt/code/aiduez
COPY AIDUez.ipynb /aihub/workspace/AIDUez.ipynb

RUN pip3 install --upgrade pip \
    --trusted-host nexus.dspace.kt.co.kr \
    --index http://aidu:new1234!@nexus.dspace.kt.co.kr/repository/pypi-dspace-group/pypi \
    --index-url http://aidu:new1234!@nexus.dspace.kt.co.kr/repository/pypi-dspace-group/simple
RUN pip3 install --no-cache-dir --default-timeout=100 \
    --trusted-host nexus.dspace.kt.co.kr \
    --index http://aidu:new1234!@nexus.dspace.kt.co.kr/repository/pypi-dspace-group/pypi \
    --index-url http://aidu:new1234!@nexus.dspace.kt.co.kr/repository/pypi-dspace-group/simple \
    -r /opt/code/aiduez/requirements.txt

RUN jupyter notebook --generate-config

COPY custom/aiduez_config.yml /root/.aiduez/aiduez_config.yml
COPY custom/custom.css /root/.jupyter/custom/custom.css
COPY custom/custom.js /root/.jupyter/custom/custom.js
COPY custom/index.html.j2 /usr/local/share/jupyter/nbconvert/templates/lab/index.html.j2
COPY custom/configuration.py /usr/local/lib/python3.8/dist-packages/voila/configuration.py
COPY custom/api.py /usr/local/lib/python3.8/dist-packages/ludwig/api.py
COPY custom/file_input.vue /usr/local/lib/python3.8/dist-packages/ipyvuetify/extra/file_input.vue

COPY assets/fonts/Nanum_Gothic/NanumGothic.ttf /usr/share/fonts/
COPY assets/fonts/AppleSD /usr/local/lib/python3.8/dist-packages/notebook/static/components/AppleSD
COPY assets/material_icons /usr/local/lib/python3.8/dist-packages/notebook/static/components/material_icon

WORKDIR /aihub/workspace