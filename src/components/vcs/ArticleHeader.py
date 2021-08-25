#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(xmlTree:ElementTree):
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
                params.append(xml2html.xml_element_to_html(param.find("./type")).strip())
            documenteeName += "&lt;{}&gt;".format(", ".join(params))
    elif articleType == "file":
        documenteeName = xmlTree.find("./compounddef/location").attrib["file"]
    elif articleType == "page":
        documenteeName = xmlTree.find("./compounddef/title").text
    elif articleType == "doxy2custom":
        articleType = "Index"

    return f"""
    <header class='article-header'>
        <span class='type'>
            {articleType.capitalize()}
        </span>
        <i class='separator fas fa-xs fa-chevron-right'></i>
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
        color: dimgray;
        display: flex;
        align-items: center;
        padding: 0;
        min-height: 65px;
        box-sizing: border-box;
    }

    .article-header .type
    {
        color: #a2a2a2;
    }

    .article-header .separator
    {
        color: #a2a2a2;
        margin: 0 8px;
    }
    """
