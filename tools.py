# _*_ coding : utf-8 _*_
# @Time : 2023/3/6 0:47
# @Author : jiang
# @File : tools
# Project : FreeIPProxyGettingPro

import sys
import requests
from lxml import etree
import json
import random
from tqdm import tqdm
from config import *

here = os.path.dirname(__file__)


def check_proxy_selfreq(ip, port, timeout=3):
    """
    方式一：利用 requests 访问百度首页，测试代理是否可用
    :param ip:
    :param port:
    :param timeout:
    :return:
    """
    url = 'http://www.baidu.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    proxies = {
        'http': '{}:{}'.format(ip, port),
        'https': '{}:{}'.format(ip, port)
    }
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)
        if '百度一下' in response.text:
            print(f'请求成功，代理 {ip} 有效！')
            # with open('xx.html', 'w', encoding='utf-8') as f:
            #     f.write(response.text)
            return True, {'ip': ip, 'port': port}
        else:
            # print('请求失败，代理 IP 无效：404')
            return False, None
    except Exception as e:
        # print(f'请求失败，代理 IP 无效：{e}')
        return False, None


def check_proxy_icanhazip(ip, port, timeout=3, realtimeout=False):
    """
    方式二：根据 http://icanhazip.com/ 返回结果来判断
    :param ip:
    :param port:
    :param timeout:
    :return:
    """
    url = "http://icanhazip.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    # 设置重连次数
    # requests.adapters.DEFAULT_RETRIES = 3
    proxies = {
        'http': '{}:{}'.format(ip, port),
        'https': '{}:{}'.format(ip, port)
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=timeout, proxies=proxies)
        proxy_ip = response.text.strip()
        if proxy_ip in [pv.split(':')[0] for pv in proxies.values()]:
            if realtimeout:
                print(f'代理 {ip}:{port} 有效！')
            return True, {'ip': ip, 'port': port}
        else:
            # print("代理 IP 无效：返回结果不一致。")
            return False, None
    except Exception as e:
        # print(f"代理 IP 无效：{e}")
        return False, None


def check_proxy_900cha(proxy, timeout=3, realtimeout=False):
    """
    方式三：根据 https://ip.900cha.com/ 返回结果来判断
    :param proxy:
    :param timeout:
    :param realtimeout: 是否实时输出可用代理
    :return:
    """
    url = 'https://ip.900cha.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    proxies = {
        'http': '{}:{}'.format(proxy['ip'], proxy['port']),
        'https': '{}:{}'.format(proxy['ip'], proxy['port'])
    }
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)
    except Exception as e:
        # print(f'代理无效：{e}')
        return False, None
    else:
        tree = etree.HTML(response.text)
        ret_ip = tree.xpath('//div[@class="col-md-8"]/h3/text()')[0].strip()
        # if ret_ip in [pv.split(':')[0] for pv in proxies.values()]:
        if ret_ip == proxies['http'].split(':')[0]:
            if realtimeout:
                print(f'代理 {proxy["ip"]}:{proxy["port"]} 有效！')
            return True, proxy
        else:
            # print('代理无效：验证不一致！')
            return False, None


def read_files():
    file_path = os.path.join(here, 'proxies_spider_results')
    # for file in sorted(os.listdir(file_path)):
    #     print(file)
    file_latest = sorted(os.listdir(file_path))[-1]
    with open(os.path.join(file_path, file_latest), 'r', encoding='utf=8') as f:
        all_free_proxies = [json.loads(s.strip()) for s in f.readlines()]

    return all_free_proxies


def get_latest_proxy_file(useful_ip_file_path):
    """
    获取当前路径下的最新文件
    :param useful_ip_file_path:
    :return:
    """
    file_latest = sorted(os.listdir(useful_ip_file_path))[-1]
    with open(os.path.join(useful_ip_file_path, file_latest), 'r', encoding='utf=8') as f:
        all_free_proxies = [json.loads(s.strip()) for s in f.readlines()]

    return all_free_proxies


def get_free_proxy():
    all_free_proxies = read_files()
    for i in tqdm(range(len(all_free_proxies)), file=sys.stdout, desc='choosing a useful proxy...'):
        index = random.randint(0, len(all_free_proxies)-1)
        proxy = all_free_proxies[index]
        useful, proxy = check_proxy_900cha(proxy)
        if useful:
            return proxy
    print('无可用 proxy ~')
    return None


if __name__ == '__main__':
    # ip = '104.17.209.9'
    # port = '80'
    #
    # # ip = '193.151.157.68'
    # # port = '80'
    #
    # ip = '183.221.242.102'
    # port = '9443'
    #
    # check_proxy_selfreq(ip, port)
    # print()
    # check_proxy_icanhazip(ip, port)
    # print()
    # check_proxy_900cha(ip, port)

    # file_latest = read_files()
    # print(file_latest)

    proxy = get_free_proxy()
    print(proxy)

