#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from html import escape
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    from src.doxy2custom import XML_INDEX

    targetEl = tree.findall("./compounddef/sectiondef[@kind='public-attrib']/memberdef")
    if not targetEl:
        return ""

    html = "<section id='data-fields'>"
    html += "<header><h1>Data fields</h1></header>"
    html += "<table class='data-field-signatures'><tbody>"
    for child in targetEl:
        # Note: We just want plain text - without e.g. hyperlinks - for the
        # type declaration.
        cType = xml2html.strip_angle_bracket_spaces(escape(child.find("./definition").text))
        cType = " ".join(cType.split(" ")[0:-1])

        cName = escape(child.find("./name").text)
                
        html += "<tr>"
        html += f"<td class='type'>{cType}</td>"
        if xml2html.is_element_documented(child):
            href = xml2html.make_inter_doc_href_link(child.attrib["id"])
            html += "<td class='name'><a href='{}'>{}</a></td>".format(href, cName)
        else:
            html += "<td class='name'>{}</td>".format(cName)
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
        padding: 6px 12px;
    }

    table.data-field-signatures td.type
    {
        text-align: right;
        white-space: nowrap;
    }

    table.data-field-signatures td.name
    {
        width: 100%;
    }
    """
