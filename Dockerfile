FROM tensorflow/tensorflow:latest-gpu-jupyter

RUN apt-get update -yq \
 && apt-get install -yq --no-install-recommends \
    wget \
    vim \
    python3-pip

RUN mkdir -p /opt/code
COPY . /opt/code
WORKDIR /opt/code

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

RUN jupyter notebook --generate-config

COPY custom/aiduez_config.yml /root/.aiduez/aiduez_config.yml
COPY custom/custom.css /root/.jupyter/custom/custom.css
COPY custom/index.html.j2 /usr/local/share/jupyter/nbconvert/templates/lab/index.html.j2

CMD [ "jupyter", "notebook", "--allow-root", "--NotebookApp.token=''", "--no-browser", "--ip=0.0.0.0" ]