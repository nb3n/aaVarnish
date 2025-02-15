#!/usr/bin/python
# coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: xxx <xxxx@qq.com>
# +-------------------------------------------------------------------

#+--------------------------------------------------------------------
#|   Pagoda Third Party Application Development
#+--------------------------------------------------------------------
import sys,os,json

#Set the running directory
os.chdir("/www/server/panel")

#Add package reference location and reference public package
sys.path.append("class/")
import public

#from common import dict_obj
#get = dict_obj();


#Reference panel cache and session objects in non-command line mode
if __name__ != '__main__':
    from BTPanel import cache,session,redirect

    #Set the cache (timeout 10 seconds) cache.set ('key', value, 10)
    #Get cache cache.get ('key')
    #Delete cache cache.delete ('key')

    #Set session: session ['key'] = value
    #Get session: value = session ['key']
    #Delete session: del (session ['key'])


class demo_main:
    __plugin_path = "/www/server/panel/plugin/demo/"
    __config = None

#Construction method
    def  __init__(self):
        pass

    #Custom access checks
    #Once this method is declared, this means that you can directly access this plugin without logging in to the panel, and the _check method is used to detect whether there is access
    #If your plug-in must be logged in to access it, please do not declare this method as this could lead to serious security holes
    #If the permission verification is passed, return True, otherwise return False or public.returnMsg (False, 'reason for failure')
    #Access the get_logs method without logging in to the panel: /demo/get_logs.json or /demo/get_logs.html (using a template)
    #The requested method name can be obtained through args.fun
    #Client IP can be obtained through args.client_ip
    def _check(self,args):
        #token = '123456'
        #limit_addr = ['192.168.1.2','192.168.1.3']
        #if args.token != token: return public.returnMsg(False,'Token verification failed!')
        #if not args.client_ip in limit_addr: return public.returnMsg(False,'IP access is restricted!')
        #return redirect('/login')
        return True

    #The default method called when accessing /demo/index.html requires index.html in the templates, otherwise it will not respond to the template correctly
    def index(self,args):
        return self.get_logs(args)


    #Get list of panel logs
    #The traditional way to access the get_logs method：/plugin?action=a&name=demo&s=get_logs
    #Output using dynamic routing template： /demo/get_logs.html
    #Output JSON using dynamic routing： /demo/get_logs.json
    def get_logs(self,args):
        #Handle parameters from the front end
        if not 'p' in args: args.p = 1
        if not 'rows' in args: args.rows = 12
        if not 'callback' in args: args.callback = ''
        args.p = int(args.p)
        args.rows = int(args.rows)

        #Handle parameters from the front end
        count = public.M('logs').count()

        #Get paging data
        page_data = public.get_page(count,args.p,args.rows,args.callback)

        #Get the data list of the current page
        log_list = public.M('logs').order('id desc').limit(page_data['shift'] + ',' + page_data['row']).field('id,type,log,addtime').select()
        
        #Return data to the front end
        return {'data': log_list,'page':page_data['page'] }
        
    #Read configuration items (the configuration file of the plugin itself)
    #@param key Take the specified configuration item, or all configurations if not passed [optional]
    #@param force Force re-read configuration items from file [optional]
    def __get_config(self,key=None,force=False):
        #Determines whether to read the configuration from a file
        if not self.__config or force:
            config_file = self.__plugin_path + 'config.json'
            if not os.path.exists(config_file): return None
            f_body = public.ReadFile(config_file)
            if not f_body: return None
            self.__config = json.loads(f_body)

        #Take the specified configuration item
        if key:
            if key in self.__config: return self.__config[key]
            return None
        return self.__config

    #Set configuration items (the configuration file of the plugin itself)
    #@param key Configuration items to be modified or added [optional]
    #@param value Configuration value [optional]
    def __set_config(self,key=None,value=None):
        #Whether you need to initialize configuration items
        if not self.__config: self.__config = {}

        #Do you need to set configuration values
        if key:
            self.__config[key] = value

        #Write to configuration file
        config_file = self.__plugin_path + 'config.json'
        public.WriteFile(config_file,json.dumps(self.__config))
        return True

