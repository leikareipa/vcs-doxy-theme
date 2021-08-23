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
    html = ""

    def make_fn_table(functionElems:ElementTree.Element):
        nonlocal html
        if functionElems:
            html += "<table class='function-signatures'><tbody>"
            for fnEl in functionElems:
                # Note: We just want plain text - without e.g. hyperlinks - for the
                # return value declaration.
                retVal = " ".join(fnEl.find("./definition").text.split(" ")[0:-1])
                
                html += "<tr>"
                html += "<td class='return-value'>{}</td>".format(retVal)
                if xml2html.is_element_documented(fnEl):
                    srcFilename = xml2html.get_html_filename_of_refid(fnEl.attrib['id'])
                    html += "<td class='function'><a href='./{}#{}'>{}</a>{}</td>".format(srcFilename, fnEl.attrib["id"], fnEl.find("./name").text, fnEl.find("./argsstring").text)
                else:
                    html += "<td class='function'>{}{}</td>".format(fnEl.find("./name").text, fnEl.find("./argsstring").text)
                html += "</tr>\n"
            html += "</tbody></table>"
            html += "</section>"

        return html

    plainFunctions = tree.findall("./compounddef/sectiondef[@kind='func']/memberdef")
    if plainFunctions:
        html += f"""
        <section id='function-declarations'>
            <header>
                <h1>Functions</h1>
            </header>
            {make_fn_table(plainFunctions)}
        </section>
        """

    publicMemberFunctions = tree.findall("./compounddef/sectiondef[@kind='public-func']/memberdef")
    if publicMemberFunctions:
        html += f"""
        <section id='public-member-function-declarations'>
            <header>
                <h1>Public member functions</h1>
            </header>
            {make_fn_table(publicMemberFunctions)}
        </section>
        """

    return html

def css():
    return """
    table.function-signatures
    {
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    table.function-signatures tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    table.function-signatures td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    table.function-signatures td
    {
        padding: 6px;
    }

    table.function-signatures td.return-value
    {
        text-align: right;
        white-space: nowrap;
    }

    table.function-signatures td.function
    {
        padding-left: 12px;
        width: 100%;
    }
    """
