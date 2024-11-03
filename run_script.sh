#!/bin/bash

eval "$(conda shell.bash hook)"
python ~/code/pi-deployer/main.py --name "$1"
cd ~/code/hosted/"$1"
docker compose build --no-cache
docker compose up -d --force-recreate
