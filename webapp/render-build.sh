#!/usr/bin/env bash

# Set up a directory to store Chrome and Chromedriver
mkdir -p /usr/local/share/chrome
cd /usr/local/share/chrome

# Download the latest stable Chromium and Chromedriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Extract the downloaded file
ar x google-chrome-stable_current_amd64.deb
tar -xvf data.tar.xz

# Move binaries to the local directory
mv ./opt/google/chrome /usr/local/share/chrome/

# Clean up
rm -rf google-chrome-stable_current_amd64.deb
