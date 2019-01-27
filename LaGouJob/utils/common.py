# -*- coding: utf-8 -*-
"""
   File Name:common
   Date：2019/1/20
   Change Activity:2019/1/20
   Description:
   框架需要使用的一些其他函数
"""

import hashlib


def get_md5(url):
    """
    将url链接转换成md5
    :param url:
    :return:
    """
    if isinstance(url, str):
        url = url.encode("utf-8")       # 设置url的编码为utf-8
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('http://web.jobbole.com/95617/'))
