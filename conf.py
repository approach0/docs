#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# enable MathJax
extensions = [
    'sphinx.ext.mathjax'
]

# specify template path 
templates_path = ['_templates']

# specify static path 
html_static_path = ['img']

# import markdown parser 
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

source_parsers = {
	'.md': CommonMarkParser,
}

source_suffix = ['.md', '.rst']

def setup(app):
    app.add_transform(AutoStructify)

# specify index file name
master_doc = 'index'

# project info
project = 'Approach0'
copyright = '2016, Wei Zhong'
author = 'Wei Zhong'
version = ''
release = ''
language = None
html_title = 'Approach0 docs'

# exclude directory
exclude_patterns = ['_build']

# syntax highlighting
pygments_style = 'sphinx'

# import sphinx_rtd_theme theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes"]

# logo
html_logo = 'logo.png'
html_favicon = 'favicon.ico'

html_show_copyright = False

# man page generation config
man_pages = [
    (master_doc, 'projectdocumentation', 'Project Documentation Documentation',
     [author], 1)
]
