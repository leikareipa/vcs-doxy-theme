#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from src import xml2html

NO_DESCRIPTION_TEXT = "No description yet."

# The sub-components used in this component.
childComponents:Final = [
]

def string(tree:ElementTree):
    targetEl = tree.find("./compounddef/briefdescription")
    text = ""

    if targetEl:
        for child in targetEl:
            if hasattr(child, "text"):
                text += child.text
    else:
        text = NO_DESCRIPTION_TEXT

    return str.strip(text)

def html(tree:ElementTree):
    targetEl = tree.find("./compounddef/briefdescription")

    html = "<section id='brief-description'>"

    if not targetEl:
        html += f"<p>{NO_DESCRIPTION_TEXT}</p>"
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
