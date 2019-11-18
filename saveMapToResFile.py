import codecs


def save_map_to_ios(filename, res_map, apptype=0):
    if apptype != 0:
        print "Not IOS Res"
        return
    list_res = ""
    with codecs.open(filename, 'w', encoding='utf8') as fp:
        for key,value in res_map.items():
            s = u'"%s" = "%s";\n' % (key, value)
            list_res = list_res + s
            # print list_res
        fp.write(list_res)


def save_all_langs_to_ios(dirname, res_map, apptype=0):
    for lang_name, lang_val_map in res_map.items():
        filename = "{}/{}.txt".format(dirname, lang_name)
        save_map_to_ios(filename, lang_val_map, apptype)