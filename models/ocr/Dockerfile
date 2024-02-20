FROM nvidia/cuda:12.3.0-base-ubuntu20.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y \
        python3-pip \
	build-essential \ 
        libssl-dev \
        libffi-dev \
        python3-dev \
	python3-venv
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3",  "./main.py" ]
