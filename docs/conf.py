# -*- coding: utf-8 -*-
# grs-service documentation build configuration file
#
import os
import sys

sys.path.insert(0, os.path.abspath('../src'))

import sphinx_rtd_theme

extensions = [
        'sphinx.ext.autodoc',
        'sphinxcontrib.httpdomain',
        'sphinxcontrib.autohttp.flask',
        'sphinxcontrib.autohttp.flaskqref'
]

templates_path = ['_templates']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
project = u'GRS Service'
copyright = u'2020, Open-DNA'
author = u'Open-DNA'
version = u'0.0.1.0'
release = u'0.0.1'
language = 'en'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

html_show_sourcelink = False
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
html_style = 'css/opendna_theme.css'
html_logo = '_static/logo.png'
html_theme_options = {
    'display_version': False
}

intersphinx_mapping = {
}
