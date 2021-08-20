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
    targetEl = tree.findall("./compounddef/sectiondef[@kind='enum']/memberdef")
    if not targetEl:
        return ""

    html = "<section id='enum-declarations'>"
    html += "<header><h1>Enumerations</h1></header>"
    html += "<table class='enum-signatures'><tbody>"
    enumElements = targetEl
    for enumEl in enumElements:
        html += "<tr>"
        html += "<td class='type'>enum</td>"
        html += "<td class='enum'><a href='#{}'>{}</a> {{ ".format(enumEl.attrib["id"], enumEl.find("./name").text)
        
        values = []
        for value in enumEl.findall("./enumvalue"):
            if xml2html.is_element_documented(value):
                values.append("<a href='#{}'>{}</a>".format(value.attrib["id"], value.find("./name").text))
            else:
                values.append(value.find("./name").text)
        html += ", ".join(values)
        html += " } </td>\n"

        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def css():
    return """
    table.enum-signatures
    {
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    table.enum-signatures tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    table.enum-signatures td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    table.enum-signatures td
    {
        padding: 6px;
    }

    table.enum-signatures td.type
    {
        text-align: right;
    }

    table.enum-signatures td.enum
    {
        padding-left: 12px;
    }
    """
