#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#
# A reference article is derived directly from the source code; it documents things like
# header files, classes, structs, etc.
#

from xml.etree import ElementTree
import xml2html

def html(xmlFilename:str):
    xmlTree = ElementTree.parse(xmlFilename)

    # E.g. "file" or "class".
    articleType = xmlTree.find("./compounddef").attrib["kind"]

    # The specific thing being documented, e.g. "code_file.h".
    documenteeName = xmlTree.find("./compounddef/compoundname").text

    # For templated classes etc.
    if articleType in ["class", "struct"]:
        templateParams = xmlTree.findall("./compounddef/templateparamlist/param")
        if templateParams:
            params = []
            for param in templateParams:
                params.append(xml2html.recursively_convert_xml_element_to_html(param.find("./type")).strip())
            documenteeName += "&lt;{}&gt;".format(", ".join(params))
    elif articleType == "file":
        documenteeName = xmlTree.find("./compounddef/location").attrib["file"]

    return f"""
    <article class='{articleType} reference'>
        <header>
            {articleType.capitalize()} reference
            <span class='separator'>
                &#9654;
            </span>
            {documenteeName}
        </header>
        {xml2html.build_brief_description(xmlTree)}
        {xml2html.build_function_declaractions(xmlTree)}
        {xml2html.build_data_structure_declarations(xmlTree)}
        {xml2html.build_enum_declaractions(xmlTree)}
        {xml2html.build_detailed_description(xmlTree)}
        {xml2html.build_enum_documentation(xmlTree)}
        {xml2html.build_function_documentation(xmlTree)}
    </article>
    """

def css():
    return """
    """

def js():
    return f"""
    """
