# _*_ coding : utf-8 _*_
# @Time : 2023/3/14 16:49
# @Author : jiang
# @File : zdaye_proxy_spider
# Project : FreeIPProxyGettingPro

from lxml import etree
from ProxiesSpider.spider import Spider
import time
import sys
from wrappers import req_respose_none_wrapper


class SpiderZdaye(Spider):
    """
    zdaye 自有证书，需要设置 verify=False
    """
    def __init__(self, *args, **kwargs):

        url = 'https://www.zdaye.com/dayProxy.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        # zdaye 封禁代理比较频繁，需要使用代理去访问资源
        super().__init__(url=url, headers=headers, verify=False)

        # self.session = None

    def pre_parse(self):
        """
        识别当天代理页面
        :return:
        """
        # 资源整合页请求
        self.update_response()

        self.response.encoding = 'utf-8'
        content = self.response.text
        tree = etree.HTML(content)
        proxy_page_info_obj = tree.xpath('//div[@class="thread_content"]/h3/a')
        for ppio in proxy_page_info_obj:
            title = ppio.xpath('./text()')[0].strip().split(' ')[0]
            parse_day = title.split('日')[0].replace('年', '-').replace('月', '-')
            if [int(x) for x in parse_day.split('-')] == [int(x) for x in self.day.split('-')]:
                self.parse_urls.append(ppio.xpath('./@href')[0])
            else:
                break
        return self.parse_urls

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        self.response.encoding = 'utf-8'  # 注意该页面的中文编码
        content = self.response.text
        tree = etree.HTML(content)
        proxies_obj = tree.xpath('//table[@id="ipc"]/tbody/tr')
        proxies = []
        for proxy_obj in proxies_obj:
            dic_ = {
                'ip': proxy_obj.xpath('./td[1]/text()')[0].strip().replace('"', '').strip(),
                'port': proxy_obj.xpath('./td[2]/text()')[0].strip().replace('"', '').strip(),
                'type': proxy_obj.xpath('./td[3]/text()')[0].strip(),
                'position': proxy_obj.xpath('./td[5]/text()')[0].strip().split(' ')[0],
                'isp': proxy_obj.xpath('./td[5]/text()')[0].strip().split(' ')[1] if len(proxy_obj.xpath('./td[5]/text()')[0].strip().split(' ')) > 1 else None,
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
        print(self.parse_urls)

        # for debug
        req_successed_urls = []
        req_failed_urls = []

        # 2 对每个 proxy 信息页的资源进行解析
        for parse_url in self.parse_urls:
            parse_url = 'https://www.zdaye.com' + parse_url
            print('parse_url:', parse_url)

            self.update_attrs(url=parse_url)
            self.update_response()

            # for debug
            print('-' * 90)
            print(self.response.status_code)
            if self.response.status_code == 200:
                req_successed_urls.append(parse_url)
            else:
                req_failed_urls.append(parse_url)
            self.response.encoding = 'utf-8'
            # print(self.response.text)
            with open('zday.html', 'w', encoding='utf-8') as f:
                f.write(self.response.text)
                print('save the page screen shot')
            print('-' * 90)

            # 3 获取资源页所有的 proxy（这里的逻辑需要根据资源页是否只有当天数据，还是所有天的数据混合在一起，来确定自己的编写逻辑）
            # 两种遍历逻辑：1）根据下一页遍历；2）获取总页数然后循环请求；
            # 两种中断逻辑：1）无需中断；2）列表中包含非当天数据，需中断处理；
            # zdaye 资源页只有当天数据，所以无需在采集过程中判断
            # 初始时指向首页
            while True:
                time.sleep(3)   # 间隔爬取
                proxies = self.parse()
                if len(proxies) == 0:
                    break

                self.all_proxies += proxies

                # etree xpath 获取不到，会返回空，而不是报错
                next_tag = etree.HTML(self.response.text).xpath('//a[@title="下一页"]/@href')
                if len(next_tag) == 0:
                    break
                else:
                    next_page = 'https://www.zdaye.com' + etree.HTML(self.response.text).xpath('//a[@title="下一页"]/@href')[0]
                    self.update_attrs(url=next_page)
                    self.update_response()

                    # for debug
                    if self.response.status_code == 200:
                        req_successed_urls.append(next_page)
                    else:
                        req_failed_urls.append(next_page)

        # for debug
        if len(req_failed_urls) > 0:
            print('+' * 90)
            print('successed urls:', req_successed_urls)
            print('failed urls:', req_failed_urls)
            print('+' * 90)
        return self.all_proxies


if __name__ == '__main__':

    # proxy = get_free_proxy()
    # print('使用代理：', proxy)
    #
    # if proxy is None:
    #     proxies = None
    # else:
    #     proxies = {
    #         'http': '{}:{}'.format(proxy['ip'], proxy['port']),
    #         'https': '{}:{}'.format(proxy['ip'], proxy['port']),
    #     }

    # proxies = None

    # zdaye 每天最后的更新时间是 21 点

    # session = requests.Session()
    # session.trust_env = False
    # response = session.get(url)
    # print(response.status_code)

    # spider_zdy = SpiderZdaye(proxies=proxies)
    # spider_zdy.run()

    spider_zdy = SpiderZdaye()
    spider_zdy.run()
