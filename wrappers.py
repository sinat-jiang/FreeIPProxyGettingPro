# _*_ coding : utf-8 _*_

"""
some self-define wrapper funcs
"""

from functools import wraps
from custom_exceptions import ResponseTextNoneException


def req_respose_none_wrapper(func):
    """
    self.response = None 时的装饰器
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
