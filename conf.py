# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
install_requires = [
    'sphinxcontrib-applehelp',
    'sphinxcontrib-devhelp',
    'sphinxcontrib-jsmath',
    'sphinxcontrib-htmlhelp>=2.0.0',
    'sphinxcontrib-serializinghtml>=1.1.5',
    'sphinxcontrib-qthelp',
    'Jinja2>=2.3',
    'Pygments>=2.0',
    'docutils=0.17.1',
    'snowballstemmer>=1.1',
    'babel>=1.3',
    'alabaster>=0.7,<0.8',
    'imagesize',
    'requests>=2.5.0',
    'setuptools',
    'packaging',
]

# -- Project information -----------------------------------------------------

project = 'SimpleUI'
copyright = '2020, Dmitry Vorontsov'
author = 'Dmitry Vorontsov'

# The full version, including alpha/beta/rc tags
release = '2.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ru'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'




# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
