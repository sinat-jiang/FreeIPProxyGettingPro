# _*_ coding : utf-8 _*_

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

    def add_proxy(self, proxy):
        proxy_str = "{}:{}".format(proxy['ip'], proxy['port'])
        if proxy_str not in self.proxies_set:
            self.proxies_set.add(proxy_str)
            self.proxies.append(proxy)

    def add_proxies(self, proxies):
        for proxy in tqdm(proxies):
            proxy_str = "{}:{}".format(proxy['ip'], proxy['port'])
            if proxy_str not in self.proxies_set:
                self.proxies_set.add(proxy_str)
                self.proxies.append(proxy)

    def get_useful_proxy(self):
        for i in tqdm(range(len(self.proxies))):
            proxy = self.get_proxy()
            if check_proxy_900cha(proxy['ip'], proxy['port']):
                return proxy
        print('无可用 proxy ~')
        return None
