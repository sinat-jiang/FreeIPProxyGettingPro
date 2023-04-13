# _*_ coding : utf-8 _*_
# @Time : 2023/3/5 22:31
# @Author : jiang
# @File : 89_proxy
# Project : FreeIPProxyGettingPro


import sys
from lxml import etree
from ProxiesSpider.spider import Spider
import time
from tqdm import tqdm
from wrappers import req_respose_none_wrapper


class Spider89(Spider):

    def __init__(self, *args, **kwargs):

        url = 'https://www.89ip.cn/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(url=url, headers=headers)

    @req_respose_none_wrapper
    def parse(self):
        """
        解析获取免费代理
        """
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//tbody/tr')

        proxies = []
        for proxy in proxies_obj:
            dic_ = {
                'ip': proxy.xpath('./td[1]/text()')[0].strip(),
                'port': proxy.xpath('./td[2]/text()')[0].strip(),
                'position': proxy.xpath('./td[3]/text()')[0].strip(),
                'isp': proxy.xpath('./td[4]/text()')[0].strip(),
                'day': self.day
            }
            proxies.append(dic_)
        return proxies

    def get_all_proxies(self):
        """
        获取所有 proxies
        construct：无 pre_parse
        :return:
        """
        # 1 initial request
        self.update_response()

        # 2 crawl all pages
        pbar = tqdm(file=sys.stdout, desc='[{}] crawling all pages...'.format(self.__class__.__name__))
        while True:
            time.sleep(1)
            proxies = self.parse()
            if len(proxies) == 0:
                break

            self.all_proxies += proxies

            next_page = 'https://www.89ip.cn/' + etree.HTML(self.response.text).xpath('//a[@class="layui-laypage-next"]/@href')[0]
            # print(next_page)
            self.update_attrs(url=next_page)
            self.update_response()

            pbar.update(1)
        pbar.close()

        return self.all_proxies


if __name__ == '__main__':
    spider_89 = Spider89()
    spider_89.run()




