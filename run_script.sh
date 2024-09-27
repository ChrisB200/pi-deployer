#!/bin/bash

conda init
conda activate pi-deployer
python ~/code/pi-deployer/main.py --name "$1"
cd ~/code/hosted/"$1"
docker compose up -d --force-recreate
conda deactivate