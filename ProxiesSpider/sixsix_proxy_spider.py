# _*_ coding : utf-8 _*_
# @Time : 2023/3/11 23:53
# @Author : jiang
# @File : 66_proxy_spider
# Project : FreeIPProxyGettingPro

from ProxiesSpider.spider import Spider
from lxml import etree
from tqdm import tqdm
import time
import sys
from wrappers import req_respose_none_wrapper


class Spider66(Spider):

    def __init__(self, *args, **kwargs):

        url = 'http://www.66ip.cn/index.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        super().__init__(url=url, headers=headers)

    def pre_parse(self):
        self.parse_urls = [
            'http://www.66ip.cn/index.html'
        ]
        return self.parse_urls

    @req_respose_none_wrapper
    def parse(self):
        """
        解析每一页的代理
        """
        self.response.encoding = 'gb2312'   # 注意该页面的中文编码
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//div[@class="layui-row layui-col-space15"]//table/tr')
        proxies = []
        for proxy_obj in proxies_obj[1:]:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[3]/text()')[0].strip(),
                'type': proxy_obj.xpath('./td[4]/text()')[0].strip(),
                'day': proxy_obj.xpath('./td[5]/text()')[0].strip().replace('年', '-').replace('月', '-').split('日')[0],
            }
            if dic_['day'] != self.day:
                break
            proxies.append(dic_)
        return proxies

    def get_all_proxies(self):
        """
        获取所有 proxies
        """
        # 1 获取 proxy 资源页
        self.pre_parse()

        # 2 解析资源页
        for parse_url in self.parse_urls:
            self.update_attrs(url=parse_url)
            self.update_response()

            pbar = tqdm(file=sys.stdout, desc='[{}] crawling all pages...'.format(self.__class__.__name__))
            while True:
                time.sleep(1)
                proxies = self.parse()
                if len(proxies) == 0:
                    break

                self.all_proxies += proxies

                next_page = 'http://www.66ip.cn' + etree.HTML(self.response.text).xpath('//div[@id="PageList"]/a/@href')[-1]
                self.update_attrs(url=next_page)
                self.update_response()

                pbar.update(1)

            pbar.close()

        return self.all_proxies


if __name__ == '__main__':
    # url
    # url = 'http://www.66ip.cn/index.html'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    # }

    # spider_66 = Spider66()
    # content_66 = spider_66.response.text
    # # print(content_66)
    #
    # all_proxies = spider_66.get_all_proxies()
    # print('爬取代理数：', len(all_proxies))
    #
    # all_proxies_filter = spider_66.filter_all_proxies_mp()
    # print('可用代理数：', len(all_proxies_filter))
    # spider_66.save_to_txt(os.path.join(useful_ip_file_path, useful_ip_file_name), spider_66.all_proxies_filter)

    spider_66 = Spider66()
    spider_66.run()



