# _*_ coding : utf-8 _*_
# @Time : 2023/4/12 21:12
# @Author : jiang
# @File : wrappers
# Project : FreeIPProxyGettingPro

"""
some self-define wrapper funcs
"""

from functools import wraps
from custom_exceptions import TryWithSelfProxyLimitException, ResponseTextNoneException


def old_version_fun_wrapper(func):
    """
    旧函数使用警告
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        print('\033[1;31m{}\033[0m'.format('Warning: This method will be remove in future version!'))
        return func(*args, **kwargs)
    return inner


def load_config_file_path_wrapper(func):
    """
    加载配置文件中的文件存储配置变量
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        kwargs['useful_ip_file_path'] = useful_ip_file_path
        kwargs['useful_ip_file_name'] = useful_ip_file_name
        return func(*args, **kwargs)

    return inner


def req_exceed_limit_wrapper(func):
    """
    对 update_response 方法装饰，对超出请求次数的 Exception 进行捕获
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        obj = args[0]
        try:
            res = func(*args, **kwargs)
            return res
        except TryWithSelfProxyLimitException as e:
            print('-' * 90)
            print('\033[1;31m{}\033[0m'.format(
                '[Trying times beyond the limit] [{}] | page: {} | e >>> {}'.format(obj.__class__.__name__, obj.url, e)
            ))
            print('-' * 90)
    return inner


def req_respose_none_wrapper(func):
    """
    当 update_response 失败时，大多数网页就报错了（少数返回一个错误页面），此时 response 为 None，parse 时会报错
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        obj = args[0]
        try:
            if obj.response is None:
                raise ResponseTextNoneException
            else:
                res = func(*args, **kwargs)
                return res
        except ResponseTextNoneException as e:
            print('-' * 90)
            print('\033[1;31m{}\033[0m'.format(
                '[Request failed, response is None] [{}] | page: {} | e >>> {}'.format(obj.__class__.__name__, obj.url, e)
            ))
            print('-' * 90)
            return []
    return inner
