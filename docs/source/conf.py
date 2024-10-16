# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'etacad'
copyright = '2024, Kevin Axel Tagliaferri'
author = 'Kevin Axel Tagliaferri'
release = '0.0.7'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for LaTex output -------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',  # Paper size.
    'pointsize': '10pt',     # Font size.
    'preamble': ''}         # Custom LaTex commands.

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_context = {
    "display_github": True,
    "github_user": "axeltag",
    "github_repo": "etacad",
    "github_version": "main",
    "conf_py_path": "/docs/source/"}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
