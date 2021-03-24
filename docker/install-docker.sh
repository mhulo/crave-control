#!/bin/bash

sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# This adds the user to the group "docker". Log out and back in for this to take effect
sudo usermod -aG docker ${USER}
sudo su - ${USER}
docker version

sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose
sudo docker-compose --version

sudo systemctl enable docker.service
sudo systemctl enable containerd.service