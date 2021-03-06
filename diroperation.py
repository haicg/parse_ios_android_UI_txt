#!/usr/bin/python2.7
# coding=utf-8
from globalVal import g_dir_ios_convert_error_result, g_dir_ios_convert_result, g_dir_ios_all_langs_result
from globalVal import g_dir_android_all_langs_result, g_dir_all_langs_error_result


def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False


def initDirs():
    mkdir(g_dir_ios_convert_error_result)
    mkdir(g_dir_ios_convert_result)
    mkdir(g_dir_ios_all_langs_result)
    mkdir(g_dir_android_all_langs_result)
    mkdir(g_dir_all_langs_error_result)


