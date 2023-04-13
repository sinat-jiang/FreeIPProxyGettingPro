# _*_ coding : utf-8 _*_
# @Time : 2023/3/6 14:35
# @Author : jiang
# @File : test
# Project : FreeIPProxyGettingPro

from tools import *
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
import time
import requests
import random


def filter_all_proxies_mp(all_proxies):
    """
    多进程处理
    :param all_proxies:
    :return:
    """
    print(f'主进程开始执行, pid:{os.getpid()}')
    all_proxies_filter = set()
    with ProcessPoolExecutor(max_workers=10) as pool:
        for proxy in tqdm(all_proxies):
            task = pool.submit(check_proxy, proxy['ip'], proxy['port'])
            res = task.result()
            if res:
                all_proxies_filter.add(proxy)
                # print(f'{proxy["ip"]} 可用！')
            # else:
            #     # print(f'{proxy["ip"]} 不可用！')

    return all_proxies_filter


def mp_test():
    # 读
    with open('./89_proxies_2023-03-06.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(len(lines))
    lines = lines[:100]

    print(lines)
    lines = [json.loads(line) for line in lines]
    print(lines)

    # 多进程验证
    start = time.time()
    print(start)
    filter_all_proxies = filter_all_proxies_mp(lines)
    end = time.time()
    print(end)
    print(f'耗时：{end - start} s')
    print(len(filter_all_proxies))


def target_func(num):
    # time.sleep(random.randint(1, 2))
    re = pow(num, 2)
    print(re)
    return re


def mp_test2():
    with ProcessPoolExecutor(max_workers=3) as pool:
        for i in range(10):
            task = pool.submit(target_func, i)


def test_for_kuaidaili(ip, port):
    url = 'http://m.kuaidaili.com/free/inha'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    proxies = {
        'http': '{}:{}'.format(ip, port),
        'https': '{}:{}'.format(ip, port)
    }
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
        with open('test_kuaidaili.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
    except Exception as e:
        print(f'代理无效：{e}')
        return False

def test_for_ipcheck():
    url = 'https://www.kuaidaili.com/free/inha/1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    proxy = get_free_proxy()
    print('使用代理：', proxy)
    if proxy is None:
        proxies = None
    else:
        proxies = {
            'http': '{}:{}'.format(proxy['ip'], proxy['port']),
            'https': '{}:{}'.format(proxy['ip'], proxy['port']),
        }

    session = requests.Session()
    session.trust_env = False
    response = session.get(url=url, headers=headers, timeout=3, proxies=proxies)
    print(response.status_code)

    # response = requests.get(url=url, headers=headers, timeout=3, proxies=proxies)

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(response.text)


if __name__ == '__main__':
    # # mp_test()
    # # mp_test2()
    #
    # ip = '183.221.242.102'
    # port = '9443'
    #
    # # test_for_kuaidaili(ip, port)
    #
    # print('http://www.kxdaili.com/dailiip/1/1.html'.split('.html'))

    # ip check test
    # test_for_ipcheck()

    #
    # parse_url = 'http://www.kxdaili.com/dailiip/1/1.html'
    # i = 4
    # url_new = parse_url.split('.html')[0][:-1] + '{}.html'.format(i)
    # print(url_new)

    # import sys
    # ll = [3,4,5]
    # count = 0
    #
    # for i in range(len(ll)):
    #     tqdm.write('-' * 90)
    #     for j in tqdm(range(ll[i]), file=sys.stdout, colour='red'):
    #         count += 1
    #         tqdm.write('+')
    #         time.sleep(1)
    #
    # print(count)

    s = "hello, world"
    # 默认字体输出:
    print('\033[0m%s\033[0m' % s)

    # 高亮显示:
    print('\033[1;31;40m%s\033[0m' % s)
    print('\033[1;32;40m%s\033[0m' % s)
    print('\033[1;33;40m%s\033[0m' % s)
    print('\033[1;34;40m%s\033[0m' % s)
    print('\033[1;35;40m%s\033[0m' % s)
    print('\033[1;36;40m%s\033[0m' % s)

    print('\033[1;31m{}\033[0m'.format(s))
