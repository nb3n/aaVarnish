#!/bin/bash
echo "Uninstalling Varnish..."
yum remove -y varnish || apt remove varnish -y
echo "Varnish uninstalled successfully."
