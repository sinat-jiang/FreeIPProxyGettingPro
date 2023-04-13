# _*_ coding : utf-8 _*_
# @Time : 2023/3/13 17:12
# @Author : jiang
# @File : main
# Project : FreeIPProxyGettingPro

"""
项目入口
逻辑：
1. 先开启全局代理持有器
2. 进行存量数据验证
3. 启动配置过的爬虫
4. 保存
"""

from proxy_manager import ProxyManager
from config import *
from ProxiesSpider.stock_proxy_spider import SpiderStock
from chain_of_spiders_cfg import *
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm


if __name__ == '__main__':
    # global proxy manager
    proxy_manager = ProxyManager()
    print('ini useful proxy num:', proxy_manager.get_proxy_num())

    # 1 存量数据验证
    stock_spider = SpiderStock()
    stock_spider.run()
    proxy_manager.add_proxies(stock_spider.all_proxies_filter)
    print('after stock proxies loading, the useful proxy num:', proxy_manager.get_proxy_num())

    # 2 启动配置过的爬虫
    spiders = [spider() for spider in proxy_spiders]

    # 2.1 多进程：为每个 spider 开启一个单独的进程，并行爬取
    # pool = ProcessPoolExecutor(max_workers=len(spiders))
    # all_task = [pool.submit(spider.run) for spider in spiders]
    # for future in as_completed(all_task):
    #     all_proxies_filter = future.result()
    #     proxy_manager.add_proxies(all_proxies_filter)
    #
    # print("proxy_manager's proxy num:", proxy_manager.get_proxy_num())

    # 2.2 单进程
    for spider in spiders:
        print('=' * 160)
        spider.run()
        proxy_manager.add_proxies(spider.all_proxies_filter)

    print("proxy_manager's proxy num:", proxy_manager.get_proxy_num())
