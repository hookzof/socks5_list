#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wed Mar 17 16:39:04 CST 2021
# AUTHOR: Mr.Frame 
# Description:
#      自动获取http代理，并添加到proxychains.conf中
#Usage:
#      python3 gethttp.py  [/path/to/proxychains.conf]


import requests
import urllib3
import json


def get_socks5(proxychains_path):
    """
    get socks from http://proxylist.fatezero.org/proxy.list.
    proxychains_path: str -> the path of proxycahins-ng configuation file.
    ***suggestion:   enable  round_robin_chain****
    #strict_chain
    #dynamic_chain
    #round_robin_chain
    random_chain
    chain_len = 2
    """

    proxychains_file = proxychains_path
    
    url="http://proxylist.fatezero.org/proxy.list"
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }

    urllib3.disable_warnings() # 关闭ssl警告
    try:
        response = requests.get(url=url,headers=headers,verify=False,timeout=2)
    except Exception as e:
        print("\033[31m[x]Connection failed\033[0m")
        print(e.__str__())
        exit()

    if response.status_code == 200 :
        proxy_list = response.text.splitlines()
        socks_list="\n\n# socks5 list from  http://proxylist.fatezero.org/proxy.list\n"
        for item in proxy_list:
            item_dict = json.loads(item)
             
            if "http" == item_dict['type'] and "high_anonymous" == item_dict['anonymity']:
                socks_list += item_dict['type'] +"\t" + item_dict['host'] + "\t" + str(item_dict['port'])+"\n"
            print(socks_list)
            
        # with open("/usr/local/etc/proxychains.conf",'a+') as f:
        with open(proxychains_file,"a+") as f:
            f.write(socks_list)


if __name__ == '__main__':
    import sys
    if sys.argv.__len__() == 1:
        get_socks5("/usr/local/etc/proxychains.conf")
    else:
        get_socks5(sys.argv[1])
    
