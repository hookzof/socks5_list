#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Mar 17 16:39:04 CST 2021
# AUTHOR: Mr.Frame 
# Description:
#      自动获取http代理，并添加到proxychains.conf中
#Usage:
#      python3 gethttp.py  [/path/to/proxychains.conf]

import requests
from bs4 import BeautifulSoup
from lxml import etree
import json



def get_http(proxychains_path):
    """
    get socks from http://www.xiladaili.com/gaoni/
    proxychains_path: str -> the path of proxycahins-ng configuation file.
    ***suggestion:   enable  round_robin_chain****
    #strict_chain
    #dynamic_chain
    #round_robin_chain
    random_chain
    chain_len = 2
    """

    proxychains_file = proxychains_path
    
    url="http://www.xiladaili.com/gaoni/"
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }

    try:
        response = requests.get(url=url,headers=headers,timeout=2)
    except Exception as e:
        print("\033[31m[x]Connection failed\033[0m")
        print(e.__str__())
        exit()


    # with open('index.html','r') as f:
    #     response_text=f.read()
    
    ip_port_list=[]
    socks_list="\n# socks5 list from  http://www.xiladaili.com/gaoni\n"
    
    if response.status_code == 200 :
        bs=BeautifulSoup(response.text,'html.parser')

        for ip_port in bs.find_all("td"):
            ip_port_list.append(ip_port.text.replace(":","\t"))

    for i in range(0,ip_port_list.__len__()):
        if i%8 == 0:
            socks_list += "http" +"\t" + ip_port_list[i] +"\n"

    # with open("/usr/local/etc/proxychains.conf",'a+') as f:
    with open(proxychains_file,"a+") as f:
        f.write(socks_list)
    
     
        

        










        

        

        
    
        




if __name__ == '__main__':
    import sys
    if sys.argv.__len__() == 1:
        get_http("/usr/local/etc/proxychains.conf")
    else:
        get_http(sys.argv[1])
    
