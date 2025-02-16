#!/bin/bash
PLUGIN_DIR=$(dirname "$(readlink -f "$0")")

# Stop and remove Varnish
if systemctl is-active --quiet varnish; then
    systemctl stop varnish
fi

if [ -f /etc/redhat-release ]; then
    yum remove -y varnish
elif [ -f /etc/lsb-release ]; then
    apt-get purge -y varnish
fi

# Restore Nginx configurations
$PLUGIN_DIR/scripts/nginx.sh restore_all

# Remove plugin files
rm -rf $PLUGIN_DIR
echo '{"status":true,"msg":"Varnish Cache plugin completely removed"}'