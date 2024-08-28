#!/usr/bin/env bash

apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
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

ln -s /usr/bin/chromium-browser /usr/bin/google-chrome
