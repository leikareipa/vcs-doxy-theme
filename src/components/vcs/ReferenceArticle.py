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
]

def html(srcXmlFilename:str):
    xmlTree = ElementTree.parse(srcXmlFilename)

    # E.g. "file" or "class".
    articleType = xmlTree.find("./compounddef").attrib["kind"]

    # The specific thing being documented, e.g. "code_file.h".
    documenteeName = xmlTree.find("./compounddef/compoundname").text

    # For templated classes etc.
    if articleType in ["class", "struct"]:
        templateParams = xmlTree.findall("./compounddef/templateparamlist/param")
        if templateParams:
            params = []
            for param in templateParams:
                params.append(xml2html.recursively_convert_xml_element_to_html(param.find("./type")).strip())
            documenteeName += "&lt;{}&gt;".format(", ".join(params))
    elif articleType == "file":
        documenteeName = xmlTree.find("./compounddef/location").attrib["file"]

    return f"""
    <article class='{articleType} reference'>
        <header>
            {articleType.capitalize()} reference
            <span class='separator'>
                &#9654;
            </span>
            {documenteeName}
        </header>
        {BriefDescription.html(xmlTree)}
        {FunctionDeclarations.html(xmlTree)}
        {DataStructureDeclarations.html(xmlTree)}
        {EnumDeclarations.html(xmlTree)}
        {DetailedDescription.html(xmlTree)}
        {EnumDocumentation.html(xmlTree)}
        {FunctionDocumentation.html(xmlTree)}
    </article>
    """

def css():
    return """
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

    article.reference samp
    {
        font-family: "JetBrains Mono";
        font-size: 88%;
    }

    article.reference a,
    article.reference a:visited
    {
        font-weight: 500;
	    color: var(--link-color);
        text-decoration: none;
    }

    article.reference a:hover,
    article.reference a:visited:hover
    {
        text-decoration: underline;
    }

    article.reference h1
    {
        font-size: 160%;
        font-weight: 500;
    }

    article.reference h2
    {
        font-size: 125%;
        font-weight: 500;
    }

    article.reference h3
    {
        font-size: 100%;
        font-weight: 500;
    }

    article.reference h4
    {
        font-size: 100%;
        font-weight: normal;
        font-style: italic;
    }
    """
