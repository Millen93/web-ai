FROM nvidia/cuda:12.3.1-base-ubuntu20.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        python3-opencv \
	      python3.8-venv \
        libglib2.0-0 
WORKDIR /app
RUN python3.8 -mvenv /app/dev 
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3",  "./main.py" ]
