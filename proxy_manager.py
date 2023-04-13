# _*_ coding : utf-8 _*_
# @Time : 2023/4/4 17:53
# @Author : jiang
# @File : proxy_manager
# Project : FreeIPProxyGettingPro

"""
代理管理器
"""

import random
from tqdm import tqdm
from tools import check_proxy_900cha


class ProxyManager:

    def __init__(self):
        self.proxies = []
        self.proxies_set = set()

    def get_proxy(self):
        idx = random.randint(0, len(self.proxies)-1)
        return self.proxies[idx]

    def get_proxy_num(self):
        return len(self.proxies)

    def add_proxy(self, ip, port):
        proxy_str = "{}:{}".format(ip, port)
        if proxy_str not in self.proxies_set:
            self.proxies_set.add(proxy_str)
            self.proxies.append({
                'ip': ip,
                'port': port
            })

    def add_proxies(self, proxies):
        for proxy in tqdm(proxies):
            proxy_str = "{}:{}".format(proxy['ip'], proxy['port'])
            if proxy_str not in self.proxies_set:
                self.proxies_set.add(proxy_str)
                self.proxies.append({
                    'ip': proxy['ip'],
                    'port': proxy['port']
                })

    def get_useful_proxy(self):
        for i in tqdm(range(len(self.proxies))):
            index = random.randint(0, len(self.proxies) - 1)
            proxy = self.proxies[index]
            if check_proxy_900cha(proxy['ip'], proxy['port']):
                return proxy
        print('无可用 proxy ~')
        return None
