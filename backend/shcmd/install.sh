#!/usr/bin/env bash

# Remeber download chromedriver_linux64.zip first and put into root path of project

# Remove existing downloads and binaries so we can start from scratch.
apt-get remove google-chrome-stable
# rm ~/chromedriver_linux64.zip
rm /usr/bin/chromedriver

# Install dependencies.
apt-get update
apt-get install tesseract-ocr

# for run the tabula dictionary
apt-get install default-jdk

# Install Chrome.
wget https://dl.google.com/linux/linux_signing_key.pub
apt-key add linux_signing_key.pub
echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
apt-get -y update
apt-get -y install google-chrome-stable

# Install ChromeDriver.
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver