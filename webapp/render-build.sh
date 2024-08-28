#!/usr/bin/env bash

# Create a directory for Chrome installation
mkdir -p /opt/chrome

# Download and install Chromium
apt-get update && apt-get install -y wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /opt/chrome/chrome.deb
apt-get install -y /opt/chrome/chrome.deb

# Ensure ChromeDriver is installed
chromedriver_autoinstaller.install()

# Optionally, you can install additional dependencies
apt-get install -y \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libgtk-3-0
