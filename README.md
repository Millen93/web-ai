## Instruction to Start WebChat

---
#### Requirements:
#### **PostgreSQL, Python3, Python3-venv, Docker**
---

## Run on host with script.sh

### Install PostgreSQL

**Download PostgreSQL**

```shell
sudo apt update && sudo apt upgrade
sudo apt install postgresql postgresql-contrib
```

**Enable PostgreSQL instance**
```shell
sudo systemctl enable postgresql
# create database and user for web chat
sudo -u postgres psql -c "CREATE DATABASE web_chat;" -c "CREATE USER admin with password 'admin';" -c "GRANT ALL PRIVILEGES ON DATABASE web_chat TO admin;"

```
### Install Python3-venv

```shell
sudo apt install python3.10-venv
```

### Install Docker
```shell
# Add Docker's official GPG key:
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# Add current user to docker group
sudo usermod -aG docker $USER
```

### Install GPU drivers to run LLM model

```shell
$ sudo add-apt-repository ppa:graphics-drivers/ppa  
$ sudo apt update  
$ sudo apt install ubuntu-drivers-common  
$ sudo apt dist-upgrade  
$ sudo reboot  
$ sudo ubuntu-drivers autoinstall  
$ sudo reboot
```

### Change .env file and define your vars

- **DB_HOST** - IP address of your PostgreSQL instance ( If you are running on docker compose specify 172.18.0.3 )
- **DB_PORT** - Port of your PostgreSQL instance ( If u running on docker specify 5432 )
- **DB_NAME** - Name of your PostgreSQL database ( If u running on docker specify postgres )
- **DB_USER** - Username to connect PostgreSQL database ( If u running on docker specify postgres )
- **DB_PASS** - Password to connect PostgreSQL database ( If u running on docker specify postgres )
- **SECRET_AUTH** - Token to use in jwt auth
- **AUTH_DB** - Disable usage of database and authentication

### Run chat

If you want to enable text-to-image and OCR models, you can run them with Python3 or Docker

When you running extra-models with main.py python3 you should change url in file src/chat/llm_model.py
```shell
sed -i 's/172.18.0.4/127.0.0.1/' src/chat/llm_model.py
sed -i 's/172.18.0.5/127.0.0.1/' src/chat/llm_model.py
```

Run extra Models
```shell
#Run by python3 text-to-image model
pip install -r models/text-to-image/requirements.txt
python3 models/text-to-image/main.py
#Run by python3 ocr model
pip install -r models/ocr/main.py
python3 models/ocr/main.py
#Run by docker text-to-image model
docker network create -d bridge models --subnet 172.18.0.0/32
docker run -it $(docker build -q models/text-to-image/) -p 7000:7000 --ip 172.18.0.4
#Run by docker ocr model
docker run -it $(docker build -q models/ocr/) -p 6000:6000 --ip 172.18.0.5
```

Run **Web-chat**
```shell
chmod +x script.sh
./script.sh
```



---

## If u want to run on Docker

Enable nvidia docker runtime
```shell
$ distribution=$(. /etc/os-release;echo  $ID$VERSION_ID)  
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -  
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit
$ sudo nvidia-ctk runtime configure --runtime=docker
$ sudo systemctl restart docker
```

### Run chat
By Docker Compose

```shell
$ docker compose up
```
