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

def html(tree:ElementTree):
    targetEl = tree.find("./compounddef/detaileddescription")
    if not targetEl:
        return ""
    
    html = "<section id='detailed-description'>"
    html += "<header><h1>Detailed description</h1></header>"

    for child in targetEl:
        html += xml2html.recursively_convert_xml_element_to_html(child) + "\n"

    html += "</section>"

    return html

def css():
    return """
    """
