# _*_ coding : utf-8 _*_
# @Time : 2023/3/11 23:34
# @Author : jiang
# @File : spider
# Project : FreeIPProxyGettingPro

"""
定义基础 Spider 类
"""
import sys
import time
import requests
from wrappers import old_version_fun_wrapper, req_exceed_limit_wrapper, req_respose_none_wrapper
from tqdm import tqdm
from tools import check_proxy_icanhazip, check_proxy_900cha
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from config import *
from tools import get_free_proxy
from custom_exceptions import Request500Exception, TryWithSelfProxyLimitException


class Spider:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.headers = kwargs.get('headers')
        self.req_type = kwargs.get('req_type')
        self.data = kwargs.get('data')
        self.proxies = kwargs.get('proxies')
        self.verify = kwargs.get('verify')
        self.day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())).split(' ')[0].strip()
        self.timeout = 3

        self.proxy_try_num = 0      # 设置代理时的全局失败尝试次数
        self.response = None
        self.parse_urls = []
        self.all_proxies = []
        self.all_proxies_filter = []

    @old_version_fun_wrapper
    def get_and_set_response(self, url=None, headers=None, data=None, proxies=None, verify=True):
        """
        获取 response
        若不传参，则返回当前 response，否则，重新请求并更新当前对象的 response 属性，返回新的 response
        """
        if url is None:
            return self.response
        else:
            if data is None:
                self.response = requests.get(url, headers=headers, timeout=self.timeout, proxies=proxies, verify=verify)
            else:
                self.response = requests.post(url, data=data, headers=headers, timeout=self.timeout, proxies=proxies, verify=verify)
            return self.response

    def pre_parse(self):
        """
        识别当天代理信息页面
        """
        pass

    @req_respose_none_wrapper
    def parse(self):
        """
        解析代理
        """
        pass

    def get_all_proxies(self):
        """
        获取所有 proxies
        """
        pass

    def update_attrs(self, *args, **kwargs):
        """
        update the spider object's self attrs
        :param args:
        :param kwargs:
        :return:
        """
        self.url = self.url if kwargs.get('url') is None else kwargs.get('url')
        self.headers = self.headers if kwargs.get('headers') is None else kwargs.get('headers')
        self.req_type = self.req_type if kwargs.get('req_type') is None else kwargs.get('req_type')
        self.data = self.data if kwargs.get('data') is None else kwargs.get('data')
        self.proxies = self.proxies if kwargs.get('proxies') is None else kwargs.get('proxies')
        self.verify = self.verify if kwargs.get('verify') is None else kwargs.get('verify')
        self.timeout = self.timeout if kwargs.get('timeout') is None else kwargs.get('timeout')

    @req_exceed_limit_wrapper
    def update_response(self, *args, **kwargs):
        """
        recontruct a url request, and update the spider's response attribute
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if self.proxy_try_num >= RETRY_LIMIT:
                # reset the re-request up limit
                self.proxy_try_num = 0
                # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                # input()
                # 如果是 500 这种有返回一个页面的，无需抛出异常，因为此时 self.response 并不是 None，后续的解析会返回 []
                # 如果是其他错误，并且会导致无返回页面的，则需要手动抛出异常，因为此时 self.response 是 None，后续解析会报错
                raise TryWithSelfProxyLimitException

            if self.data is None:
                self.response = requests.get(self.url, headers=self.headers, timeout=self.timeout, proxies=self.proxies, verify=self.verify)
            else:
                self.response = requests.post(self.url, headers=self.headers, data=self.data, timeout=self.timeout, proxies=self.proxies, verify=self.verify)

            # 自定义一些特定异常
            if self.response.status_code == 500:
                raise Request500Exception(self)

        # except Request500Exception as e:
        #     print('[{}][{}] | page: {} | e >>> {}'.format(self.proxy_try_num, self.__class__.__name__, self.url, e))
        except TryWithSelfProxyLimitException as e:
            # 该类 Exception 无需重新请求，直接返回就好
            # print('[{}] | page: {} | e >>> {}'.format(self.__class__.__name__, self.url, e))
            # 继续往上抛出，让上层处理，因为直接返回 self.response 是 None，上层解析会报错
            raise TryWithSelfProxyLimitException
        except Exception as e:
            print('\033[1;31m{}\033[0m'.format(
                '[{}][{}] | page: {} | e >>> {}'.format(self.proxy_try_num, self.__class__.__name__, self.url, e)
            ))
            if self.proxy_try_num == 0:
                # 先简单停一下
                print('\033[1;31m{}\033[0m'.format(
                    '停一下停一下~'
                ))
                time.sleep(16)
            else:
                # 使用新代理重新请求
                proxy = get_free_proxy()
                if proxy is None:
                    proxies = None
                else:
                    proxies = {
                        'http': '{}:{}'.format(proxy['ip'], proxy['port']),
                        'https': '{}:{}'.format(proxy['ip'], proxy['port']),
                    }
                print('[{}] use new proxy: {}'.format(self.__class__.__name__, proxies))
                self.update_attrs(proxies=proxies)
            self.proxy_try_num += 1
            return self.update_response()

        return self.response

    @old_version_fun_wrapper
    def filter_all_proxies(self):
        """
        测试所有代理的可用性
        """
        all_proxies_filter = []
        for proxy in tqdm(self.all_proxies):
            ip = proxy['ip']
            port = proxy['port']
            is_useful = check_proxy_icanhazip(ip, port)
            if is_useful:
                all_proxies_filter.append(proxy)
        return all_proxies_filter

    def filter_all_proxies_mp(self):
        """
        测试代理 ip 可用性
        多进程处理
        """
        # print(f'IP 验证，主进程开始执行, pid:{os.getpid()}')
        self.all_proxies_filter = dict()

        # 进程池
        pool = ProcessPoolExecutor(max_workers=50)
        all_task = [pool.submit(check_proxy_900cha, proxy) for proxy in self.all_proxies]
        for future in tqdm(as_completed(all_task), total=len(all_task), file=sys.stdout, desc='[{}] checking proxies...'.format(self.__class__.__name__)):
            res, proxy = future.result()
            if res:
                self.all_proxies_filter['{}:{}'.format(proxy['ip'], proxy['port'])] = proxy

        # 这种写法有坑啊，如果在 for 循环中等待子进程返回结果，那本质上根本就没有多进程并行啊
        # with ProcessPoolExecutor(max_workers=50) as pool:
        #     for proxy in tqdm(self.all_proxies, desc='checking proxies...'):
        #         task = pool.submit(check_proxy_icanhazip, proxy['ip'], proxy['port'])
        #         res = task.result()
        #         if res:
        #             self.all_proxies_filter[proxy['ip']] = proxy

        self.all_proxies_filter = self.all_proxies_filter.values()
        return self.all_proxies_filter

    def save_to_txt(self, file_name, all_proxies, add_day_tag=True):
        """
        存文件
        """
        if not os.path.isdir(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        if add_day_tag:
            file_name = file_name.split('.')[0] + '_{}.'.format(self.day.replace('-', '_')) + file_name.split('.')[-1]
        with open(file_name, 'a+', encoding='utf-8') as f:
            for proxy in all_proxies:
                f.write(json.dumps(proxy, ensure_ascii=False) + '\n')
        # print(f'写入成功：{file_name}')

    def run(self):
        """
        General spider running logic：
            init -> face page url request -> (resource page collect) -> crawl all proxies -> check proxies' usability -> save
        :return:
        """
        # 1 入口请求
        # self.update_response()

        # 1 > 更新：request 不在初始化中体现，全部归类到 get_all_proxies() 中

        # try:

        # 2 爬取所有 proxies
        self.all_proxies = self.get_all_proxies()
        print('[{}] 爬取代理数：{}'.format(self.__class__.__name__, len(self.all_proxies)))
        # 3 过滤可用代理
        self.all_proxies_filter = self.filter_all_proxies_mp()
        print('[{}] 可用代理数：{}'.format(self.__class__.__name__, len(self.all_proxies_filter)))
        # 4 存储可用代理
        # 默认存储路径配置在 config 中，如果想要另存，在子爬虫中重构 run() 方法即可
        self.save_to_txt(os.path.join(useful_ip_file_path, useful_ip_file_name), self.all_proxies_filter)

        print('[{}] run successed.'.format(self.__class__.__name__))

        # except AttributeError:
        #     print('无法正常爬取 [{}] ~'.format(self.__class__.__name__))
        # except Exception as e:
        #     print('无法正常爬取 | [{}] e >>> '.format(self.__class__.__name__), e)

        return list(self.all_proxies_filter)


if __name__ == '__main__':
    help(Spider)

    # print(os.path.join(useful_ip_file_path, useful_ip_file_name))

