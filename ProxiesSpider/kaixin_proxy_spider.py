# _*_ coding : utf-8 _*_
from tqdm import tqdm
from ProxiesSpider.spider import Spider
import time
from lxml import etree
import sys
from wrappers import req_respose_none_wrapper


class SpiderKaixin(Spider):

    def __init__(self, *args, **kwargs):

        url = 'http://www.kxdaili.com/dailiip.html'
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
            'http://www.kxdaili.com/dailiip/1/1.html',  # 高匿代理
            'http://www.kxdaili.com/dailiip/2/1.html'  # 普通代理
        ]
        return self.parse_urls

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        self.response.encoding = 'utf-8'
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//table[@class="active"]/tbody/tr')
        proxies = []
        for proxy_obj in proxies_obj:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip(),
                'type': proxy_obj.xpath('./td[4]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[6]/text()')[0].strip().split(' ')[0],
                'isp': proxy_obj.xpath('./td[6]/text()')[0].strip().split(' ')[1] if len(proxy_obj.xpath('./td[6]/text()')[0].strip().split(' ')) > 1 else None,
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
            page_num = int(etree.HTML(self.response.text).xpath('//div[@id="listnav"]/ul/li/a/text()')[-1])
            for i in tqdm(range(1, page_num+1), file=sys.stdout, desc='[{}] crawling all pages...'.format(self.__class__.__name__)):
                time.sleep(3)  # 间隔爬取
                url_new = parse_url.split('.html')[0][:-1] + '{}.html'.format(i)
                self.update_attrs(url=url_new)
                self.update_response()
                proxies = self.parse()
                self.all_proxies += proxies

        return self.all_proxies


if __name__ == '__main__':

    spider_kx = SpiderKaixin()
    spider_kx.run()
