# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'Control de Stock'
copyright = '2026, Federico'
author = 'Federico'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',    
    'sphinx.ext.viewcode',    
    'sphinx.ext.napoleon',      
    'sphinx.ext.intersphinx',  
    'sphinx.ext.autosummary',  
]

# Orden de documentacion: miembros en el orden en que aparecen en el codigo
autodoc_member_order = 'bysource'

# Muestra el tipo de los parametros automaticamente desde las anotaciones
autodoc_typehints = 'description'

# Intersphinx: permite referenciar la documentacion oficial de Python
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'peewee': ('https://docs.peewee-orm.com/en/latest/', None),
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']

# Opciones del tema Furo
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# Titulo de la barra lateral
html_title = f"{project} v{release}"