#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#
# A reference article is derived directly from the source code; it documents things like
# header files, classes, structs, etc.
#

from components.vcs import (
    BriefDescription,
    DetailedDescription,
    FunctionDeclarations,
    EnumDeclarations,
    EnumDocumentation,
    FunctionDocumentation,
    DataStructureDeclarations,
    ArticleHeader,
)
from xml.etree import ElementTree
from typing import Final
import xml2html

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
]

def html(srcXmlFilename:str):
    xmlTree = ElementTree.parse(srcXmlFilename)

    # E.g. "file" or "class".
    articleType = xmlTree.find("./compounddef").attrib["kind"]

    return f"""
        <article class='{articleType} reference'>
            {ArticleHeader.html(xmlTree)}
            <div class='contents article'>
                {BriefDescription.html(xmlTree)}
                {FunctionDeclarations.html(xmlTree)}
                {DataStructureDeclarations.html(xmlTree)}
                {EnumDeclarations.html(xmlTree)}
                {DetailedDescription.html(xmlTree)}
                {EnumDocumentation.html(xmlTree)}
                {FunctionDocumentation.html(xmlTree)}
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
        box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.15), 0 0 18px white;
        border-radius: 7px;
        border: 1px solid lightgray;
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
    }
    """
