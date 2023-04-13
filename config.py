# _*_ coding : utf-8 _*_
# @Time : 2023/3/13 17:10
# @Author : jiang
# @File : config
# Project : FreeIPProxyGettingPro

import os

RETRY_LIMIT = 4     # 爬取失败时的重试次数

# 可用 ip 存储文件地址
useful_ip_file_path = os.path.join('D:/D0/coding/workspaceforC_ide/PycharmCommunity2019/python_spider/FreeIPProxyGettingPro', 'proxies_spider_results')
# 可用 ip 存储文件名称
useful_ip_file_name = 'useful_proxies_spiding.txt'

# 所有资源爬取后汇总的 proxy 资源
# useful_ip_file_name_latest = 'useful_proxies_latest.txt'
