#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
import xml2html

def html(xmlFilename:str):
    xmlTree = ElementTree.parse(xmlFilename)

    return f"""
    <article class='markdown page'>
        <header>
            {xmlTree.find("./compounddef/title").text}
        </header>
        {xml2html.build_detailed_description(xmlTree, includeHeader=False)}
    </article>
    """

def css():
    return """
    """

def js():
    return """
    """
