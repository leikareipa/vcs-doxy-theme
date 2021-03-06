#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from functools import reduce
from html import escape
from src import xml2html
import sys
import re

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    html = ""

    def make_fn_documentation(functionElems:ElementTree.Element):
        nonlocal html

        for fnEl in functionElems:
            assert xml2html.is_element_documented(fnEl), "Expected only documented elements"

            pType = xml2html.xml_element_to_html(fnEl.find("./type"))
            pType = xml2html.strip_angle_bracket_spaces(pType)
            pName = xml2html.xml_element_to_html(fnEl.find("./name"))

            html += f"<section class='data-field {pName}'>"
            html += "<header id='{}' class='anchor highlightable'>".format(fnEl.attrib["id"])
            html += f"<span class='type'>{pType}</span> <span class='name'>{pName}</span>"
            html += "</header>"

            html += "<article class='description'>"
            for brief in fnEl.findall("./briefdescription/*"):
                html += xml2html.xml_element_to_html(brief)
            for detailed in fnEl.findall("./detaileddescription/*"):
                html += xml2html.xml_element_to_html(detailed)
            html += "</article>"

            html += "</section>\n"

        return html

    dataFields = tree.findall("./compounddef/sectiondef[@kind='public-attrib']/memberdef")
    dataFields = list(filter(lambda el: xml2html.is_element_documented(el), dataFields))
    if dataFields:
        html += f"""
        <section id='data-field-documentation'>
            <header>
                <h1>Data field documentation</h1>
            </header>
            {make_fn_documentation(dataFields)}
        </section>
        """

    return html

def css():
    return """
    section.data-field
    {
        border: 1px solid var(--element-border-color);
    }

    section.data-field:not(:last-child)
    {
        margin-bottom: var(--content-spacing);
    }

    section.data-field > header
    {
        padding: 16px;
        border-bottom: 1px solid var(--element-border-color);
        background-color: var(--secondary-background-color);
        font-size: 105%;
    }

    section.data-field > header > *
    {
        margin-right: 0.2em;
    }
    
    section.data-field > header .name
    {
        font-style: italic;
    }

    section.data-field > header a,
    section.data-field > header a:visited
    {
        font-weight: normal;
    }

    section.data-field > article
    {
        padding: 0 16px;
    }
    """
