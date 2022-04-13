#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import Aria2Py as a2p
import json, requests, os,re,urllib
from requests import get
from time import sleep
from time import ctime


# In[ ]:


# 爬取网页或者图片的内容或者二进制信息
def download(url,Type):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}
    content = ''
    t = 0
    while t < 3:
        try:
            content = get(url,headers = headers,timeout=20,proxies=proxies)
            if Type == '':
                pass
            else:
                print('获取',Type,'成功')
                
            return content
            t = 4
        except Exception as e:
            t = t + 1
            print('错误，',e)
            content='no picture'
    return content


# In[ ]:


#爬取网页的爬虫
def get_page_info():
    
    status = True
    urls=[]
    
    log = open('/tmp/downloadlog','a')
    log.write('\n' + '\t' + str(ctime()) + '\n')
    log.close
    
    while status:
        # 读取每页的页面链接
        url = input('添加网址链接,exit终止输入：\n')
        if url == 'exit':
            status = 0
        else:
            urls.append(url)
            log = open('/tmp/downloadlog','a')
            log.write(url+'\n')
            log.close
        # 扫描该分页下该标题内的图片信息
        
        
        
    for url in urls:
        pics = []
        mds = []
        magnet = ''
        try:
            text = download(url,'').text
            magnet = re.findall("magnet\:\?xt=.*?<",text)[0][:-1]
            jpg = re.findall("(https?:\/\/.*?jpg)",text)
            png = re.findall("(https?:\/\/.*?png)",text)
            jpeg = re.findall("(https?:\/\/.*?jpeg)",text)
            pic_urls = pics + jpg + png + jpeg
            title_1 = re.findall("""<meta name="keywords" content.*>""",text)[0].replace("""<meta name="keywords" content=""","")
            title = re.findall('''\".*\"''',title_1)[0].replace('"','')
            print("\n"+"#####"+title+"#####")
            print(magnet)
            
            for pic in pic_urls:
                if pic in pics:
                    pass
                else:
                    pics.append(pic)
                    
        except Exception as e:
            
            print('发生错误，请确认是否输入正确网页，刚刚记录的网址在/tmp/downloadlog可找到。或到GitHub提交以下错误：\n')
            print(e)
                
                
            #print(pics)
                
        i = 0
        print('共',len(pics),'图')
        for pic in pics:
            i = i + 1
            file_path = path + "/" + title + "/" + str(i) + '.jpg'
            ndir = urllib.parse.quote(file_path)
            md = "\n![](" + ndir  + ")"
            mds.append(md)
            #print ("getting page ",head)
            picture = download(pic,file_path)
            if not os.path.exists(str(path)):
                os.makedirs(str(path))   
                #创建页文件夹下的分文件夹
            if not os.path.exists((path) + "/" + title):
                os.makedirs((path) + "/" +  title)
            with open(file_path, 'wb') as file:
                try:
                    file.write(picture.content)
                except:
                    print('pic error')

            
        print('adding file')
        try:
            client.add_uri(magnet,path + "/" + title)
            creat_file(title,magnet,path,mds)
            
        except:
            pass


# In[ ]:


#根据爬取的图片信息创建markdown文件和php文件
def creat_file(title,magnet,path,mds):
    if not os.path.exists(str(path)):
        os.makedirs(str(path))   
        #创建页文件夹下的分文件夹
    if not os.path.exists((path) + "/" + title):
        os.makedirs((path) + "/" +  title)
        
    index = title + """\n bt: """ 
    index = index + magnet + '\n'
    for md in mds:
        index = index + md

    index_file = path + '/' + title + "/" + "README.md"
    
    with open(index_file,'w',encoding = 'utf-8') as w_file:
        for each_line in index:
            w_file.write(each_line)
            
            
            
    # Creat php web page
    php_index = """ <?php
    $folder = "./";   // 文件夹路径
    $files = array();
   $handle = opendir($folder);  // 遍历文件夹
    while(false!==($file=readdir($handle))){
        if($file!='.' && $file!='..'){
  $hz=strstr($file,".");
       if($hz==".gif" or $hz==".jpg" or $hz==".JPG"or $hz==".JPEG"or 
       $hz==".PNG"or $hz==".png"or $hz==".GIF") 
 {$files[] = $file; }
         }
      }
    if($files){
        foreach($files as $k=>$v){
            echo '<img widht=auto  src="'.$v.'">';  // 循环显示
        }
    }
  ?>
    """
    php_index_file = path + '/' + title + "/" + "index.php"
    with open(php_index_file,'w',encoding = 'utf-8') as w_file:
        
        w_file.write(php_index)


# In[ ]:


#检查依赖
def checke_aria_rclone():
    from os import popen
    ariaStatus = popen('aria2c -v').readline()
    if ariaStatus:
        pass
    else:
        ariaStatus = ('未安装Aria2')
    rcloneStatus = popen('rclone --version').readline()
    if rcloneStatus:
        pass
    else:
        rcloneStatus = ('未安装rclone')
    result = '\t' + ariaStatus + '\t' + rcloneStatus
    return result


# In[ ]:


def tell_active():
    downloads={}
    active = client.tell_active()
    for i in active:
        completed_length = i['completedLength']
        total_length = i['totalLength']
        downloadDir = i['dir']
        gid = i['gid']
     
        if 'bittorrent' in i.keys():
            try:
                file = downloadDir + "/" + i['bittorrent']['info']['name']
            except:
                file = "正在获取种子" +  downloadDir + "/"  + i['dir']
        else:
            file = i['files'][0]['path']
            
        if total_length == completed_length:
             if (int(completed_length) > 536870912):
                    print('@',file,'download complet')
                    downloads[downloadDir]=gid
                    
        else: 
            percent = (int(completed_length)/int(total_length)) * 100
            print( int(percent),'%',file)
        
    return downloads


# In[ ]:


#主界面
def menu(path):
    dependens = checke_aria_rclone()
    print('''-----------下片机------------''')
    print('''- 1. 爬取网址里的magnet链接和图片''')
    print('''- 2. 检测下载状态''')
    print('''- 3. 监测下载状态并使用rclone上传已完成的bt任务''')
    print('''- 4. 添加正常下载链接''')
    if '未' in dependens:
        print('''- 5. 安装Aria2Dash与rclone''')
    else:
        pass
    print('''- 6. 卸载''')
    print("- 7. 设置网页解析代理")
    print('''- 0. 退出''')
    print('''--------------------------------''')
    print(checke_aria_rclone())
    print('''--------------------------------''')
    
    
    
    opt = str(input ('输入选项：'))
    if opt == '1':
        get_page_info()
    elif opt == '2':
        try:
            tell_active()
        except Exception as e:
            print (e)
            print('无法连接Aria2服务，请确认已正确启动并填写rpc')
            #return 0
    elif opt == '3':
        
        print(str(os.popen('rclone listremotes').read()).replace(':',''))
        rclone = input('输入选择使用的rclone remote： ')
        
        count = 0
        while True:
            os.system('date')
            try:
                file = tell_active()
            except Exception as e:
                print (e)
                print('无法连接Aria2服务，请确认已正确启动并填写rpc')
                return 0
            try:
                for key in file.keys():
                    dir = key.strip()
                    if ' ' in dir:
                        dir = dir.replace(' ','''\ ''')
                
                    if dir[0] == '/':
                        pass
                    else:
                        dir = '/' + dir
                    print('---------------------------------------------------')
                    print('Preparing to upload ',dir)
                
                
                    
                    #cmd0 = 'rclone copy '  + dir + ' gdrive:' + dir + ' -P'
                    print('uploading...')
                    cmd = 'rclone move '  + dir +  ' ' + rclone.strip() + ':' + dir + ' -P'
                    sleep(30)
                    #os.system(cmd0)
                    print(cmd)
                    #input('ss')
                    os.system(cmd)
                    log = open('/tmp/uploadlog','a')
                    log.write(str(ctime()) + dir + '\n')
                    log.close
                
                
                
                
                    client.remove(file[key])
                    #os.system(cmd2)
                
                sleep(10)
                count = count + 1
                if count == 10:
                    count = 0
                    print("sync between clouds")
                    #os.system("""rclone sync gdrive:/ bcgdrive:/ -P""")
                    #os.system("""rclone copy gdrive:/ hell:/ -P""")
            except Exception as e:
                print (e)
                
                print('---------------------------------------------------')
                sleep(30)
                
    elif opt == '4':
        while True:
            path = input('输入0直接退出,否则输入保存路径，留空为默认或者不变:\n')
            #folder = input('输入:\n')
            if path == '0':
                return 1
        
            url = input('input url/magnet:\n')
            client.add_uri(uri=url,position=path)
            
    elif opt == '5':
        o = input('将运行快速部署Aria2的脚本。具有剩余容量显示监控及显示功能。本脚本会一同安装文件管理器，按y确认安装，n取消。详细内容看以下链接：\n https://github.com/Masterchiefm/Aria2Dash \n 输入选择：')
        if o == 'y':
            print('请稍等...')
            os.system('bash <(curl -s -L https://github.com/Masterchiefm/Aria2Dash/raw/master/Aria2Dash.sh)')
            os.system('apt instal rclone -y')
        else:
            print('已取消')
            
    elif opt == '6':
        os.system('sudo rm -rf /usr/bin/aria2py')
        os.system('sudo rm -rf /usr/bin/aria2_py.py')
        print('卸载完成，无残留')
        
    elif opt == '0':
        return 0 
    
    elif opt == "7":
        global proxies
        proxy = input("输入http proxy地址，如输入 127.0.0.1:10809")
        proxy_url = "http://" + proxy.strip()
        proxy_url2 = "https://" + proxy.strip()
        proxies = {
            'http': proxy_url,
            'https': proxy_url2,
                }
    else:
        print('输入有误')
        return 1
    return 1


# In[ ]:


if "__main__" in __name__:
    add = input("输入Aria2地址，例如http://127.0.0.1\n")
    port = input("输入端口，默认6800\n")
    token = input("输入密码，默认无\n")
    global path
    path = input("输入下载保存路径，不填为配置文件默认。\n")
    if path == '':
        print('未输入保存路径，将存于配置文件定义的目录')
        path = ''
    else:
        if path[0]=='/':
            pass
        else:
            path='/'+ path
            
        if path[-1]=='/':
            path = path[:-1]
    print(path)
        
    global client
    client = a2p.Aria2Client()
    client.set_server(server_add=add,server_port=port,token=token)
    
    global proxies
    proxies = {
      'http': '',
      'https': '',
        }
    
    a = 1
    while a:
        a = menu(path)


# In[ ]:




