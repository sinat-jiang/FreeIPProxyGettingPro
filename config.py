# _*_ coding : utf-8 _*_

"""
配置文件
"""
import os

RETRY_LIMIT = 4     # 爬取失败时的重试次数

# 可用 ip 存储文件地址
here_cfg = os.path.dirname(__file__)
useful_ip_file_path = os.path.join(here_cfg, 'proxies_spider_results')
# 可用 ip 存储文件名称
useful_ip_file_name = 'useful_proxies_spiding.txt'

