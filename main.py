# _*_ coding : utf-8 _*_

"""
项目入口
逻辑：
    1. 先开启全局代理持有器
    2. 进行存量数据验证
    3. 启动配置过的爬虫
    4. 保存
"""

from proxy_manager import ProxyManager
from chain_of_spiders_cfg import *


if __name__ == '__main__':
    # global proxy manager
    proxy_manager = ProxyManager()
    print('ini useful proxy num:', proxy_manager.get_proxy_num())

    # 按序执行爬虫链
    spiders = [spider() for spider in proxy_spiders]
    for i, spider in enumerate(spiders):
        print('=' * 160)
        spider.run()
        proxy_manager.add_proxies(spider.all_proxies_filter)
        if i == 0:
            print('after stock proxies loading, the useful proxy num:', proxy_manager.get_proxy_num())

    print("proxy_manager's proxy num:", proxy_manager.get_proxy_num())
