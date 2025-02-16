#!/bin/bash
case $1 in
    install)
        systemctl enable varnish
        systemctl start varnish
        ;;
    configure)
        DOMAIN=$2
        # Generate VCL from template
        sed "s/{{DOMAIN}}/$DOMAIN/g" ../config/varnish.vcl > /etc/varnish/$DOMAIN.vcl
        systemctl reload varnish
        ;;
    uninstall)
        systemctl stop varnish
        yum remove -y varnish || apt-get remove -y varnish
        ;;
esac