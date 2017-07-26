# coding=utf-8
import sys,os
import sqlite3
import errno
import json
import globalVal
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import csv
import xlrd
import xlwt
import ui
import codecs


def connect_db():
    globalVal.g_db_conn = sqlite3.connect('test.db')
    globalVal.g_db_conn.close()



def close_file(fp):
    try:
        fp. close()
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

def store_one_recd(line_str):
    line_list = line_str.split("=")
    #print line_list
    if (len(line_list) < 2) :
        if (len(line_list) == 1) :
            line_list[0].strip()
            if (line_list[0].startswith('//')):
                print "Comment"
            elif (line_list[0].startswith('/*')):
                print "Comment"
            else :
                print "error data"
                return
        else:
            print "error data"
            return
    dict_ele = []
    val_str = None
    if (len(line_list) == 0):
        print "ERROR DATE"
        return
    elif (len(line_list) > 1):
        val_str = get_pure_data(line_list[1])
        key_str = get_pure_data(line_list[0])
    else:
        val_str = None
        key_str = line_list[0]
    dict_ele.append(key_str)
    if (val_str):
        dict_ele.append(val_str)
    globalVal.g_list_all_vals.append(dict_ele)
    return


def save_to_excel(xlsfilename, list_val):
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)  ##第二参数用于确认同一个cell单元是否可以重设值。

    sheet.write(0,0,'some text')
    sheet.write(0,0,'this should overwrite')   ##重新设置，需要cell_overwrite_ok=True

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
        i = i+1
    wbk.save(xlsfilename)    ##该文件名必须存在

def save_to_cvs(csvfilename, dict_val):
    with open(csvfilename, 'wb') as csvfile:
        #fieldnames = ['key', 'value']
        writer = csv.writer(csvfile)
        for (k,v) in dict_val.items():
            #print [k , v]
            writer.writerow([k, v])

def import_data(filename):
    fp = None
    with codecs.open(filename, 'r', encoding='utf8') as fp:
        fp = open_file(filename)
        while True:
            line = fp.readline()
            if not line:
                break
            #print line
            store_one_recd(line)


def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

#根据索引获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    #colnames =  table.row_values(colnameindex) #某一行数据

    for rownum in range(0,nrows):
        row = table.row_values(rownum)
        map_dict = []
        if (len(row) > 2 ):
            if (row[0].startswith('//') or row[0].startswith('/*')):
                map_dict.append(row[0])
            else:
                map_dict.append(row[0])
                map_dict.append(row[2])
        elif (len(row) > 0) :
            map_dict.append(row[0])
        else:
            continue
        globalVal.g_list_all_res_vals.append(map_dict)
    return globalVal.g_list_all_res_vals

#根据名称获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list


def save_result_txt(file='res.txt', res_list = [], apptype = 0):
    list_res = ""
    with codecs.open(file, 'w', encoding='utf8') as fp:
        # fieldnames = ['key', 'value']
        for ele in res_list:
            if (apptype == 0) :
                if (len(ele) == 1) :
                    s = u'%s' % (ele[0])
                elif (len(ele) == 2):
                    s = u'"%s" = "%s";\n' %(ele[0], ele[1])
                else:
                    continue
            else:
                continue
            list_res = list_res + s;
        fp.write(list_res)
