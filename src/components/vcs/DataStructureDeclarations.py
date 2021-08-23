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
    from doxy2custom import XML_INDEX

    targetEl = tree.findall("./compounddef/innerclass")
    if not targetEl:
        return ""

    html = "<section id='data-structures'>"
    html += "<header><h1>Data structures</h1></header>"
    html += "<table class='data-structure-signatures'><tbody>"
    for child in targetEl:
        dataType = XML_INDEX.find(f"./compound[@refid='{child.attrib['refid']}']").attrib["kind"]
        srcFilename = xml2html.get_html_filename_of_refid(child.attrib["refid"])
        html += "<tr>"
        html += f"<td class='type'>{dataType}</td>"
        html += "<td class='name'><a href='./{}#{}'>{}</a></td>".format(srcFilename, child.attrib["refid"], child.text)
        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def css():
    return """
    table.data-structure-signatures
    {
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    table.data-structure-signatures tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    table.data-structure-signatures td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    table.data-structure-signatures td
    {
        padding: 6px;
    }

    table.data-structure-signatures td.type
    {
        text-align: right;
        white-space: nowrap;
    }

    table.data-structure-signatures td.name
    {
        padding-left: 12px;
        width: 100%;
    }
    """
