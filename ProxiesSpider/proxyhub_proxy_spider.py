# _*_ coding : utf-8 _*_
import requests
from tqdm import tqdm
from lxml import etree
from ProxiesSpider.spider import Spider
import time
import sys
from wrappers import req_respose_none_wrapper


class SpiderPH(Spider):

    def __init__(self, *args, **kwargs):

        kwargs['url'] = 'https://proxyhub.me/en/all-http-proxy-list.html'
        kwargs['headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(**kwargs)

    def pre_parse(self):
        """
        识别当天代理页面
        :return:
        """
        self.parse_urls = [
            'https://proxyhub.me/zh/all-http-proxy-list.html',
            'https://proxyhub.me/zh/all-https-proxy-list.html',
        ]
        return self.parse_urls

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//table/tbody/tr')
        proxies = []
        for proxy_obj in proxies_obj:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip(),
                'type': proxy_obj.xpath('./td[3]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[5]/a/text()')[0].strip(),
                'day': self.day
            }
            proxies.append(dic_)
        return proxies

    def get_all_proxies(self):
        """
        获取所有 proxies
        """
        # 1 先获取所有待采集的 proxy list 页
        self.pre_parse()

        # 2 对每个 proxy 信息页的资源进行解析
        for parse_url in self.parse_urls:
            # 3 获取资源页所有的 proxy
            self.update_attrs(url=parse_url)
            self.update_response()

            # 获取总页数
            tree = etree.HTML(self.response.text)
            total_page = int(tree.xpath('//span[@class="page-link"]/@page')[-1])

            for i in tqdm(range(total_page), file=sys.stdout, desc='[{}] crawling all pages...'.format(self.__class__.__name__)):
                # 资源页首页无需重新请求
                if i == 0:
                    self.all_proxies += self.parse()
                else:
                    page_headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'cache-control': 'max-age=0',
                        'cookie': 'page={}; anonymity=all'.format(i + 1),
                        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': 'Windows',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                    }
                    try:
                        self.update_attrs(headers=page_headers)
                        self.update_response()
                    except Exception as e:
                        print('\033[1;31m{}\033[0m'.format(
                            '停一下停一下~'
                        ))
                        time.sleep(16)
                        self.update_attrs(headers=page_headers)
                        self.update_response()
                    self.all_proxies += self.parse()

            return self.all_proxies


if __name__ == '__main__':
    spider_ph = SpiderPH()
    spider_ph.run()