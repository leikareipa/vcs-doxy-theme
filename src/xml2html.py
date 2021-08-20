#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#
# Provides functionality to convert Doxygen's (v1.8) XML output into HTML.
#

import re
import sys
from xml.etree import ElementTree
from html import escape
from typing import Final
from functools import reduce

XML_INDEX:Final = ElementTree.parse("index.xml")

def query_xml_index(xpath:str = ""):
    global XML_INDEX
    return XML_INDEX.find(xpath)

def is_element_documented(el:ElementTree.Element):
    return len(el.find("./briefdescription")) or len(el.find("./detaileddescription"))

def build_function_declaractions(tree:ElementTree):
    html = ""

    def make_fn_table(functionElems:ElementTree.Element):
        nonlocal html
        if functionElems:
            html += "<table class='function-signatures'><tbody>"
            for fnEl in functionElems:
                html += "<tr>"
                html += "<td class='return-value'>{}</td>".format(recursively_convert_xml_element_to_html(fnEl.find("./type")))
                if is_element_documented(fnEl):
                    html += "<td class='function'><a href='#{}'>{}</a>{}</td>".format(fnEl.attrib["id"], fnEl.find("./name").text, fnEl.find("./argsstring").text)
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

def build_function_documentation(tree:ElementTree):
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
                html += recursively_convert_xml_element_to_html(brief)
            for detailed in fnEl.findall("./detaileddescription/*"):
                html += recursively_convert_xml_element_to_html(detailed)
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

def build_enum_declaractions(tree:ElementTree):
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
            if is_element_documented(value):
                values.append("<a href='#{}'>{}</a>".format(value.attrib["id"], value.find("./name").text))
            else:
                values.append(value.find("./name").text)
        html += ", ".join(values)
        html += " } </td>\n"

        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html

def build_enum_documentation(tree:ElementTree):
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
            html += recursively_convert_xml_element_to_html(brief)
        for detailed in child.findall("./detaileddescription/*"):
            html += recursively_convert_xml_element_to_html(detailed)
        html += "</section>"

        values = child.findall("./enumvalue")
        numValDocumented = reduce(lambda numDocumented, valueEl: (numDocumented + is_element_documented(valueEl)), values, 0)
        if numValDocumented:
            html += "<section class='values'>"
            html += "<table><tbody>"
            for value in values:
                html += "<tr id='{}'>".format(value.attrib["id"])
                html += "<td>{}</td>".format(value.find("./name").text)
                if is_element_documented(value):
                    brief = recursively_convert_xml_element_to_html(value.find("./briefdescription"))
                    detailed = recursively_convert_xml_element_to_html(value.find("./detaileddescription"))
                    html += f"<td>{brief}{detailed}</td>"
                else:
                    html += "<td><p>&mdash;</p></td>"
                html += "</tr>\n"
            html += "</tbody></table>"
            html += "</section>"

        html += "</article>"
    html += "</section>"

    return html

def build_data_structure_declarations(tree:ElementTree):
    targetEl = tree.findall("./compounddef/innerclass")
    if not targetEl:
        return ""

    html = "<section id='data-structures'>"
    html += "<header><h1>Data structures</h1></header>"
    html += "<table class='data-structure-signatures'><tbody>"
    for child in targetEl:
        dataType = query_xml_index(f"./compound[@refid='{child.attrib['refid']}']").attrib["kind"]
        html += "<tr>"
        html += f"<td>{dataType}</td>"
        html += "<td><a href='#{}'>{}</a></td>".format(child.attrib["refid"], child.text)
        html += "</tr>"
    html += "</tbody></table>"
    html += "</section>"

    return html
        
def build_detailed_description(tree:ElementTree, includeHeader:bool = True):
    targetEl = tree.find("./compounddef/detaileddescription")
    if not targetEl:
        return ""
    
    html = "<section id='detailed-description'>"

    if includeHeader:
        html += "<header><h1>Detailed description</h1></header>"

    for child in targetEl:
        html += recursively_convert_xml_element_to_html(child) + "\n"

    html += "</section>"

    return html

def build_brief_description(tree:ElementTree):
    targetEl = tree.find("./compounddef/briefdescription")
    if not targetEl:
        return ""

    html = "<section id='brief-description'>"

    for child in targetEl:
        html += recursively_convert_xml_element_to_html(child)

    if tree.find("./compounddef/detaileddescription"):
        html += "<a href='#detailed-description'>More...</a>"

    html += "</section>"

    return html

def recursively_convert_xml_element_to_html(el:ElementTree.Element):
    text = ""
    subtext = ""

    elText = escape(el.text if el.text else "").replace("\n", "")
    elTail = escape(el.tail if el.tail else "").replace("\n", "")

    for subelement in el:
        subtext += recursively_convert_xml_element_to_html(subelement)

    if el.tag == "para":
        # Certain HTML elements shouldn't be wrapped in <p> although the XML wraps then in <para>.
        if (re.match(r"^<h\d ?.*?>", subtext) or    # Only a heading: e.g. <p><h1>...</h1></p>.
            re.match(r"^<(o|u)l ?.*?>", subtext) or # Only an ordered/unordered list: e.g. <p><ul>...</ul></p>.
            re.match(r"^<pre ?.*?>", subtext) or    # Only a code listing: <p><pre>...</pre></p>.
            re.match(r"^<a ?.*?>", subtext)         # Only a link: <p><a>...</a></p>.
           and not str.strip(elText + elTail)): 
            text = elText + subtext
        elif el.text or subtext:
            text = "<p>{}{}</p>".format(elText, subtext)
    elif el.tag == "orderedlist":
        text = "<ol>{}{}</ol>".format(elText, subtext)
    elif el.tag == "listitem":
        noParagrSubtext = re.sub(r"^<p>(.*?)</p>$", r"\1", subtext)
        text = "<li>{}{}</li>".format(elText, noParagrSubtext)
    elif el.tag == "name":
        text = elText
    elif el.tag == "memberdef":
        text = "<p>{}{}{}</p>".format(elText, subtext, elTail)
    elif el.tag == "enumvalue":
        text = "<p>{}{}{}</p>".format(elText, subtext, elTail)
    elif el.tag == "detaileddescription" or el.tag == "briefdescription":
        text = elText + subtext + elTail
    elif el.tag == "programlisting":
        text = "<pre class='program-listing'>{}{}</pre>{}".format(elText, subtext, elTail)
    elif el.tag == "codeline":
        text = "<code>{}{}</code>{}".format(elText, subtext, elTail)
    elif el.tag == "highlight":
        text = elText + subtext + elTail
    elif el.tag == "ndash":
        text = "&ndash;" + elTail
    elif el.tag == "type":
        text = elText + subtext + elTail
    elif el.tag == "sp":
        text = " " + elTail
    elif el.tag == "ref":
        text = "<a href='#{}'>{}{}</a>{}".format(el.attrib["refid"], elText, subtext, elTail)
    elif el.tag == "ulink":
        text = "<a href='#{}'>{}{}</a>{}".format(el.attrib["url"], elText, subtext, elTail)
    elif el.tag == "emphasis":
        text = "<em>{}{}</em>{}".format(elText, subtext, elTail)
    elif el.tag == "computeroutput":
        text = "<samp>{}{}</samp>{}".format(elText, subtext, elTail)
    elif el.tag == "simplesect":
        if el.attrib["kind"] == "see":
            text = "<div class='interjection see-also'><span class='label'>See also </span>{}{}</div>{}".format(elText, subtext, elTail)
        elif el.attrib["kind"] == "note":
            text = "<div class='interjection note'><span class='label'>Note: </span>{}{}</div>{}".format(elText, subtext, elTail)
        elif el.attrib["kind"] == "warning":
            text = "<div class='interjection warning'><span class='label'>Warning: </span>{}{}</div>{}".format(elText, subtext, elTail)
        else:
            text = "<div class='interjection {}'>{}{}</div>{}".format(el.attrib["kind"], elText, subtext, elTail)
    elif el.tag == "heading":
        text = "<h{0}>{1}{2}</h{0}>{3}".format(el.attrib["level"], elText, subtext, elTail)
    elif el.tag == "table":
        text = "{}<table>{}</table>{}".format(elText, subtext, elTail)
    elif el.tag == "row":
        text = f"<tr>{subtext}</tr>"
    elif el.tag == "entry":
        if el.attrib["thead"] == "yes":
            text = f"<th>{subtext}</th>"
        else:
            text = f"<td>{subtext}</td>"
    elif el.tag == "image":
        text = "<img src='{}'>".format(el.attrib["name"])
    else:
        print("Unrecognized tag:", el.tag, file=sys.stderr)
        text = "<i style='background-color: crimson; color: white; padding: 10px 15px; display: inline-block; margin: 5px;'>&lt;{}&gt;</i>".format(el.tag)

    return text
