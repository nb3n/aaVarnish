#!/bin/bash
NGINX_CONF_DIR="/www/server/panel/data/vhost"
BACKUP_DIR="./backup/nginx"

case $1 in
    enable_varnish)
        DOMAIN=$2
        CONFIG_FILE="$NGINX_CONF_DIR/${DOMAIN}.conf"
        
        # Create backup
        mkdir -p $BACKUP_DIR
        cp $CONFIG_FILE "$BACKUP_DIR/${DOMAIN}.conf.bak"
        
        # Modify port from 80 -> 8080
        sed -i 's/listen 80;/listen 8080;/g' $CONFIG_FILE
        
        # Reload Nginx
        systemctl reload nginx
        echo '{"status":true,"msg":"Nginx configured for Varnish"}'
        ;;
        
    disable_varnish)
        DOMAIN=$2
        # Restore original config
        cp "$BACKUP_DIR/${DOMAIN}.conf.bak" "$NGINX_CONF_DIR/${DOMAIN}.conf"
        systemctl reload nginx
        echo '{"status":true,"msg":"Nginx configuration restored"}'
        ;;
        
    restore_all)
        # Restore all backups
        cp $BACKUP_DIR/*.conf.bak $NGINX_CONF_DIR/
        systemctl reload nginx
        echo '{"status":true,"msg":"All Nginx configs restored"}'
        ;;
esac