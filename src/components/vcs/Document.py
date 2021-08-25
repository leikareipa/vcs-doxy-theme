#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from components.vcs import (
    ReferenceArticle,
    MarkdownArticle,
    DocumentHeader,
    IndexArticle,
)
from typing import Final
from functools import reduce

# The sub-components used in this component.
childComponents:Final = [
    ReferenceArticle,
    MarkdownArticle,
    DocumentHeader,
    IndexArticle,
]

# Iterates through all child components and their child components, and returns
# all visited components as a set.
def _get_dependent_components(componentTree:list, components:set = set()):
    for child in componentTree:
        components.add(child)
        if child.childComponents:
            _get_dependent_components(child.childComponents, components)
    return components

def html(xmlTree:ElementTree, auxiliaryData:list = []):
    articleType = xmlTree.find("./compounddef").attrib["kind"]
    articleName = xmlTree.find("./compounddef/compoundname").text
    article = ""

    if articleType == "doxy2custom":
        article = IndexArticle.html(xmlTree, auxiliaryData)
    else:
        if articleName.endswith(".md") or articleName == "index":
            article = MarkdownArticle.html(xmlTree)
        else:
            article = ReferenceArticle.html(xmlTree)

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>VCS Dev Docs</title>
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <script src="./js/highlight.min.js"></script>
            <script>hljs.highlightAll()</script>
            <script>
                // Highlight the target element on anchor navigation.
                window.addEventListener('hashchange', ()=>{{
                    const elem = document.querySelector(window.location.hash);
                    if (elem && !elem.classList.contains('highlight')) {{
                        elem.classList.add('highlight');
                        setTimeout(()=>elem.classList.remove('highlight'), 1500);
                    }}
                }});
            </script>
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono&display=swap">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.14.0/css/all.css" crossorigin="anonymous" integrity="sha384-HzLeBuhoNPvSl5KYnjx0BT+WB0QEEqLprO+NBkkk5gbc67FTaL7XIGa2w1L0Xbgc">
            <link rel="stylesheet" href="./css/index.css">
        </head>
        <body>
            <aside>
                {DocumentHeader.html()}
            </aside>
            <main>
                {article}
            </main>
        </body>
    </html>
    """

def css():
    selfSheet = """
    :root
    {
        --element-border-color: #e0e0e0;
        --section-vertical-margin: 16px;
        --link-color: #0c64ee;
        --secondary-background-color: #f7f7f7;
        --article-horizontal-padding: 30px;
        --article-vertical-padding: 30px;
        --content-spacing: 30px;
        --header-height: 40px;
    }

    body
    {
        font-family: Roboto, sans-serif;
        margin: 0;
        padding: 0;
        background-color: var(--secondary-background-color);
    }

    p,
    .interjection
    {
        line-height: 1.35em;
    }

    main
    {
        position: fixed;
        top: var(--header-height);
        bottom: 0;
        width: 100%;
        overflow: auto;
    }

    main > article
    {
        margin-left: 20%;
        width: 60%;
        min-width: 800px;
        max-width: 1400px;
        padding-bottom: var(--content-spacing);
    }

    article a,
    article a:visited
    {
        font-weight: 500;
	    color: var(--link-color);
        text-decoration: none;
    }

    article a:hover,
    article a:visited:hover
    {
        text-decoration: underline;
    }

    article h1
    {
        margin-top: var(--content-spacing);
    }

    article .contents > h1:first-child
    {
        margin-top: 0;
    }

    article h2,
    article h3,
    article h4,
    article h5
    {
        margin-top: 16px;
    }

    article h1
    {
        font-size: 160%;
        font-weight: 500;
    }

    article h2
    {
        font-size: 125%;
        font-weight: 500;
    }

    article h3
    {
        font-size: 100%;
        font-weight: 500;
    }

    article h4
    {
        font-size: 100%;
        font-weight: normal;
        font-style: italic;
    }

    article li
    {
        padding: 5px 0;
    }

    .anchor
    {
        scroll-margin-top: 24px;
    }

    .highlightable
    {
        transition: background-color 0.75s ease;
    }

    .highlightable.highlight
    {
        transition: background-color 0s ease;
    }

    .highlightable.highlight
    {
        background-color: #f0e8fd !important;
    }
    """

    subComponents = _get_dependent_components(childComponents)

    return reduce(lambda styleSheet, child: (styleSheet + child.css()), subComponents, selfSheet)
