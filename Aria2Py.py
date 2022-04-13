#!/usr/bin/env python
# coding: utf-8
import os
import xmlrpc.client as xmlrpc_client
class Aria2Client:
    """Default server address is http://127.0.0.1,
    default port is 6800, default token is empty"""
    #print("ss")
    def __init__(self):
        #print("初始化信息")
        self.server_add = "http://127.0.0.1"
        self.server_port = "6800"
        rpc = "rpc"
        self.server_url = self.server_add + ":" + self.server_port + "/" + rpc
        self.server = xmlrpc_client.ServerProxy(self.server_url)
        self.token = ''

    
    
    def set_server(self,server_add = '',server_port = '6800', token = ''):
        """set server info. If you leave the parameters blank, the server info will be unchanged or remained default."""
        #server信息更改
        rpc = "rpc"
        
        #更改服务器地址
        if server_add == '':
            pass
        else:
            if server_add[-1] == "/":
                server_add = server_add[:-1]
            self.server_add = server_add
        
        #更改端口
        if server_port == '':
            pass
        else:
            self.server_port = str(server_port)
            

        
        if token == '':
            pass
        else:
            self.token = str(token)
       
    
        self.server_url = self.server_add + ":" + self.server_port + "/" + rpc
        self.server = xmlrpc_client.ServerProxy(self.server_url)
    
    
    def get_version(self):
        try:
            version = self.server.aria2.getVersion("token:%s"%self.token)
            return str(version)
        except Exception as e:
            return str(e)
        
    def check_connection(self):
        try:
            version = self.get_version()
            if "Unauthorized" in version:
                return "Unauthorized"
            elif "version" in version:
                return "Authorized"
            else:
                return version
        except Exception as e:
            return e
        
        
    def add_uri(self,uri,dir='',option = {}):
        """provide the download link (or link list) to donload. Options is the same as --inputFile option."""
        
        # convert uri to list.
        if type(uri) == type([1]):
            uri_list = uri
        else:
            uri_list = [uri]
        
        if dir != "":
            download_dir = dict(dir=dir)
            option.update(download_dir)
        try:    
            pid = self.server.aria2.addUri("token:%s"%self.token,uri_list,option)
            return pid
        except Exception as e:
            return e
            
            
    def add_Torrent(self,torrent_dir,dir='',uri=[],option={}):
        '''add local torrent file to download.uris is an array of URIs (string). uris is used for Web-seeding.
        For single file torrents, the URI can be a complete URI pointing to the resource; 
        if URI ends with /, name in torrent file is added. For multi-file torrents, name and path in torrent are added to form a URI for each file.
        options is a struct and its members are pairs of option name and value.'''
        
        torrent = xmlrpc_client.Binary(open(torrent_dir, mode='rb').read())
        if dir != "":
            download_dir = dict(dir=dir)
            option.update(download_dir)
        
        try:    
            pid = self.server.aria2.addTorrent("token:%s"%self.token,torrent,uri,option)
            return pid
        except Exception as e:
            return e
    
    def remove(self,gid):
        """remove a downloading or waiting, paused job."""
        try:
            result = self.server.aria2.remove("token:%s"%self.token,gid)
            return result
        except Exception as e:
            return e
        
        
    def force_remove(self,gid):
        """This method removes the download denoted by gid. This method behaves just like aria2.remove()
        except that this method removes the download without performing any actions which take time, 
        such as contacting BitTorrent trackers to unregister the download first."""
        
        try:
            result = self.server.aria2.forceRemove("token:%s"%self.token,gid)
            return result
        except Exception as e:
            return e
        
    def pause(self,gid = ''):
        """if gid is empty, this method will pause all."""
        if gid == '':
            try:
                result = self.server.aria2.pauseAll("token:%s"%self.token)
                return result
            except Exception as e:
                return e
        
        try:
            result = self.server.aria2.pause("token:%s"%self.token,gid)
            return result
        except Exception as e:
            return e
    
    def unpause(self,gid = ''):
        """if gid is empty, this method will unpause all."""
        if gid == '':
            try:
                result = self.server.aria2.unpauseAll("token:%s"%self.token)
                return result
            except Exception as e:
                return e
        
        try:
            result = self.server.aria2.unpause("token:%s"%self.token,gid)
            return result
        except Exception as e:
            return e
    
    
    def tell_status(self,gid = '',keys = []):
        """provide a specific gid to get status. you can specific the outputs by giving keys(list), 
        or you will get all status infomation. """
        if type(keys) == type('string'):
            keys = [keys]
        try:
            status = self.server.aria2.tellStatus("token:%s"%self.token,gid,keys)
            return status
        except Exception as e:
            return e
        
    def tell_active(self,keys = []):
        """Show what is currently downloading. you can specific the outputs by giving keys(list), 
        or you will get all status infomation.  """
        if type(keys) == type('string'):
            keys = [keys]
        try:
            active_jobs = self.server.aria2.tellActive("token:%s"%self.token,keys)
            return active_jobs
        except Exception as e:
            return e
        
    def tell_waiting(self,offset = 0, num = 50, keys = []):
        """This method returns a list of waiting downloads, including paused ones.
        offset is an integer and specifies the offset from the download waiting at the front.
        num is an integer and specifies the max. number of downloads to be returned. 
        For the keys parameter, please refer to the aria2.tellStatus() method."""
        if type(keys) == type('string'):
            keys = [keys]
        try:
            waiting_jobs = self.server.aria2.tellWaiting("token:%s"%self.token,offset,num,keys)
            return waiting_jobs
        except Exception as e:
            return e
        
    def tell_stopped(self,offset = 0, num = 50, keys = []):
        """This method returns a list of waiting downloads, including paused ones.
        offset is an integer and specifies the offset from the download waiting at the front.
        num is an integer and specifies the max. number of downloads to be returned. 
        For the keys parameter, please refer to the aria2.tellStatus() method."""
        if type(keys) == type('string'):
            keys = [keys]
        try:
            stopped_jobs = self.server.aria2.tellStopped("token:%s"%self.token,offset,num,keys)
            return stopped_jobs
        except Exception as e:
            return e
        
    def list_methods(self):
        try:
            methods = self.server.system.listMethods("token:%s"%self.token)
            return methods
        except Exception as e:
            return e
        
    def list_notifications(self):
        try:
            notifications = self.server.system.listNotifications()
            return notifications
        except Exception as e:
            return e
        
    def get_files(self,gid):
        """This method returns the file list of the download denoted by gid (string). 
        The response is an array of structs."""
        try:
            files = self.server.aria2.getFiles("token:%s"%self.token,gid)
            return files
        except Exception as e:
            return e
        
    def multicall(self,method):
        """This methods encapsulates multiple method calls in a single request. 
        methods is an array of structs. The structs contain two keys: methodName and params. 
        methodName is the method name to call and params is array containing parameters to the method call.
        This method returns an array of responses. 
        The elements will be either a one-item array containing the return value of the method call or a struct
        of fault element if an encapsulated method call fails."""
        try:
            mc = xmlrpc_client.MultiCall(self.server)
            return mc
        except Exception as e:
            return e
    
    def get_session_info(self):
        try:
            info = self.server.aria2.getSessionInfo("token:%s"%self.token)
            return info
        except Exception as e:
            return e
        
    def remove_stopped(self,gid = ''):
        """If gid is not specific, this method will remove all stopped jobs."""
        if gid == '':
            try:
                result = self.server.aria2.purgeDownloadResult("token:%s"%self.token)
                return result
            except Exception as e:
                return e
        
        else:
            try:
                result = self.server.aria2.removeDownloadResult("token:%s"%self.token,gid)
                return result
            except Exception as e:
                return e
            
    def get_option(self,gid):
        """return the options of a specific job you can modify."""
        try:
            option = self.server.aria2.getOption("token:%s"%self.token,gid)
            return option
        except Exception as e:
                return e
            
            
    def change_option(self,gid,options):
        """This method changes options of the download denoted by gid (string) dynamically.
        options is a struct. 
        option parameter example:  {'max-download-limit':'20K'}  """
        try:
            option = self.server.aria2.changeOption("token:%s"%self.token,gid,options)
            return option
        except Exception as e:
                return e
            
            
    def get_global_option(self,gid):
        """return the global options you can modify."""
        try:
            option = self.server.aria2.getGlobalOption("token:%s"%self.token,gid)
            return option
        except Exception as e:
                return e
            
    def change_global_option(self,options):
        """This method changes options of the download denoted by gid (string) dynamically.
        options is a struct. 
        option parameter example:  {'max-overall-download-limit':'0'} """
        try:
            option = self.server.aria2.changeGlobalOption("token:%s"%self.token,options)
            return option
        except Exception as e:
                return e
    
    
    def get_global_status(self):
        """speed (byte/sec)."""
        try:
            status = self.server.aria2.getGlobalStat("token:%s"%self.token)
            return status
        except Exception as e:
            return e
        

    
    def save_session(self):
        """This method saves the current session to a file specified by the --save-session option. 
        This method returns OK if it succeeds."""
        try:
            result = self.server.aria2.saveSession("token:%s"%self.token)
            return result
        except Exception as e:
            return e
    
    def nofification(self,method = '',gid=''):
        """future work.不想做"""
        if method == '':
            methods = []
            result = self.list_notifications()
            for i in result:
                m = i.replace("aria2.","")
                methods.append(m)
            
            return methods
        
        
        
        
        else:
            #未完成。不想做。
            pass  
            


