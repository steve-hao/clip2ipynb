from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication

from html2md import html2md,LF

from _datetime import datetime
import json

ignore_class =['result']

options = {
    'ignore_emphasis': False,   
    'ignore_images': False, 
    'ignore_links': False,
    'def_list': True,   
    'table': True, 
    'strikethrough': True, 
    'attrs': False, 
    'ul_style_dash': False, 
    'em_style_asterisk': False, 
    'ignore_list': [],
    'code_class': 'example_code'
        }

def md2ipynb(text):
    def add_code(code):
        cell = {}
        cell['metadata'] = {}
        cell['outputs'] = []
        cell['source'] = [code.strip()]
        cell['execution_count'] = None
        cell['cell_type'] = 'code'
        ipynb['cells'].append(cell)

    def add_md(md,ascode=False):

        mdtext = md.strip() if not ascode else '```' + LF + md.strip() + LF +'```' 
        cell = {}
        cell['metadata'] = {}
        cell['source'] = [mdtext]
        cell['cell_type'] = 'markdown'
        ipynb['cells'].append(cell)

    ipynb = {'nbformat': 4, 'nbformat_minor': 1, 'cells': [], 'metadata': {}}
    ident = 0

    text = text.strip().replace(LF+':    ',LF+'+ ')

    if text.startswith('```'):
        iscode = True 
        text = text[3:]
    else:
        iscode = False

    if text.endswith('```'):
        text = text[0:-3]

    tlist = text.split('```')

    for t in tlist:

        if not iscode:

            t,ident_char = t.rsplit(LF,1)
            ident = len(ident_char)
            if t.strip():
                add_md(t)
        else:
  
            ignore = False
            firstline,t = t.split(LF,1)

            for s in ignore_class:
                if s in firstline.split():
                    ignore = True
                    break

            if ignore:

                add_md(t,True)

            else:

                codelist=t.strip('\r\n').splitlines(True)
                
                if ident:
                    codelist = [t[ident:] for t in codelist]

                pre_type = ''
                in_code = True

                if codelist[0].startswith('>>>'):
                    pre_type = 'python'
                    sep_char = ' '
                    pre_char = '>>>'
                if codelist[0].startswith('In '):
                    pre_type = 'ipython'
                    sep_char = ':'
                    pre_char = 'In '
                if codelist[0].startswith('Out['):
                    pre_type = 'ipython'
                    sep_char = ':'
                    pre_char = 'In '
                    in_code = False
                
                if not pre_type:
            
                    code = ''.join(codelist)
                    add_code(code)
            
                else: 
            
                    code = ''
                    for c in codelist:
                        pre ,sep, others = c.partition(sep_char)

                        if in_code:

                            if pre.startswith(pre_char) or '...' in pre:
                                code += others
                            else:
                                add_code(code) 
                                in_code = False
                                code = others if pre.startswith('Out[') else c
                        else:
                            if pre.startswith(pre_char):
                                add_md(code,True) 
                                in_code = True
                                code = others
                            else:
                                code += others if pre.startswith('Out') else c
                                
                    if code:
                        if in_code:
                            add_code(code)
                        else:
                            add_md(code,True)            

        iscode = not iscode

    return ipynb

    

def monitor_clipboard():

    if  data.hasHtml(): 
        text=html2md(data.html(), **options)
        ipynb=md2ipynb(text)
        output_file = 'notebook' + datetime.now().strftime("%y%m%d%H%M%S")+'.ipynb'
        fp=open(output_file, 'w')
        fp.write(json.dumps(ipynb))
        fp.close()


if __name__ == '__main__':


    app = QApplication([])
    clipboard = app.clipboard()
    data = clipboard.mimeData()
    clipboard.dataChanged.connect(monitor_clipboard)
    app.exec_()
