import codecs
import globalVal
import xml.etree.ElementTree as ET

def save_map_to_ios(filename, res_map, apptype=0, keyindex_map = None):
    if apptype != 0:
        print "Not IOS Res"
        return
    list_res = ""
    with codecs.open(filename, 'w', encoding='utf8') as fp:
        if keyindex_map:
            for index,key in keyindex_map.items():
                if res_map.has_key(key):
                    s = u'"%s" = "%s";\n' % (key, res_map[key])
                    list_res = list_res + s
        else:
            for key,value in res_map.items():
                s = u'"%s" = "%s";\n' % (key, value)
                list_res = list_res + s
            # print list_res
        fp.write(list_res)


def save_all_langs_to_ios(dirname, res_map, apptype=0):
    for lang_name, lang_val_map in res_map.items():
        filename = "{}/{}.txt".format(dirname, lang_name)
        save_map_to_ios(filename, lang_val_map, apptype)


def save_all_langs_to_ios_with_keyindex(keyindex, dirname, res_map, apptype=0):
    for lang_name, lang_val_map in res_map.items():
        filename = "{}/{}.txt".format(dirname, lang_name)
        save_map_to_ios(filename, lang_val_map, apptype, keyindex)


def save_map_to_xml(file='res.xml', res_map={}):
    list_res = ""
    import xml.dom.minidom
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    root = dom.documentElement
    if not res_map:
        return
    with codecs.open(file, 'w', encoding='utf8') as fp:
        # fieldnames = ['key', 'value']
        for k, v in res_map.items():
            stringNode = None
            stringNode = dom.createElement('string')
            stringNode.setAttribute('name', k)
            try:
                textNode = dom.createTextNode(v)
                stringNode.appendChild(textNode)
            except Exception as e:
                print (e)
                raise TypeError, v + "Not String"

            if stringNode:
                root.appendChild(stringNode)
        dom.writexml(fp, addindent='  ', newl='\n', encoding='utf-8')


def save_all_langs_to_android(dirname, res_map):
    for lang_name, lang_val_map in res_map.items():
        filename = "{}/{}.xml".format(dirname, lang_name)
        save_map_to_xml(filename, lang_val_map)
