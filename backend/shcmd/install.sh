#!/usr/bin/env bash
# https://developers.supportbee.com/blog/setting-up-cucumber-to-run-with-Chrome-on-Linux/
# https://gist.github.com/curtismcmullan/7be1a8c1c841a9d8db2c
# https://stackoverflow.com/questions/10792403/how-do-i-get-chrome-working-with-selenium-using-php-webdriver
# https://stackoverflow.com/questions/26133486/how-to-specify-binary-path-for-remote-chromedriver-in-codeception
# https://stackoverflow.com/questions/40262682/how-to-run-selenium-3-x-with-chrome-driver-through-terminal
# https://askubuntu.com/questions/760085/how-do-you-install-google-chrome-on-ubuntu-16-04

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

# apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4

# Install Chrome.
# curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
wget https://dl.google.com/linux/linux_signing_key.pub
apt-key add linux_signing_key.pub
echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# sudo nano /etc/apt/sources.list.d/google-chrome.list

# deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
# wget https://dl.google.com/linux/linux_signing_key.pub
# apt-key add linux_signing_key.pub
apt-get -y update
apt-get -y install google-chrome-stable

# Install ChromeDriver.
# wget -N https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip -P ~/
# unzip ~/chromedriver_linux64.zip -d ~/
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
# rm ~/chromedriver_linux64.zip
# mv -f ~/chromedriver /usr/local/bin/chromedriver
# chown root:root /usr/local/bin/chromedriver
# chmod 0755 /usr/local/bin/chromedriver