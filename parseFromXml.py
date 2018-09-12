# coding=utf-8
import sys,os
import sqlite3
import errno
import json
import globalVal
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class CommentedTreeBuilder(ET.XMLTreeBuilder):
    def __init__(self, html=0, target=None):
        ET.XMLTreeBuilder.__init__(self, html, target)
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ET.Comment, {})
        self._target.data(data)
        self._target.end(ET.Comment)

def import_data(filename):
    fp = None

    with open(filename, 'r') as fp:
        tree = ET.parse(fp, parser=CommentedTreeBuilder())
        root = tree.getroot()
        for child in root:
            key_str = None
            val_str = None
            dict_ele = []
            if child.attrib:
                #print "key = " + child.attrib['name']
                key_str = child.attrib['name']
                val_str = child.text
            else:
                key_str = child.text
                val_str = None

            dict_ele.append(key_str)
            if (val_str):
                dict_ele.append(val_str)
            globalVal.g_list_all_vals.append(dict_ele)

#from ET.SimpleXMLWriter import XMLWriter
import codecs
def packet_to_xml():
    #from xml.dom.minidom import Document
    import xml.dom.minidom
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    root = dom.documentElement
    stringNode = dom.createElement('string')
    root.appendChild(stringNode)
    stringNode.setAttribute('name', '12345')
    textNode = dom.createTextNode('Sensor')
    stringNode.appendChild(textNode)
    commentNode = dom.createComment('HAHA')
    root.appendChild(commentNode)


    f= codecs.open('employees2.xml', 'w', encoding='utf-8')
    dom.writexml(f, addindent='  ', newl='\n',encoding='utf-8')
    f.close()

def save_result_xml(file='res.xml', res_list=[], apptype=0):
    list_res = ""
    import xml.dom.minidom
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    root = dom.documentElement
    with codecs.open(file, 'w', encoding='utf8') as fp:
        # fieldnames = ['key', 'value']
        for ele in res_list:
            stringNode = None
            if (apptype == 0):
                if (len(ele) == 1):
                    #s = u'%s' % (ele[0])
                    stringNode = dom.createComment(ele[0])
                elif (len(ele) == 2):
                    #s = u'"%s" = "%s";\n' % (ele[0], ele[1])
                    stringNode = dom.createElement('string')
                    stringNode.setAttribute('name', ele[0])
                    try:
                        textNode = dom.createTextNode(ele[1])
                        stringNode.appendChild(textNode)
                    except Exception as e:
                        print (e)
                        raise TypeError, ele[1] + "Not String"
                else:
                    continue
            else:
                continue
            if stringNode:
                root.appendChild(stringNode)
        dom.writexml(fp, addindent='  ', newl='\n', encoding='utf-8')


#packet_to_xml()
