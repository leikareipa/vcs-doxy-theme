#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(xmlTree:ElementTree):
    # E.g. "file" or "class".
    articleType = xmlTree.find("./compounddef").attrib["kind"]
    indexUrl = ""

    # The specific thing being documented, e.g. "code_file.h".
    documenteeName = xmlTree.find("./compounddef/compoundname").text

    # For templated classes etc.
    if articleType in ["class", "struct"]:
        templateParams = xmlTree.findall("./compounddef/templateparamlist/param")
        if templateParams:
            params = []
            for param in templateParams:
                params.append(xml2html.xml_element_to_html(param.find("./type")).strip())
            documenteeName += "&lt;{}&gt;".format(", ".join(params))
        indexUrl = "./index=data_structures.html"
    elif articleType == "file":
        documenteeName = xmlTree.find("./compounddef/location").attrib["file"]
        indexUrl = "./index=files.html" ## TODO: Don't hard-code these URLs.
    elif articleType == "page":
        documenteeName = xmlTree.find("./compounddef/title").text
        indexUrl = "./index=pages.html"
    elif articleType == "doxy2custom":
        articleType = "Index"

    return f"""
    <header class='article-header'>
        <span class='crumb root'>
            <a href='./index.html'>VCS Dev Docs</a>
            <i class='separator fas fa-xs fa-chevron-right'></i>
        </span>
        <span class='crumb type'>
            <a {f'href="{indexUrl}"' if indexUrl else ''}>{articleType.capitalize()}</a>
            <i class='separator fas fa-xs fa-chevron-right'></i>
        </span>
        <span class='crumb target'>
            {documenteeName}
        </span>
    </header>
    """

def css():
    return """
    .article-header
    {
        font-size: 110%;
        display: flex;
        align-items: center;
        min-height: var(--article-header-height);
        box-sizing: border-box;
        margin: 1.5em 0;
        margin-top: 0;
        background-color: var(--secondary-background-color);
        padding: 1em;
        padding-left: calc((100% - min(var(--article-max-width), var(--article-width))) * 0.5 + 1rem);
        overflow: auto;
        white-space: nowrap;
        border-bottom: 1px solid var(--element-border-color);
    }

    .article-header .crumb
    {
        display: flex;
        align-items: center;
    }

    .article-header .separator
    {
        margin: 0 0.6em;
    }
    """
