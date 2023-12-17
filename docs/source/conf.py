# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pymmdb'
copyright = '2023, Jiawei Li'
author = 'Jiawei Li'
release = 'v1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['recommonmark', 'nbsphinx', 'sphinx_markdown_tables'] # 'sphinx_markdown_tables'

templates_path = ['_templates']
exclude_patterns = []
smartquotes = True  # open smartquotes
smartquotes_action = 'qe'  # open smartquotes and escape quotes

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_theme = 'classic'
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/logo.png"
html_theme_options = {
    'vcs_pageview_mode': 'blob',
    "logo_only": True
}

html_context = {
    "display_github": False,
    "last_updated": True,
    "commit": False,
}
