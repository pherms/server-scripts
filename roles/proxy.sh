#!/bin/bash

echo "Installing nginx"
apt update
apt install -y nginx nginx-doc

echo "Start en enable nginx"
systemctl enable nginx
systemctl start nginx