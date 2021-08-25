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
    targetEl = tree.find("./compounddef/briefdescription")

    html = "<section id='brief-description'>"

    if not targetEl:
        html += "<p>No description yet.</p>"
    else:
        for child in targetEl:
            html += xml2html.xml_element_to_html(child)
        if tree.find("./compounddef/detaileddescription"):
            html += "<a href='#detailed-description'>More...</a>"

    html += "</section>"

    return html

def css():
    return """
    #brief-description > *
    {
        display: inline;
    }
    """
