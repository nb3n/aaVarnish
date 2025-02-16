#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#Configure the plugin installation directory
install_path=/www/server/panel/plugin/aa_varnish

#Installaion
Install()
{
	
	echo 'Installing...'
	#==================================================================
	#Depends on the installation

	# Detect OS
    OS="$(grep -Eo "(debian|ubuntu|centos|rocky|alma|rhel)" /etc/os-release | head -1)"

    # Install Varnish based on OS
    if [[ "$OS" =~ (debian|ubuntu) ]]; then
        apt update && apt install -y varnish
    elif [[ "$OS" =~ (centos|rocky|alma|rhel) ]]; then
        yum install -y epel-release
        yum install -y varnish
    else
        echo "Unsupported OS: $OS"
        exit 1
    fi

    # Configure Varnish to run on port 6081
    sed -i 's/ExecStart=.*/ExecStart=\/usr\/sbin\/varnishd -a :6081 -T localhost:6082 -F -f \/etc\/varnish\/default.vcl -s malloc,256m/' /lib/systemd/system/varnish.service

    # Reload systemd and restart Varnish
    systemctl daemon-reload
    systemctl enable --now varnish

    echo "Varnish setup complete on $OS!"

	#Depends on the end of installation
	#==================================================================

	echo '================================================'
	echo 'The installation is complete'
}

#Uninstall
Uninstall()
{
	# Detect OS
    OS="$(grep -Eo "(debian|ubuntu|centos|rocky|alma|rhel)" /etc/os-release | head -1)"

    # Stop Varnish service
    systemctl stop varnish
    systemctl disable varnish

    # Remove Varnish package
    if [[ "$OS" =~ (debian|ubuntu) ]]; then
        apt remove -y varnish && apt autoremove -y
    elif [[ "$OS" =~ (centos|rocky|alma|rhel) ]]; then
        yum remove -y varnish
    else
        echo "Unsupported OS: $OS"
        exit 1
    fi

    # Restore original Nginx configuration
    rm -f /etc/nginx/conf.d/varnish.conf
    systemctl restart nginx

    # Remove Varnish data
    rm -rf /etc/varnish
    rm -rf /var/lib/varnish

    echo "Varnish uninstalled successfully from $OS! Nginx remains unaffected."

	# Remove Plugin data/folder
	rm -rf $install_path
}

#Operational judgment
if [ "${1}" == 'install' ];then
	Install
elif [ "${1}" == 'uninstall' ];then
	Uninstall
else
	echo 'Error!';
fi