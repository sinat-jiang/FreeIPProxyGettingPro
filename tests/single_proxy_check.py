# _*_ coding : utf-8 _*_
# @Time : 2023/4/11 16:58
# @Author : jiang
# @File : single_proxy_check
# Project : FreeIPProxyGettingPro

"""
单个代理的验证
"""

import requests


if __name__ == '__main__':

    proxy = {'ip': '111.40.124.221', 'port': '9091'}
    proxies = {
        'http': '{}:{}'.format(proxy['ip'], proxy['port']),
        'https': '{}:{}'.format(proxy['ip'], proxy['port']),
    }

    check_url = 'https://ip.900cha.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    response = requests.get(url=check_url, headers=headers)

    with open('single_proxy_check.html', 'w', encoding='utf-8') as f:
        f.write(response.text)