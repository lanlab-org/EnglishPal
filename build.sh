#!/bin/sh

DEPLOYMENT_DIR=/home/lanhui/EnglishPal
cd $DEPLOYMENT_DIR

# Stop service
sudo docker stop EnglishPal
sudo docker rm EnglishPal

# Rebuild container. Run this after modifying the source code.
sudo docker build -t englishpal .

# Run the application
sudo docker run -d --name EnglishPal -p 90:80 -v ${DEPLOYMENT_DIR}/app/static/frequency:/app/static/frequency -v ${DEPLOYMENT_DIR}/app/static/:/app/static/ -t englishpal  # for permanently saving data

# Save space.  Run it after sudo docker run
sudo docker system prune -a -f
