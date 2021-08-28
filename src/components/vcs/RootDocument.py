#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from src.components.vcs import (
    ReferenceArticle,
    MarkdownArticle,
    RootDocumentHeader,
    IndexArticle,
    ResponsiveStyling,
)
from typing import Final
from functools import reduce

# The sub-components used in this component.
childComponents:Final = [
    ReferenceArticle,
    MarkdownArticle,
    RootDocumentHeader,
    IndexArticle,
    ResponsiveStyling,
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
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;1,400;1,500&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400;1,500&display=swap">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.14.0/css/all.css" crossorigin="anonymous" integrity="sha384-HzLeBuhoNPvSl5KYnjx0BT+WB0QEEqLprO+NBkkk5gbc67FTaL7XIGa2w1L0Xbgc">
            <link rel="stylesheet" href="./css/index.css">
        </head>
        <body>
            <aside>
                {RootDocumentHeader.html(xmlTree)}
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
        --header-height: 32px;
        --article-header-height: 70px;
        --text-color: rgba(58, 58, 58);
        --heading-text-color: rgba(30, 30, 30);
    }

    body
    {
        font-family: Roboto, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #3c3c3c;
        color: var(--text-color);
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
        overflow-y: scroll;
    }

    main > article
    {
        margin: 0 auto;
        width: 60%;
        max-width: 1400px;
        padding-bottom: var(--content-spacing);
    }

    article section header
    {
        color: var(--heading-text-color);
    }

    article a,
    article a:visited
    {
        font-weight: 500;
	    color: var(--link-color);
        text-decoration: none;
    }

    article a:not([href]),
    article a:not([href]):visited
    {
        color: inherit;
        text-decoration: none;
        font-weight: inherit;
    }

    article a:hover,
    article a:visited:hover
    {
        text-decoration: underline;
    }

    article a:not([href]):hover,
    article a:not([href]):visited:hover
    {
        text-decoration: none;
    }

    article h1,
    article h2,
    article h3,
    article h4,
    article h5
    {
        color: var(--heading-text-color);
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

    article .interjection > .label
    {
        font-weight: 500;
    }

    article .interjection > *
    {
        display: inline;
    }

    article .interjection
    {
        margin: 16px 0;
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
        transition: background-color 0.5s ease;
    }

    .highlightable.highlight
    {
        transition: background-color 0s ease;
    }

    .highlightable.highlight
    {
        background-color: #ffff0040 !important;
    }
    """

    subComponents = _get_dependent_components(childComponents)

    return reduce(lambda styleSheet, child: (styleSheet + child.css()), subComponents, selfSheet)
