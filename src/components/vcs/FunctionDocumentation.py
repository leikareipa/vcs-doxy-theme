#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from functools import reduce
from html import escape
import xml2html
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

            retVal = xml2html.xml_element_to_html(fnEl.find("./type")).strip()
            retVal = xml2html.strip_angle_bracket_spaces(retVal)
            retVal = xml2html.strip_leading_address_operator_spaces(retVal)
            name = xml2html.xml_element_to_html(fnEl.find("./name")).strip()

            args = []
            for paramEl in fnEl.findall("./param"):
                pType = xml2html.xml_element_to_html(paramEl.find('./type')).strip()
                pType = xml2html.strip_angle_bracket_spaces(pType)
                pName = xml2html.xml_element_to_html(paramEl.find('./declname')).strip()

                # Assumes that <type> is followed by <declname>; we want things like
                # "unsigned &r" but not "unsignedr" or "unsigned & r", so we insert
                # a space after <type> (assumed to be between <type> and <declname
                # only if <type> doesn't end in a particular substring that we want
                # to keep attached to the subsequent <declname>.
                if pName and not re.search(r"(&amp;|\*)$", pType):
                    pType += " "

                args.append(f"<span class='param'><span class='type'>{pType}</span><span class='name'>{pName}</span></span>")

            html += "<section class='function {}'>".format(fnEl.find("./name").text)
            html += "<header id='{}' class='anchor highlightable'>".format(fnEl.attrib["id"])
            html += f"<span class='return'>{retVal}</span> <span class='signature'>{name}({', '.join(args)})</span>"
            html += "</header>"

            html += "<article class='description'>"
            for brief in fnEl.findall("./briefdescription/*"):
                html += xml2html.xml_element_to_html(brief)
            for detailed in fnEl.findall("./detaileddescription/*"):
                html += xml2html.xml_element_to_html(detailed)
            html += "</article>"

            html += "</section>\n"

        return html

    plainFunctions = tree.findall("./compounddef/sectiondef[@kind='func']/memberdef")
    plainFunctions = list(filter(lambda el: xml2html.is_element_documented(el), plainFunctions))
    if plainFunctions:
        html += f"""
        <section id='function-documentation'>
            <header>
                <h1>Function documentation</h1>
            </header>
            {make_fn_documentation(plainFunctions)}
        </section>
        """

    publicMemberFunctions = tree.findall("./compounddef/sectiondef[@kind='public-func']/memberdef")
    publicMemberFunctions = list(filter(lambda el: xml2html.is_element_documented(el), publicMemberFunctions))
    if publicMemberFunctions:
        html += f"""
        <section id='public-member-function-documentation'>
            <header>
                <h1>Public member function documentation</h1>
            </header>
            {make_fn_documentation(publicMemberFunctions)}
        </section>
        """

    return html

def css():
    return """
    section.function
    {
        border: 1px solid var(--element-border-color);
    }

    section.function:not(:last-child)
    {
        margin-bottom: var(--content-spacing);
    }

    section.function > header
    {
        padding: 16px;
    }
    
    section.function > article
    {
        padding: 0 16px;
    }

    section.function > header
    {
        border-bottom: 1px solid var(--element-border-color);
        background-color: var(--secondary-background-color);
    }

    section.function > header .param .name
    {
        font-style: italic;
    }
    """
