<?php

class varnish_cache {
    
    public function __construct(){
        $this->plugin_path = dirname(__FILE__);
        $this->config_path = $this->plugin_path.'/config/';
        $this->view_path = $this->plugin_path.'/view/';
    }
    
    public function onInstall(){
        // Check Nginx installation
        if(!file_exists('/www/server/nginx/')){
            return ['status'=>false, 'msg'=>'Nginx not installed'];
        }
        
        // Install Varnish
        $result = $this->execShell('scripts/varnish.sh install');
        if(!$result['status']){
            return $result;
        }
        
        return ['status'=>true, 'msg'=>'Installed successfully'];
    }
    
    public function onUninstall(){
        // Restore original configurations
        $this->execShell('scripts/nginx.sh restore_all');
        $this->execShell('scripts/varnish.sh uninstall');
        return ['status'=>true];
    }
    
    public function index(){
        $sites = $this->getNginxSites();
        include $this->view_path.'index.html';
    }
    
    public function toggleCache(){
        $site = $this->request('site');
        $status = $this->request('status');
        
        if($status == 'true'){
            $this->execShell("scripts/nginx.sh enable_varnish {$site}");
            $this->execShell("scripts/varnish.sh configure {$site}");
        }else{
            $this->execShell("scripts/nginx.sh disable_varnish {$site}");
        }
        
        return ['status'=>true];
    }
    
    private function getNginxSites(){
        $sites = [];
        $path = '/www/server/panel/data/vhost/';
        foreach(glob($path.'*.conf') as $file){
            $content = file_get_contents($file);
            preg_match('/server_name\s+(.+);/', $content, $matches);
            if($matches[1]){
                $sites[] = [
                    'name' => trim($matches[1]),
                    'config' => $file
                ];
            }
        }
        return $sites;
    }
    
    private function execShell($command){
        // aaPanel recommended execution method
        $result = shell_exec('sh '.$this->plugin_path.'/'.$command);
        return json_decode($result, true);
    }

    public function saveConfig(){
        $ttl = $this->request('ttl', 'int', 120);
        $memory = $this->request('memory', 'text', '256M');
        
        // Update Varnish systemd service
        $service_file = '/etc/systemd/system/varnish.service';
        $config = file_get_contents($service_file);
        $config = preg_replace('/-s malloc,.* \\\/', "-s malloc,$memory \\\\", $config);
        file_put_contents($service_file, $config);
        
        // Update default TTL in VCL
        $vcl_template = file_get_contents($this->config_path.'varnish.vcl');
        $vcl_template = preg_replace('/beresp.ttl = .*h;/', "beresp.ttl = {$ttl}m;", $vcl_template);
        file_put_contents($this->config_path.'varnish.vcl', $vcl_template);
        
        $this->execShell('scripts/varnish.sh reload');
        return ['status'=>true, 'msg'=>'Configuration updated'];
    }
}
