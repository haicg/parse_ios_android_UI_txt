#!/usr/bin/python2.7
# coding=utf-8


import xlrd
import globalVal


def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)


def read_cell(table, x, y):
    if table.cell_type(x, y) == 4:  # 4是真值类型(bool)
        return "TRUE" if table.cell_value(x, y) == 1 else "FALSE"
    elif table.cell_type(x, y) == 2:  # 2是数字类型(number)
        return str(table.cell_value(x, y))
    else:  # 其他类型不再一一列举，用到时再做增加
        return table.cell_value(x, y)

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
        typeCell0 = table.cell_type(rownum, 0)
        typeCell1 = table.cell_type(rownum, 1)
        typeCell2 = table.cell_type(rownum, 2)
        if (len(row) > 2 ):
            row[0] = read_cell(table, rownum, 0)
            row[1] = read_cell(table, rownum, 1)
            row[2] = read_cell(table, rownum, 2)
            if (row[0].startswith('//') or row[0].startswith('/*')):
                map_dict.append(row[0])
            elif (row[1] == '' or typeCell0 == 0):
                map_dict.append(row[0])
            elif row[2] == '' or typeCell2 == 0:
                map_dict.append(row[0])
                map_dict.append(row[1])
                if (typeCell0 != 1 or typeCell1 != 1):
                    err_msg = {}
                    err_msg['line'] = rownum;
                    err_msg['key'] = row[0];
                    globalVal.g_list_result_error_cols.append(err_msg)
            else:
                map_dict.append(row[0])
                map_dict.append(row[2])
                if (typeCell0 != 1 or typeCell1 != 1 or typeCell2 != 1):
                    err_msg = {}
                    err_msg['line'] = rownum;
                    err_msg['key'] = row[0];
                    globalVal.g_list_result_error_cols.append(err_msg)
        elif (len(row) > 0) :
            map_dict.append(row[0])
        else:
            continue
        globalVal.g_list_all_res_vals.append(map_dict)
    return globalVal.g_list_all_res_vals


#根据名称获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称


def load_one_lang_single_sheet(excel_object, table, key_index, val_index):
    result_map = {}
    nrows = table.nrows  # 行数
    for rownum in range(1,nrows):
        row_values = table.row_values(rownum)
        if row_values and row_values[key_index] and row_values[val_index]:
            result_map[row_values[key_index]] = row_values[val_index].strip()
    return result_map


def getColMap(colnames):
    langname2indexmap = {}
    index2langnamemap = {}
    i = 0
    keynameIndex = -1
    for i in range(len(colnames)):
        colnames[i] = colnames[i].replace(" ", "")
        if colnames[i] == u"EN英文":
            colnames[i] = u"EN英语"
        elif "瑞典语SE" == colnames[i] or colnames[i].find("SE瑞典语") != -1 :
            colnames[i] = "SE瑞典语"
        elif "意大利语IT" == colnames[i] or colnames[i].find("IT意大利语") != -1:
            colnames[i] = "IT意大利语"
        index2langnamemap[i] = colnames[i]

        if colnames[i] == u"备注说明":
            continue
        elif colnames[i].find("Keyname") != -1:
            keynameIndex = i
        else :
            langname2indexmap[colnames[i]] = i
    return keynameIndex, langname2indexmap, index2langnamemap


def load_langs_sheet(excel_object, sheetname, colnameindex=0):
    table = excel_object.sheet_by_name(sheetname)
    colnames =  table.row_values(colnameindex) #某一行数据
    # print colnames
    list =[]
    global g_langs_map
    keynameIndex, colMap, index2langname = getColMap(colnames)
    if keynameIndex < 0:
        return None
    langs_map = {}
    for lang_name, lang_index in colMap.items():
        # if len(langs_map) == 0:
        #     langs_map[lang_index] = {}
        langs_map[lang_name] = load_one_lang_single_sheet(excel_object, table, keynameIndex, lang_index)
    return langs_map


def excel_load_sheets(file= 'file.xls'):
    excel_obj = open_excel(file)
    names = excel_obj.sheet_names()
    langs_map = {}
    for item in names:
        if u"版本备注" != item:
            print item
            onesheet_langs_map = load_langs_sheet(excel_obj, item)
            # print onesheet_langs_map
            if not onesheet_langs_map:
                continue
            for lang_name, lang_val_map in onesheet_langs_map.items():
                if not langs_map.has_key(lang_name):
                    langs_map[lang_name] = lang_val_map
                else:
                    langs_map[lang_name] = dict(langs_map[lang_name],**lang_val_map)

    for (lang_name, lang_val_map) in langs_map.items():
        print lang_name
        print len(lang_val_map)
        # print lang_val_map

    return langs_map