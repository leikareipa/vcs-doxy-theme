#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from html import escape
import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    from doxy2custom import XML_INDEX

    targetEl = tree.findall("./compounddef/sectiondef[@kind='public-attrib']/memberdef")
    if not targetEl:
        return ""

    html = "<section id='data-fields'>"
    html += "<header><h1>Data fields</h1></header>"
    html += "<table class='data-field-signatures'><tbody>"
    for child in targetEl:
        # Note: We just want plain text - without e.g. hyperlinks - for the
        # type declaration.
        cType = escape(" ".join(child.find("./definition").text.split(" ")[0:-1]))
                
        html += "<tr>"
        html += f"<td class='type'>{cType}</td>"
        if xml2html.is_element_documented(child):
            href = xml2html.make_inter_doc_href_link(child.attrib["id"])
            html += "<td class='name'><a href='{}'>{}</a></td>".format(href, child.find("./name").text)
        else:
            html += "<td class='name'>{}</td>".format(child.find("./name").text)
        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def css():
    return """
    table.data-field-signatures
    {
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    table.data-field-signatures tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    table.data-field-signatures td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    table.data-field-signatures td
    {
        padding: 6px;
    }

    table.data-field-signatures td.type
    {
        text-align: right;
        white-space: nowrap;
    }

    table.data-field-signatures td.name
    {
        padding-left: 12px;
        width: 100%;
    }
    """
