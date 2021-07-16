#!/bin/sh

cd /home/lanhui/englishpal

# Stop service
sudo docker stop EnglishPal

# Rebuild container. Run this after modifying the source code.
sudo docker build -t englishpal .

# Run the application
sudo docker run -d --name EnglishPal -p 90:80 -v /home/lanhui/englishpal/app/static/frequency:/app/static/frequency -t englishpal  # for permanently saving data

# Save space.  Run it after sudo docker run
sudo docker system prune -a -f


