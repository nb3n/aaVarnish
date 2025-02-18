#!/usr/bin/python
# coding: utf-8

import public  # aaPanel helper functions
import os

class aapanel_varnish_main:
    # Check Varnish service status
    def get_varnish_status(self, args):
        status = public.ExecShell("systemctl is-active varnish")[0].strip()
        is_running = status == "active"
        return public.ReturnMsg(True, {"status": is_running, "message": "Running" if is_running else "Stopped"})

    # Start Varnish
    def start_varnish(self, args):
        public.ExecShell("systemctl start varnish")
        return public.ReturnMsg(True, "Varnish started successfully.")

    # Stop Varnish
    def stop_varnish(self, args):
        public.ExecShell("systemctl stop varnish")
        return public.ReturnMsg(True, "Varnish stopped successfully.")

    # Restart Varnish
    def restart_varnish(self, args):
        public.ExecShell("systemctl restart varnish")
        return public.ReturnMsg(True, "Varnish restarted successfully.")
    
    # Check if Nginx is installed
    def check_nginx_installed(self, args):
        web_server = public.GetWebServer()
        if web_server != "nginx":
            return public.ReturnMsg(False, "Nginx is not installed. Please install Nginx first.")
        return public.ReturnMsg(True, "Nginx is installed.")

    # Install Varnish
    def install_varnish(self, args):
        if not self.check_nginx_installed(args)["status"]:
            return public.ReturnMsg(False, "Cannot install Varnish. Nginx is required.")
        
        public.ExecShell("yum install -y varnish")
        return public.ReturnMsg(True, "Varnish installed successfully.")

    # Enable caching for a domain
    def enable_cache(self, args):
        domain = args.domain
        config_path = f"/www/server/panel/plugin/aapanel_varnish/{domain}.conf"

        varnish_config = f"""
        backend default {{
            .host = "127.0.0.1";
            .port = "80";
        }}

        sub vcl_recv {{
            if (req.http.host == "{domain}") {{
                return (pass);
            }}
        }}
        """
        
        public.WriteFile(config_path, varnish_config)
        public.ServiceReload()
        return public.ReturnMsg(True, f"Varnish enabled for {domain}")

    # Disable caching for a domain
    def disable_cache(self, args):
        domain = args.domain
        config_path = f"/www/server/panel/plugin/aapanel_varnish/{domain}.conf"

        if os.path.exists(config_path):
            os.remove(config_path)
        
        public.ServiceReload()
        return public.ReturnMsg(True, f"Varnish disabled for {domain}")

    # Purge cache
    def purge_cache(self, args):
        domain = args.domain
        public.ExecShell(f"varnishadm ban req.http.host == {domain}")
        return public.ReturnMsg(True, f"Cache purged for {domain}")

    # Get list of all Nginx-hosted websites with Varnish status
    def get_websites(self, args):
        sites = public.M('sites').field('name').select()
        varnish_config_path = "/www/server/panel/plugin/aapanel_varnish/"
        
        for site in sites:
            domain = site["name"]
            config_file = os.path.join(varnish_config_path, f"{domain}.conf")
            site["varnish_status"] = os.path.exists(config_file)
        
        return public.ReturnMsg(True, sites)