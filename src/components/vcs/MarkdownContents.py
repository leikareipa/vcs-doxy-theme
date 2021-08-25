#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from src.components.vcs import (
    MarkdownContents,
)
from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
    MarkdownContents,
]

def html(xmlFilename:str):
    xmlTree = ElementTree.parse(xmlFilename)

    return f"""
    <article class='markdown-page'>
        <header>
            {xmlTree.find("./compounddef/title").text}
        </header>
        {MarkdownContents.html(xmlTree)}
    </article>
    """

def css():
    return """

    article.markdown-page td > p
    {
        margin: 0;
    }

    article.markdown-page pre
    {
        display: flex;
        flex-direction: column;
        background-color: white;
        border: 1px solid var(--element-border-color);
        border-radius: 7px;
        margin: var(--section-vertical-margin) 0;
        margin-top: var(--section-vertical-margin);
        margin-bottom: var(--section-vertical-margin);
        padding: 16px;
        overflow: auto;
    }

    article.markdown-page pre > code
    {
        font-family: "JetBrains Mono";
        font-size: 88%;
        font-variant-ligatures: none;
        line-height: 1.35em;
    }

    article.markdown-page samp
    {
        font-family: "JetBrains Mono";
        font-size: 88%;
    }

    article.markdown-page a,
    article.markdown-page a:visited
    {
        font-weight: 500;
	    color: var(--link-color);
        text-decoration: none;
    }

    article.markdown-page a:hover,
    article.markdown-page a:visited:hover
    {
        text-decoration: underline;
    }

    article.markdown-page h1
    {
        font-size: 160%;
        font-weight: 500;
    }

    article.markdown-page h2
    {
        font-size: 125%;
        font-weight: 500;
    }

    article.markdown-page h3
    {
        font-size: 100%;
        font-weight: 500;
    }

    article.markdown-page h4
    {
        font-size: 100%;
        font-weight: normal;
        font-style: italic;
    }
    """
