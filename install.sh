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
	echo 'Copying Pluin Logo to static asset' 
	cp -a -r /www/server/panel/plugin/aa_varnish/icon.png /www/server/panel/static/img/soft_ico/ico-aa_varnish.png

	#Depends on the end of installation
	#==================================================================

	echo '================================================'
	echo 'The installation is complete'
}

#Uninstall
Uninstall()
{
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
