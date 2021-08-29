#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from functools import reduce
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='enum']/memberdef")
    targetEl = list(filter(lambda el: xml2html.is_element_documented(el), targetEl))
    if not targetEl:
        return ""
        
    html = "<section id='enum-documentation'>"
    html += "<header><h1>Enumeration type documentation</h1></header>"
    for child in targetEl:
        assert xml2html.is_element_documented(child), "Expected only documented elements"

        isStrongEnum = child.attrib["strong"] == "yes"

        html += "<section class='enum {}'>".format(child.find("./name").text)
        html += "<header class='anchor highlightable' id='{}'>".format(child.attrib["id"])
        html += "<span class='type'>{}</span> {}".format("enum class" if isStrongEnum else "enum", child.find("./name").text)
        html += "</header>"

        html += "<article class='description'>"
        for brief in child.findall("./briefdescription/*"):
            html += xml2html.xml_element_to_html(brief)
        for detailed in child.findall("./detaileddescription/*"):
            html += xml2html.xml_element_to_html(detailed)
        html += "</article>"

        values = child.findall("./enumvalue")
        numValDocumented = reduce(lambda numDocumented, valueEl: (numDocumented + xml2html.is_element_documented(valueEl)), values, 0)
        if numValDocumented:
            html += "<article class='values'>"
            html += "<div class='table-container'><table class='values'><tbody>"
            for value in values:
                html += "<tr>"
                html += "<td class='value'>{}</td>".format(value.find("./name").text)
                if xml2html.is_element_documented(value):
                    brief = xml2html.xml_element_to_html(value.find("./briefdescription"))
                    detailed = xml2html.xml_element_to_html(value.find("./detaileddescription"))
                    html += f"<td class='description'>{brief}{detailed}</td>"
                else:
                    html += "<td class='description'><p>&mdash;</p></td>"
                html += "</tr>\n"
            html += "</tbody></table></div>"
            html += "</article>"

        html += "</section>"
    html += "</section>"

    return html

def css():
    return """
    section.enum
    {
        border: 1px solid var(--element-border-color);
    }

    section.enum .type
    {
        border: 1px solid lightgray;
        padding: 4px 5px;
        border-radius: 3px;
        background-color: var(--secondary-background-color);
        margin-right: 3px;
    }

    section.enum:not(:last-child)
    {
        margin-bottom: var(--content-spacing);
    }

    section.enum > header
    {
        padding: 16px;
    }
    
    section.enum > article
    {
        padding: 0 16px;
    }

    section.enum > header
    {
        border-bottom: 1px solid var(--element-border-color);
        background-color: var(--secondary-background-color);
    }
    
    section.enum .table-container
    {
        padding: 6px;
        border: 1px solid var(--element-border-color);
        border-radius: 7px;
        margin: 16px 0;
    }

    section.enum table.values
    {
        width: 100%;
        border-collapse: collapse;
    }

    section.enum table.values td
    {
        padding: 6px 8px;
    }

    section.enum table.values td.value
    {
        border-right: 1px solid var(--element-border-color);
        text-align: right;
        font-weight: 500;
        white-space: nowrap;
    }

    section.enum table.values td.description
    {
        width: 100%;
    }

    section.enum table.values tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }
    """
