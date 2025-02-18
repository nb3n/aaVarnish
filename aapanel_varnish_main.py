#!/usr/bin/python
# coding: utf-8

import public  # aaPanel helper functions
import os
import time
import logging

class aapanel_varnish_main:
    # Set up the logger
    def __init__(self):
        log_folder = "/www/server/panel/plugin/aapanel_varnish/logs/"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = os.path.join(log_folder, "varnish_operations.log")
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        
    # Get logs from the logs folder
    def get_logs(self, args):
        log_folder = "/www/server/panel/plugin/aapanel_varnish/logs/"
        log_files = [f for f in os.listdir(log_folder) if os.path.isfile(os.path.join(log_folder, f))]
        logs = []
        
        for log_file in log_files:
            log_path = os.path.join(log_folder, log_file)
            with open(log_path, 'r') as file:
                log_content = file.readlines()[-10:]  # Get last 10 lines for display
                for line in log_content:
                    logs.append({
                        'filename': log_file,
                        'content': line.strip(),
                        'timestamp': os.path.getmtime(log_path)
                    })
        
        return public.ReturnMsg(True, logs)

    # Clean up the logs by deleting the log files
    def clean_up_logs(self, args):
        log_folder = "/www/server/panel/plugin/aapanel_varnish/logs/"
        log_files = os.listdir(log_folder)

        for log_file in log_files:
            log_path = os.path.join(log_folder, log_file)
            os.remove(log_path)

        return public.ReturnMsg(True, "Logs cleaned successfully.")
    
    # Check Varnish service status
    def get_varnish_status(self, args):
        status = public.ExecShell("systemctl is-active varnish")[0].strip()
        is_running = status == "active"
        return public.ReturnMsg(True, {"status": is_running, "message": "Running" if is_running else "Stopped"})

    # Start Varnish
    def start_varnish(self, args):
        try:
            public.ExecShell("systemctl start varnish")
            log_message = "Varnish started successfully."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to start Varnish: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)

    # Stop Varnish
    def stop_varnish(self, args):
        try:
            public.ExecShell("systemctl stop varnish")
            log_message = "Varnish stopped successfully."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to stop Varnish: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)

    # Restart Varnish
    def restart_varnish(self, args):
        try:
            public.ExecShell("systemctl restart varnish")
            log_message = "Varnish restarted successfully."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to restart Varnish: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)
    
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
        try:
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
            log_message = f"Varnish enabled for {domain}."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to enable Varnish for {domain}: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)

    # Disable caching for a domain
    def disable_cache(self, args):
        try:
            domain = args.domain
            config_path = f"/www/server/panel/plugin/aapanel_varnish/{domain}.conf"

            if os.path.exists(config_path):
                os.remove(config_path)

            public.ServiceReload()
            log_message = f"Varnish disabled for {domain}."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to disable Varnish for {domain}: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)

    # Purge cache
    def purge_cache(self, args):
        try:
            domain = args.domain
            public.ExecShell(f"varnishadm ban req.http.host == {domain}")
            log_message = f"Cache purged for {domain}."
            logging.info(log_message)
            return public.ReturnMsg(True, log_message)
        except Exception as e:
            error_message = f"Failed to purge cache for {domain}: {str(e)}"
            logging.error(error_message)
            return public.ReturnMsg(False, error_message)

    # Get list of all Nginx-hosted websites with Varnish status
    def get_websites(self, args):
        sites = public.M('sites').field('name').select()
        varnish_config_path = "/www/server/panel/plugin/aapanel_varnish/"
        
        for site in sites:
            domain = site["name"]
            config_file = os.path.join(varnish_config_path, f"{domain}.conf")
            site["varnish_status"] = os.path.exists(config_file)
        
        return public.ReturnMsg(True, sites)