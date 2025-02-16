#!/bin/bash
# Check dependencies
if ! [ -x "$(command -v nginx)" ]; then
    echo '{"status":false,"msg":"Nginx not found"}'
    exit 1
fi

# Install Varnish based on OS
if [ -f /etc/redhat-release ]; then
    yum install -y varnish
elif [ -f /etc/lsb-release ]; then
    apt-get install -y varnish
fi

# Backup original configs
mkdir -p backup/nginx
cp /www/server/nginx/conf/nginx.conf backup/nginx/

echo '{"status":true,"msg":"Installation complete"}'