# coding=utf-8
import codecs
import json
import tkFileDialog
from Tkinter import *
from FileDialog import *
import ttk
import tkMessageBox
import globalVal
import parse_words
import parseFromXml


#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

def get_txt_dialog_option(title, filename):
    options = {}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('TXT', '*.txt')]
    options['initialdir'] = cur_file_dir()
    options['initialfile'] = filename
    options['title'] = title
    return options


def get_xls_dialog_option(title, filename):
    options = {}
    options['defaultextension'] = '.xls'
    options['filetypes'] = [('Excel', '*.xls')]
    options['initialdir'] = cur_file_dir()
    options['initialfile'] = filename
    options['title'] = title
    return options

def get_xml_dialog_option(title, filename):
    options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('*.XML', '*.xml')]
    options['initialdir'] = cur_file_dir()
    options['initialfile'] = filename
    options['title'] = title
    return options

def donothing():
    x = 0

def choose_data_file():
    filename = tkFileDialog.askopenfilename(title='choose data file',
                                            filetypes=[('TXT', '*.txt'),('XML', '*.xml')],
                                            initialdir=cur_file_dir())

    pathext = os.path.splitext(filename)[1]
    print pathext
    if pathext == '.xml' or pathext == '.XML':
        print "XML FILE"
        parseFromXml.import_data(filename)
    elif pathext == '.txt' or pathext == '.TXT':
        print "TXT FILE"
        parse_words.import_data(filename)
    else:
        return
    data_excel_name = tkFileDialog.asksaveasfilename(title='save empty Excel file',
                                        filetypes=[('Excel', '*.xls')],
                                       initialdir=cur_file_dir())
    #parse_words.save_to_cvs(data_excel_name, globalVal.g_map_all_vals)
    parse_words.save_to_excel(data_excel_name, globalVal.g_list_all_vals)
    str_val = 'success ! \n Excel File Path: %s' % (data_excel_name)
    msgBox = tkMessageBox.showinfo('Result', str_val)

def choose_excel_file():
    map_dict_val = []
    globalVal.g_excel_file = ""
    option = {}
    option = get_xls_dialog_option('Excel file', "")
    excel_file_name = tkFileDialog.askopenfilename(**option)
    if excel_file_name == None or excel_file_name == "":
        return map_dict_val
    else :
        map_dict_val = parse_words.excel_table_byindex(file=excel_file_name)
    (filepath, tempfilename) = os.path.split(excel_file_name)
    os.path.splitext(tempfilename)
    (filename, extension) = os.path.splitext(tempfilename)
    globalVal.g_excel_file = filename;
    #print map_dict_val
    return map_dict_val

def save_err_check_to_file(res_file_name):
    (filepath, tempfilename) = os.path.split(res_file_name)
    os.path.splitext(tempfilename)
    (filename, extension) = os.path.splitext(tempfilename)
    ResultErrorColsFile = filepath + '/' + filename + "_ResultErrorCols.txt"
    with codecs.open(ResultErrorColsFile, 'w', encoding='utf8') as fp:
        resErrorBuf = json.dump(globalVal.g_list_result_error_cols, fp, indent=4)
    msgBox = tkMessageBox.showinfo('Notification', "Need Read " + ResultErrorColsFile)
    globalVal.g_list_result_error_cols = []

def save_to_txt():
    map_dict_val = choose_excel_file()
    option = {}
    option = get_txt_dialog_option('save result file', globalVal.g_excel_file)
    res_file_name = tkFileDialog.asksaveasfilename(**option)
    # parse_words.save_to_cvs(data_excel_name, globalVal.g_map_all_vals)

    parse_words.save_result_txt(res_file_name, map_dict_val)
    str_val = 'success ! \n RESULT File Path: %s' % (res_file_name)
    msgBox = tkMessageBox.showinfo('Result', str_val)
    save_err_check_to_file(res_file_name)

def save_to_xml():
    map_dict_val = choose_excel_file()
    option = {}
    option = get_xml_dialog_option('save result file', globalVal.g_excel_file)
    res_file_name = tkFileDialog.asksaveasfilename(**option)
    # parse_words.save_to_cvs(data_excel_name, globalVal.g_map_all_vals)

    parseFromXml.save_result_xml(res_file_name, map_dict_val)
    str_val = 'success ! \n RESULT File Path: %s' % (res_file_name)
    msgBox = tkMessageBox.showinfo('Result', str_val)
    save_err_check_to_file(res_file_name)

def ui_create():
    root = Tk()
    root.title('Translate Words')
    # -- Create the menu frame, and menus to the menu frame
    menu_frame = Frame(root)

    menu_frame.pack(fill=X, side=TOP)
    menubar = Menu(menu_frame)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=choose_data_file)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)


    history_frame = Frame(root)
    history_frame.pack(fill=X, side=BOTTOM, pady=2)
    # -- Create the info frame and fill with initial contents
    '''
    info_frame = Frame(root)
    info_frame.pack(fill=X, side=TOP)
    # first put the column labels in a sub-frame
    label_line = Frame(info_frame, relief=RAISED, borderwidth=1)
    label_line.pack(side=TOP, padx=2, pady=1)
    Label(label_line, text="Key", width=100).pack(side=LEFT)
    Label(label_line, text="translate Words", width=100).pack(side=LEFT)
    # then put the "next run" information in a sub-frame
    info_line = Frame(info_frame)
    info_line.pack(side=TOP, padx=2, pady=1)
    Label(info_line, text="1 #", width=100).pack(side=LEFT)
    Entry(info_line, bd=5, width=100, textvariable="TEST").pack(side=LEFT)
'''
    tree = ttk.Treeview(root, columns=('col1', 'col2'))
    tree.column('col1', width=100, anchor='center')
    tree.column('col2', width=100, anchor='center')

    def onDBClick(event):
        item = tree.selection()[0]
        print "you clicked on ", tree.item(item, "values")

    for i in range(10):
        tree.insert('', i, values=('a' + str(i), 'b' + str(i), 'c' + str(i)))
    tree.bind("<Double-1>", onDBClick)
    tree.pack(side=LEFT)
        # -- Finally, let's actually do all that stuff created above
    mainloop()

def botton_ui_create():
    root = Tk()
    root.title('Translate Words')
    root.minsize(600, 400)
    centerFrame = Frame(root)
    centerFrame.pack(fill=X, side=TOP)

    buttonImport = Button(centerFrame, text='Import Data', width = 40, height = 4, command=choose_data_file)
    buttonImport.pack(side=TOP)
    buttonImport = Button(centerFrame, text='Convert RESULT EXCEL TO IOS TXT', width=40, height=4, command=save_to_txt)
    buttonImport.pack(side=TOP)
    buttonImport = Button(centerFrame, text='Convert RESULT EXCEL Android XML', width=40, height=4, command=save_to_xml)
    buttonImport.pack(side=TOP)
    mainloop()

def main():
    print "Hello"
    # import_data("data.txt")
    botton_ui_create()
    #print list(globalVal.g_map_all_vals)
    # save_to_cvs("res.cvs", globalVal.g_map_all_vals)
    # save_to_excel("res.xls", globalVal.g_map_all_vals)

      # connect_db()
    # ui_create()

if __name__ == "__main__":
    main()
