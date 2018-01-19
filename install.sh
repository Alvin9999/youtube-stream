#!/bin/bash
# author: gfw-breaker

server_home=/usr/local/youtube-stream

## install system dependencies
yum install -y python python-pip vim sysstat

## install python libraries
pip install flask pafy youtube-dl requests

## deploy code
server_ip=$(ifconfig | grep "inet addr" | sed -n 1p | cut -d':' -f2 | cut -d' ' -f1)
sed -i "s/local_server_ip/$server_ip/g" server.py
sed -i "s/local_server_ip/$server_ip/g" templates/index.html 
mkdir -p $server_home
cp -R * $server_home 

## enable and start service
chmod +x yt-stream
cp yt-stream /etc/init.d
chkconf yt-stream on
service yt-stream start


