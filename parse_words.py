# coding=utf-8
import sys, os
import sqlite3
import errno
import json
import globalVal
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import csv
import xlwt
import codecs


def connect_db():
    globalVal.g_db_conn = sqlite3.connect('test.db')
    globalVal.g_db_conn.close()


def close_file(fp):
    try:
        fp.close()
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise


def open_file(filename):
    try:
        fp = open(filename)
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise IOError
    else:
        #      with fp:
        return fp


def open_file_write(filename):
    try:
        fp = open(filename, 'w')
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise
    else:
        #      with fp:
        return fp


def get_pure_data(data_str):
    pattern = re.compile('"(.*)"')
    list_res = pattern.findall(data_str)
    if (len(list_res) > 0):
        return list_res[0]
    return None


def store_one_recd(line_str, index, indexDict, filedataDicts):
    line_list = line_str.split("=")
    # print line_list
    if len(line_list) < 2:
        if len(line_list) == 1:
            line_list[0].strip()
            if line_list[0].startswith('//'):
                print "Comment  : {}".format(line_str)
                return index, indexDict, filedataDicts
            elif line_list[0].startswith('/*'):
                print "Comment  : {}".format(line_str)
                return index, indexDict, filedataDicts
            else:
                print "error data  list len = {} : {}".format(len(line_list), line_str)
                return index, indexDict, filedataDicts
        else:
            print "error data EMPTY {} ".format(line_str)
            return index, indexDict, filedataDicts
    val_str = None
    if len(line_list) == 0:
        print "ERROR DATA line_list length 0"
        return index, indexDict, filedataDicts

    elif len(line_list) > 1:
        val_str = get_pure_data(line_list[1])
        key_str = get_pure_data(line_list[0])
    else:
        val_str = None
        key_str = line_list[0]
        print "ERROR DATA : {}".format(line_list)
        return index, indexDict, filedataDicts
    if val_str:
        # dict_ele.append(val_str)
        filedataDicts[key_str] = val_str.strip()
        indexDict[index] = key_str
        index = index + 1
    else:
        filedataDicts[key_str] = ""
        indexDict[index] = key_str
        index = index + 1
        print ("store_one_recd : line_str = {}".format(line_str))
    # globalVal.g_list_all_vals.append(dict_ele)
    return index, indexDict, filedataDicts


def save_to_excel(xlsfilename, list_val):
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)  ##第二参数用于确认同一个cell单元是否可以重设值。

    sheet.write(0, 0, 'some text')
    sheet.write(0, 0, 'this should overwrite')  ##重新设置，需要cell_overwrite_ok=True

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    style.font = font
    i = 0
    j = 0
    for ele in list_val:
        if (len(ele) > 1):
            sheet.write(i, j + 1, ele[1], style)
        sheet.write(i, j, ele[0], style)
        i = i + 1
    wbk.save(xlsfilename)  ##该文件名必须存在


def save_to_cvs(csvfilename, dict_val):
    with open(csvfilename, 'wb') as csvfile:
        # fieldnames = ['key', 'value']
        writer = csv.writer(csvfile)
        for (k, v) in dict_val.items():
            # print [k , v]
            writer.writerow([k, v])


def import_ios_resource_data(filename):
    fp = None
    filedataDicts = {}
    indexDict = {}
    index = 0
    with codecs.open(filename, 'r', encoding='utf8') as fp:
        fp = open_file(filename)
        while True:
            line = fp.readline()
            if not line:
                break
            # print line
            index, indexDict, filedataDicts = store_one_recd(line, index, indexDict, filedataDicts)

    return indexDict, filedataDicts
