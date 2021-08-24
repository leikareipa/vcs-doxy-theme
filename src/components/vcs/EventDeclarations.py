#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from html import escape
from functools import reduce
import xml2html
import re

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    from doxy2custom import XML_INDEX

    targetEl = tree.findall("./compounddef/sectiondef[@kind='var']/memberdef")
    targetEl = filter(lambda el: el.find("./definition").text.startswith("vcs_event_c"), targetEl)
    if not targetEl:
        return ""

    html = "<section id='events'>"
    html += "<header><h1>Events</h1></header>"
    html += "<table class='event-signatures'><tbody>"
    for child in targetEl:
        # Note: We just want plain text - without e.g. hyperlinks - for the
        # event parameter declaration.
        param = escape(" ".join(child.find("./definition").text.split(" ")[0:-1]))
        param = re.sub(r"^vcs_event_c(.*)", r"\1", param)
                
        html += "<tr>"
        html += "<td class='type'>"
        if xml2html.is_element_documented(child):
            href = xml2html.make_inter_doc_href_link(child.attrib["id"])
            html += "<a href='{}'>{}</a>".format(href, child.find("./name").text)
        else:
            html += "{}".format(child.find("./name").text)
        html += f" &rrarr; <span class='param'>{param}</span>"
        html += "</td>"
        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def css():
    return """
    table.event-signatures
    {
        width: 100%;
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    table.event-signatures tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    table.event-signatures td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    table.event-signatures td
    {
        padding: 6px;
        padding-left: 12px;
    }
    """
