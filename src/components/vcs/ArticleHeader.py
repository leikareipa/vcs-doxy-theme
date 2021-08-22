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

    return f"""
    <header class='article-header'>
        <span class='article-type'>
            {articleType.capitalize()} reference
        </span>
        <i class='separator fas fa-caret-right'></i>
        <span class='article-target'>
            {documenteeName}
        </span>
    </header>
    """

def css():
    return """
    .article-header
    {
        display: flex;
        align-items: center;
        padding: 0 var(--article-horizontal-padding);
        border-bottom: 1px solid var(--element-border-color);
        background-color: var(--secondary-background-color);
        min-height: var(--header-height);
        box-sizing: border-box;
        position: sticky;
        top: 0;
        font-weight: 500;
    }

    .article-header .separator
    {
        color: #a2a2a2;
        margin: 0 8px;
    }
    """
