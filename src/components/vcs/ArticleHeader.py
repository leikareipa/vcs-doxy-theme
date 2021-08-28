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
        indexUrl = "./index=structures.html"
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
        <span class='type'>
            <a {f'href="{indexUrl}"' if indexUrl else ''}>{articleType.capitalize()}</a>
        </span>
        <i class='separator fas fa-sm fa-chevron-right'></i>
        <span class='target'>
            {documenteeName}
        </span>
    </header>
    """

def css():
    return """
    .article-header
    {
        font-size: 110%;
        color: whitesmoke;
        display: flex;
        align-items: center;
        padding: 0;
        height: var(--article-header-height);
        margin-top: -10px;
        box-sizing: border-box;
    }

    .article-header .separator
    {
        margin: 0 12px;
    }

    .article-header .type a[href]
    {
        font-weight: normal;
        color: inherit;
        border-bottom: 2px solid whitesmoke;
    }

    .article-header .type a:hover
    {
        text-decoration: none;
    }
    """
