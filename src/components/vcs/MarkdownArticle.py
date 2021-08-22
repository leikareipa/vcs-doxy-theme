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

def html(srcXmlFilename:str):
    xmlTree = ElementTree.parse(srcXmlFilename)

    targetEl = xmlTree.find("./compounddef/detaileddescription")
    if not targetEl:
        return ""
    
    html = "<section id='markdown-document'>"

    for child in targetEl:
        html += xml2html.xml_element_to_html(child) + "\n"

    html += "</section>"

    return html

def css():
    return """
    """
