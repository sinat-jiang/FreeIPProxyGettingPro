# _*_ coding : utf-8 _*_

"""
前一天爬取的存量代理的验证（为保持结构一致性，也封装成 Spider 类形式）
"""

from tqdm import tqdm
from config import *
import json
from tools import get_latest_proxy_file
from concurrent.futures import ProcessPoolExecutor, as_completed
from tools import check_proxy_900cha
import time
import sys


class SpiderStock:

    def __init__(self):
        self.parse_urls = []
        self.all_proxies = []
        self.all_proxies_filter = []

    def pre_parse(self):
        """
        识别当天代理页面
        :return:
        """
        pass

    def parse(self):
        """
        解析代理
        """
        pass

    def get_all_proxies(self):
        """
        获取所有 proxies
        """
        self.all_proxies = get_latest_proxy_file(useful_ip_file_path)
        return self.all_proxies

    def filter_all_proxies_mp(self):
        """
        测试代理 ip 可用性
        多进程处理
        """
        self.all_proxies_filter = dict()

        # process pool
        pool = ProcessPoolExecutor(max_workers=50)
        all_task = [pool.submit(check_proxy_900cha, proxy) for proxy in self.all_proxies]
        for future in tqdm(as_completed(all_task), file=sys.stdout, total=len(all_task), desc='[{}] checking proxies...'.format(self.__class__.__name__)):
            res, proxy = future.result()
            if res:
                self.all_proxies_filter['{}:{}'.format(proxy['ip'], proxy['port'])] = proxy

        self.all_proxies_filter = self.all_proxies_filter.values()
        return self.all_proxies_filter

    def save_to_txt(self, file_name, all_proxies, add_day_tag=True):
        """
        存文件
        """
        day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())).split(' ')[0].strip()
        if not os.path.isdir(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        if add_day_tag:
            file_name = file_name.split('.')[0] + '_{}.'.format(day.replace('-', '_')) + file_name.split('.')[-1]
        with open(file_name, 'w', encoding='utf-8') as f:
            for proxy in all_proxies:
                f.write(json.dumps(proxy, ensure_ascii=False) + '\n')
        # print(f'写入成功：{file_name}')

    def run(self):
        """
        General spider running logic：
            init -> face page url request -> (resource page collect) -> crawl all proxies -> check proxies' usability -> save
        :return:
        """
        self.get_all_proxies()
        self.filter_all_proxies_mp()
        self.save_to_txt(os.path.join(useful_ip_file_path, useful_ip_file_name), self.all_proxies_filter)


if __name__ == '__main__':
    stock_spider = SpiderStock()
    stock_spider.run()
