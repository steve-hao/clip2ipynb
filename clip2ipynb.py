from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication

from html2md import html2md,LF

from _datetime import datetime
import json



def md2ipynb(text):
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
            loop = False

        if iscode:
            code=text[start:end]
            cell = {}
            cell['metadata'] = {}
            cell['outputs'] = []
            cell['source'] = [code.strip()]
            cell['execution_count'] = None
            cell['cell_type'] = 'code'
        else:
            cell = {}
            cell['metadata'] = {}
            cell['source'] = [text[start:end].strip()]
            cell['cell_type'] = 'markdown'

        start = end + 3
        if start >= len(text) :
            loop = False
        ipynb['cells'].append(cell)
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
