#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from components.vcs import (
    ReferenceArticle,
    MarkdownArticle,
)
from typing import Final
from functools import reduce

# Iterates through all child components and their child components, and returns
# all visited components as a set.
def _get_dependent_components(componentTree:list, components:set = set()):
    for child in componentTree:
        components.add(child)
        if child.childComponents:
            _get_dependent_components(child.childComponents, components)
    return components

def html(srcXmlFilename:str):
    article = ReferenceArticle.html(srcXmlFilename)
    subComponents = _get_dependent_components([ReferenceArticle])
    styleSheet = reduce(lambda styleSheet, child: (styleSheet + child.css()), subComponents, css())

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>VCS Dev Docs</title>
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono&display=swap">
            <style>
                {styleSheet}
            </style>
        </head>
        <body>
            <aside>
                <header class='grand-header'>
                    <h1>VCS Dev Docs</h1>
                </header>
            </aside>
            <main>
                {article}
            </main>
        </body>
    </html>
    """

def css():
    return """
    :root
    {
        --element-border-color: #e0e0e0;
        --section-vertical-margin: 16px;
        --link-color: #0c64ee;
    }

    body
    {
        font-family: Roboto, sans-serif;
        margin: 0;
        padding: 0;
        
        /* Temporary.*/
        margin-left: 15%;
        width: 70%;
        min-width: 800px;
        border: 1px solid var(--element-border-color);
        padding: 0 40px;
        box-sizing: border-box;
    }

    p,
    .interjection
    {
        line-height: 1.35em;
    }
    """
