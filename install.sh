#!/bin/bash
echo "Checking if Nginx is installed..."
if ! command -v nginx &> /dev/null; then
    echo "Nginx is required. Please install it first."
    exit 1
fi

echo "Installing Varnish..."
yum install -y varnish || apt install varnish -y
systemctl enable varnish
systemctl start varnish
echo "Varnish installed successfully."
