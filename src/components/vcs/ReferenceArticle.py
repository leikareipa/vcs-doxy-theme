#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#
# A reference article is derived directly from the source code; it documents things like
# header files, classes, structs, etc.
#

from src.components.vcs import (
    BriefDescription,
    DetailedDescription,
    FunctionDeclarations,
    EnumDeclarations,
    EnumDocumentation,
    FunctionDocumentation,
    DataStructureDeclarations,
    ArticleHeader,
    DataFieldDeclarations,
    DataFieldDocumentation,
    EventDeclarations,
    EventDocumentation,
)
from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
    BriefDescription,
    DetailedDescription,
    FunctionDeclarations,
    EnumDeclarations,
    EnumDocumentation,
    FunctionDocumentation,
    DataStructureDeclarations,
    ArticleHeader,
    DataFieldDeclarations,
    DataFieldDocumentation,
    EventDeclarations,
    EventDocumentation,
]

def html(xmlTree:ElementTree):
    articleType = xmlTree.find("./compounddef").attrib["kind"]

    return f"""
    <article class='{articleType} reference'>
        {ArticleHeader.html(xmlTree)}
        <div class='contents article'>
            {BriefDescription.html(xmlTree)}
            {FunctionDeclarations.html(xmlTree)}
            {DataStructureDeclarations.html(xmlTree)}
            {DataFieldDeclarations.html(xmlTree)}
            {EnumDeclarations.html(xmlTree)}
            {EventDeclarations.html(xmlTree)}
            {DetailedDescription.html(xmlTree)}
            {EnumDocumentation.html(xmlTree)}
            {FunctionDocumentation.html(xmlTree)}
            {EventDocumentation.html(xmlTree)}
            {DataFieldDocumentation.html(xmlTree)}
        </div>
    </article>
    """

def css():
    return """
    .contents.article
    {
        width: 100%;
        background-color: white;
        box-sizing: border-box;
        padding: var(--article-vertical-padding) var(--article-horizontal-padding);
        border-radius: 4px;
        overflow: hidden;
        box-shadow: inset 0 0 11px rgba(0, 0, 0, 0.5);
        min-height: calc(100vh - var(--article-header-height) - var(--header-height) - var(--content-spacing));
    }

    article.reference tr:not(.highlightable):hover
    {
        background-color: var(--secondary-background-color);
    }

    article.reference td > p
    {
        margin: 0;
    }

    article.reference pre
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

    article.reference pre > code
    {
        font-family: "JetBrains Mono";
        font-size: 88%;
        font-variant-ligatures: none;
        line-height: 1.35em;
    }

    article.reference pre > code .hljs-comment
    {
        color: #3e8220;
    }

    article.reference samp
    {
        font-family: "JetBrains Mono";
        font-size: 88%;
        padding: 0 4px;
        background-color: var(--secondary-background-color);
        border-radius: 7px;
    }

    article.reference article.description samp
    {
        transform: skew(-10deg, 0);
        display: inline-block;
        font-weight: 500;
    }
    """
