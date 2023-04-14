# _*_ coding : utf-8 _*_
from tqdm import tqdm
from lxml import etree
from ProxiesSpider.spider import Spider
import time
import sys
from wrappers import req_respose_none_wrapper


class SpiderYun(Spider):

    def __init__(self, *args, **kwargs):

        url = 'http://www.ip3366.net/free/?stype=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(url=url, headers=headers)

    def pre_parse(self):
        """
        识别当天代理页面
        :return:
        """
        self.parse_urls = [
            'http://www.ip3366.net/free/?stype=2',      # 高匿代理
            'http://www.ip3366.net/free/?stype=1'       # 普通代理
        ]
        return self.parse_urls

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        self.response.encoding = 'gb2312'  # 注意该页面的中文编码
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        proxies = []
        for proxy_obj in proxies_obj:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip(),
                'type': proxy_obj.xpath('./td[4]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[5]/text()')[0].strip(),
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
            self.update_attrs(url=parse_url)
            self.update_response()

            # 3 获取资源页所有的 proxy
            total_pages = int(etree.HTML(self.response.text).xpath('//div[@id="listnav"]/ul/strong/text()')[0].replace('/', ''))
            for i in tqdm(range(total_pages), file=sys.stdout, desc='[{}] crawling all pages...'.format(self.__class__.__name__)):
                time.sleep(2)
                if i == 0:
                    self.all_proxies += self.parse()
                else:
                    url_new = parse_url.split('&')[0] + '&page={}'.format(i+1)
                    self.update_attrs(url=url_new)
                    self.update_response()
                    self.all_proxies += self.parse()

            return self.all_proxies


if __name__ == '__main__':
    spider_yun = SpiderYun()
    spider_yun.run()
