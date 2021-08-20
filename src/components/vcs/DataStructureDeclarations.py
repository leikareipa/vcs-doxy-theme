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
    targetEl = tree.findall("./compounddef/innerclass")
    if not targetEl:
        return ""

    html = "<section id='data-structures'>"
    html += "<header><h1>Data structures</h1></header>"
    html += "<table class='data-structure-signatures'><tbody>"
    for child in targetEl:
        dataType = xml2html.query_xml_index(f"./compound[@refid='{child.attrib['refid']}']").attrib["kind"]
        html += "<tr>"
        html += f"<td>{dataType}</td>"
        html += "<td><a href='#{}'>{}</a></td>".format(child.attrib["refid"], child.text)
        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def css():
    return """
    """
