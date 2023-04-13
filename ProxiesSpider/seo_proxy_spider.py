# _*_ coding : utf-8 _*_
# @Time : 2023/3/13 16:32
# @Author : jiang
# @File : seo_proxy_spider
# Project : FreeIPProxyGettingPro


from tools import *
from ProxiesSpider.spider import Spider
from wrappers import req_respose_none_wrapper


class SpiderSeo(Spider):

    def __init__(self, *args, **kwargs):

        url = 'https://proxy.seofangfa.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(url=url, headers=headers)

    def pre_parse(self):
        self.parse_urls = [
            'https://proxy.seofangfa.com/'
        ]

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//table[@class="table"]/tbody/tr')
        proxies = []
        for proxy_obj in proxies_obj:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[4]/text()')[0].strip(),
                'day': proxy_obj.xpath('./td[5]/text()')[0].strip().split(' ')[0],
            }
            proxies.append(dic_)
        return proxies

    def get_all_proxies(self):
        """
        获取所有 proxies
        """
        self.pre_parse()

        for parse_url in self.parse_urls:
            self.update_attrs(url=parse_url)
            self.update_response()

            proxies = self.parse()
            self.all_proxies += proxies

        return self.all_proxies


if __name__ == '__main__':

    spider_seo = SpiderSeo()
    spider_seo.run()
