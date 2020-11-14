#!/usr/bin/env python3

# enable MathJax
extensions = [
    'sphinx.ext.mathjax'
]

# specify template path
templates_path = ['_templates']

# specify static path
html_static_path = ['content/static']
master_doc = 'content/en/index'
html_logo = 'content/static/logo.png'
html_favicon = 'content/static/favicon.ico'
html_show_copyright = False

# import markdown parser
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.md', '.rst']
templates_path = ['README.md'] # exclude file
exclude_patterns = ['_build', 'node_modules']

def setup(app):
    app.add_transform(AutoStructify)

def convert_npm_name(name):
    return name.upper().replace('_', ' ')

# project info
import json
fh = open('./package.json')
manifest = json.load(fh)
project = convert_npm_name(manifest['name'])
html_title = convert_npm_name(manifest['name'])
copyright = manifest['author']
author = manifest['author']
version = ''
release = ''
fh.close()

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes"]
