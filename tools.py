# _*_ coding : utf-8 _*_

import sys
import requests
from lxml import etree
import json
import random
from tqdm import tqdm
import os
from config import useful_ip_file_path


here = os.path.dirname(__file__)


def check_proxy_900cha(proxy, timeout=3, realtimeout=False):
    """
    根据 https://ip.900cha.com/ 返回结果来测试代理的可用性
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
        return False, None
    else:
        tree = etree.HTML(response.text)
        ret_ip = tree.xpath('//div[@class="col-md-8"]/h3/text()')[0].strip()
        if ret_ip == proxies['http'].split(':')[0]:
            if realtimeout:
                print(f'代理 {proxy["ip"]}:{proxy["port"]} 有效！')
            return True, proxy
        else:
            return False, None


def get_latest_proxy_file(file_path):
    """
    获取当前路径下的最新文件内容
    :param file_path:
    :return:
    """
    file_latest = sorted(os.listdir(file_path))[-1]
    with open(os.path.join(file_path, file_latest), 'r', encoding='utf=8') as f:
        all_free_proxies = [json.loads(s.strip()) for s in f.readlines()]

    return all_free_proxies


def get_free_proxy():
    all_free_proxies = get_latest_proxy_file(useful_ip_file_path)
    for i in tqdm(range(len(all_free_proxies)), file=sys.stdout, desc='choosing a useful proxy...'):
        index = random.randint(0, len(all_free_proxies)-1)
        proxy = all_free_proxies[index]
        useful, proxy = check_proxy_900cha(proxy)
        if useful:
            return proxy
    print('无可用 proxy ~')
    return None


if __name__ == '__main__':
    proxy = get_free_proxy()
    print(proxy)

