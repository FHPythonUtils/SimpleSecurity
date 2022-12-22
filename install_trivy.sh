#!/bin/bash

# Install Deb-Get
sudo apt install curl
curl -sL https://raw.githubusercontent.com/wimpysworld/deb-get/main/deb-get | sudo -E bash -s install deb-get
# Install Trivy
sudo deb-get install trivy