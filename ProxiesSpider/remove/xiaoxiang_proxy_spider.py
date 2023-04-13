# _*_ coding : utf-8 _*_
# @Time : 2023/3/12 23:56
# @Author : jiang
# @File : xiaoxiang_proxy_spider
# Project : FreeIPProxyGettingPro

"""
小象代理已不再提供免费代理服务 ~
"""

from ProxiesSpider.spider import Spider
import os
from lxml import etree
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from tools import check_proxy_900cha, check_proxy_icanhazip, check_proxy_selfreq
from config import *


class SpiderXiaoXiang(Spider):

    def __init__(self, *args, **kwargs):

        url = 'https://www.xiaoxiangdaili.com/free/list'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(url=url, headers=headers)

        self.next = True
        self.parse_urls = []
        self.all_proxies = []
        self.all_proxies_filter = []

    def pre_parse(self):
        """
        识别当天代理页面
        """
        content = self.response.text
        tree = etree.HTML(content)
        proxy_page_info_obj = tree.xpath('//div[@class="blogTop"]//a')
        for ppio in proxy_page_info_obj:
            title = ppio.xpath('./div[@class="title line_2 fl"]/text()')[0].strip().split(' ')[0]
            if self.day == title.split('日')[0].replace('年', '-').replace('月', '-'):
                self.parse_urls.append('{}{}'.format('https://www.xiaoxiangdaili.com', ppio.xpath('./@href')[0]))
            else:
                break
        print("当天有 {} 份资源~".format(len(self.parse_urls)))

    def parse(self):
        """
        对单个 ip 资源页面进行代理解析
        :return:
        """
        content = self.response.text
        tree = etree.HTML(content)

        proxies_obj = tree.xpath('//div[@class="freeProxyInfo"]/table//tr')
        proxies = []
        for po in proxies_obj:
            dic_ = {
                'ip': po.xpath('./td[1]/text()')[0].strip(),
                'port': po.xpath('./td[2]/text()')[0].strip(),
                'position': po.xpath('./td[3]/text()')[0].strip(),
                'type': po.xpath('./td[4]/text()')[0].strip(),
                'isp': po.xpath('./td[5]/text()')[0].strip(),
                'day': self.day
            }
            proxies.append(dic_)
        return proxies

    def get_all_proxies(self):
        """
        获取所有 proxies
        simple：小象代理不用翻页，所有代理直接在一页全部返回了
        """
        self.pre_parse()

        for parse_url in self.parse_urls:
            # 重新获取代理 ip 页面资源
            self.update_attrs(url=parse_url)
            self.update_response()
            self.all_proxies += self.parse()
        if len(self.all_proxies) == 0:
            print('当天（{}）无新免费代理资源！'.format(spider_xx.day))
        return self.all_proxies


if __name__ == '__main__':

    spider_xx = SpiderXiaoXiang()
    spider_xx.day = '2023-04-10'
    try:
        spider_xx.run()
    except Exception as e:
        print(e)
        print('{} 代理资源不可用~')
