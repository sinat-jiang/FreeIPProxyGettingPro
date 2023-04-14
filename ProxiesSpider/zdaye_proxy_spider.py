# _*_ coding : utf-8 _*_
from lxml import etree
from ProxiesSpider.spider import Spider
import time
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

        super().__init__(url=url, headers=headers, verify=False)

    def pre_parse(self):
        """
        代理资源页解析
        :return:
        """
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
        # 1 先获取所有代理详情页的 url
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
            with open('zday.html', 'w', encoding='utf-8') as f:
                f.write(self.response.text)
                print('save the page screen shot')
            print('-' * 90)

            # 3 获取资源页所有的 proxy
            while True:
                time.sleep(3)   # 间隔爬取
                proxies = self.parse()
                if len(proxies) == 0:
                    break

                self.all_proxies += proxies

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
    spider_zdy = SpiderZdaye()
    spider_zdy.run()
