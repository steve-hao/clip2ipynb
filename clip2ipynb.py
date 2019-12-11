from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication

from html2md import html2md,LF

from _datetime import datetime
import json

ignore_class =['result']

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

    if text.startswith('```'):
        iscode = True 
        start = 3
    else:
        iscode = False
        start = 0

    loop = True

    while loop:
        end = text.find('```',start)
        if end == -1:
            end = len(text)
        else:
            if not text[start:end].strip():
                start = end + 3
                iscode = not iscode
                continue

        if iscode:
            ignore = False
            line_end = text.find(LF,start)
            for s in ignore_class:
                if s in text[start:line_end].split():
                    ignore = True
                    break

            if ignore:
                start = line_end
                md = text[start:end].strip()
                cell = add_md(md,True)
            else:
                
                last_LF = text.rfind(LF, 0, start) 
                if last_LF == -1:
                    ignore_chars = start -3
                else:
                    ignore_chars = start -last_LF -3 - len(LF)

                start = line_end

                codelist=text[start:end].strip('\r\n').splitlines(True)
                
                if ignore_chars:
                    codelist = [t[ignore_chars:] for t in codelist]

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
                
                if pre_type:
                    code = ''
                    for t in codelist:
                        pre ,sep, others = t.partition(sep_char)

                        if in_code:

                            if pre.startswith(pre_char) or '...' in pre:
                                code += others
                            else:
                                add_code(code) 
                                in_code = False
                                code = others if pre.startswith('Out[') else t
                        else:
                            if pre.startswith(pre_char):
                                add_md(code,True) 
                                in_code = True
                                code = others
                            else:
                                code += others if pre.startswith('Out') else t

                                
                    if code:
                        if in_code:
                            add_code(code)
                        else:
                            add_md(code,True)            

                else: 
                    code = ''.join(codelist)
                    add_code(code)
        else:
            md = text[start:end]
            cell = add_md(md)

        start = end + 3
        if start >= len(text) :
            loop = False
        iscode = not iscode

    return ipynb

    

def monitor_clipboard():

    if  data.hasHtml(): 
        text=html2md(data.html())
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
