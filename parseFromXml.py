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



#tree = ET.parse('IP116.xml')
tree = ET.parse('IP116.xml', parser=CommentedTreeBuilder())
root = tree.getroot()
for child in root:
    print child.tag
    print child.attrib
    if child.attrib:
        print "key = " + child.attrib['name']
    print child.text

    #print "value = " + child.text
    #print root.items