FROM conda/miniconda3

RUN apt-get update && \
    apt-get install -y sudo \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    wget \
    python 3.6 python3-pip \
    libxrender-dev \
    libxext6 \
    libsm6 \
    openssl \
    python3-dev git

RUN mkdir -p /opt/service
RUN mkdir -p /opt/service/summarizer
COPY summarizer /opt/service/summarizer
COPY server.py /opt/service
COPY environment.yml /opt/service
WORKDIR /opt/service

RUN conda create -n summary python=3.6 \
    && conda env update -n summary -f environment.yml \
    && echo "source activate summary" >> ~/.bashrc

ENV PATH /opt/conda/envs/env/bin:$PATH
CMD /bin/bash -c "source activate summary && python server.py"