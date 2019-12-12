# [clip2ipynb](https://github.com/steve-hao/clip2ipynb)

clip2ipynb is a Python script that monitor your system clipboard and converts HTML into ipynb notebook file.

``` 
Usage:  clip2ipynb.py

```

When script is running,it will monitor your system clipboard, if have some HTML format contents go in, then convert it into a ipynb notebook file

It analysis all code in `<pre>` Tag ,and split it into code and output

The output file is named notebook+timestamp (e.g. notebook191211165707.ipynb) on you current directory