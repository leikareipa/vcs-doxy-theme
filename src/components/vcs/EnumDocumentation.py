#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from functools import reduce
import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='enum']/memberdef")
    if not targetEl:
        return ""
        
    html = "<section id='enum-documentation'>"
    html += "<header><h1>Enumeration type documentation</h1></header>"
    for child in targetEl:
        html += "<article id='{}' class='enum {}'>".format(child.attrib["id"], child.find("./name").text)

        html += "<header>"
        html += "enum {}".format(child.find("./name").text)
        html += "</header>"

        html += "<section class='description'>"
        for brief in child.findall("./briefdescription/*"):
            html += xml2html.recursively_convert_xml_element_to_html(brief)
        for detailed in child.findall("./detaileddescription/*"):
            html += xml2html.recursively_convert_xml_element_to_html(detailed)
        html += "</section>"

        values = child.findall("./enumvalue")
        numValDocumented = reduce(lambda numDocumented, valueEl: (numDocumented + xml2html.is_element_documented(valueEl)), values, 0)
        if numValDocumented:
            html += "<section class='values'>"
            html += "<table><tbody>"
            for value in values:
                html += "<tr id='{}'>".format(value.attrib["id"])
                html += "<td>{}</td>".format(value.find("./name").text)
                if xml2html.is_element_documented(value):
                    brief = xml2html.recursively_convert_xml_element_to_html(value.find("./briefdescription"))
                    detailed = xml2html.recursively_convert_xml_element_to_html(value.find("./detaileddescription"))
                    html += f"<td>{brief}{detailed}</td>"
                else:
                    html += "<td><p>&mdash;</p></td>"
                html += "</tr>\n"
            html += "</tbody></table>"
            html += "</section>"

        html += "</article>"
    html += "</section>"

    return html

def css():
    return """
    """
