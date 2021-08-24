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
    detailed = tree.find("./compounddef/detaileddescription")
    brief = tree.find("./compounddef/briefdescription")

    if not detailed or not brief:
        return ""
    
    html = "<section class='anchor' id='detailed-description'>"
    html += "<header><h1>Detailed description</h1></header>"

    for child in brief:
        html += xml2html.xml_element_to_html(child) + "\n"

    for child in detailed:
        html += xml2html.xml_element_to_html(child) + "\n"

    html += "</section>"

    return html

def css():
    return """
    """
