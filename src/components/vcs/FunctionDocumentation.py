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
    html = ""

    def make_fn_documentation(functionElems:ElementTree.Element):
        nonlocal html

        for fnEl in functionElems:
            html += "<section id='{}' class='function {}'>".format(fnEl.attrib["id"], fnEl.find("./name").text)

            html += "<header>"
            html += "{}{}".format(fnEl.find("./definition").text, fnEl.find("./argsstring").text)
            html += "</header>"

            html += "<article class='description'>"
            for brief in fnEl.findall("./briefdescription/*"):
                html += xml2html.recursively_convert_xml_element_to_html(brief)
            for detailed in fnEl.findall("./detaileddescription/*"):
                html += xml2html.recursively_convert_xml_element_to_html(detailed)
            html += "</article>"

            html += "</section>\n"

        return html

    plainFunctions = tree.findall("./compounddef/sectiondef[@kind='func']/memberdef")
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
    """
