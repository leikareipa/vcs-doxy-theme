#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#
# Converts Doxygen's (v1.8) XML output into HTML.
#

import re
import sys
from xml.etree import ElementTree
from html import escape

def build_function_declaractions(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='func']/memberdef")
    if not targetEl:
        return ""

    html = "<article id='function-declarations'>"
    html += "<h1>Functions</h1>"
    html += "<table><tbody>"
    for fnEl in targetEl:
        html += "<tr>"
        html += "<td>{}</td>".format(fnEl.find("./type").text)
        html += "<td><a href='#{}'>{}</a>{}</td>".format(fnEl.attrib["id"], fnEl.find("./name").text, fnEl.find("./argsstring").text)
        html += "</tr>"
    html += "</tbody></table>"
    html += "</article>"

    return html

def build_function_documentation(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='func']/memberdef")
    if not targetEl:
        return ""
        
    html = "<article id='function-documentation'>"
    html += "<h1>Function documentation</h1>"
    for fnEl in targetEl:
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

        html += "</section>"
    html += "</article>"

    return html

def build_enum_declaractions(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='enum']/memberdef")
    if not targetEl:
        return ""

    html = "<article id='enum-declarations'>"
    html += "<h1>Enumerations</h1>"
    html += "<table><tbody>"
    enumElements = targetEl
    for enumEl in enumElements: 
        html += "<tr>"
        html += "<td>enum</td>"
        print(enumEl.tag, file=sys.stderr)

        if enumEl.attrib["id"]:
            html += "<td><a href='#{}'>{}</a> {{ ".format(enumEl.attrib["id"], enumEl.find("./name").text)
        else:
            html += "<td>{} {{ ".format(enumEl.find("./name").text)
        values = []
        for value in enumEl.findall("./enumvalue"):
            if value.attrib["id"]:
                values.append("<a href='#{}'>{}</a>".format(value.attrib["id"], value.find("./name").text))
            else:
                values.append(value.find("./name").text)
        html += ", ".join(values)
        html += " } </td>"
        html += "</tr>"
    html += "</tbody></table>"
    html += "</article>"

    return html

def build_enum_documentation(tree:ElementTree):
    targetEl = tree.findall("./compounddef/sectiondef[@kind='enum']/memberdef")
    if not targetEl:
        return ""
        
    html = "<article id='enum-documentation'>"
    html += "<h1>Enumeration type documentation</h1>"
    for child in targetEl:
        html += "<section id='{}' class='enum {}'>".format(child.attrib["id"], child.find("./name").text)

        html += "<header>"
        html += "enum {}".format(child.find("./name").text)
        html += "</header>"

        html += "<article class='description'>"
        for brief in child.findall("./briefdescription/*"):
            html += recursively_convert_xml_element_to_html(brief)
        for detailed in child.findall("./detaileddescription/*"):
            html += recursively_convert_xml_element_to_html(detailed)
        html += "</article>"

        html += "<article class='values'>"
        html += "<table><tbody>"
        for enum in child.findall("./enumvalue"):
            html += "<tr id='{}'>".format(enum.attrib["id"])
            html += "<td>{}</td>".format(enum.find("./name").text)
            html += "<td>{}</td>".format(recursively_convert_xml_element_to_html(enum.find("./detaileddescription")))
            html += "</tr>"
        html += "</tbody></table>"
        html += "</article>"

        html += "</section>"
    html += "</article>"

    return html

def build_detailed_description(tree:ElementTree):
    targetEl = tree.find("./compounddef/detaileddescription")
    if not targetEl:
        return ""
    
    html = "<article id='detailed-description'>"
    html += "<h1>Detailed description</h1>"
    for child in targetEl:
        html += recursively_convert_xml_element_to_html(child)
    html += "</article>"

    return html

def build_brief_description(tree:ElementTree):
    targetEl = tree.find("./compounddef/briefdescription")
    if not targetEl:
        return ""

    html = "<article id='brief-description'>"

    for child in targetEl:
        html += recursively_convert_xml_element_to_html(child)

    if tree.find("./compounddef/detaileddescription"):
        html += "<a href='#detailed-description'>More...</a>"

    html += "</article>"

    return html

def recursively_convert_xml_element_to_html(el:ElementTree.Element):
    text = ""
    subtext = ""

    elText = escape(el.text if el.text else "")
    elTail = escape(el.tail if el.tail else "")

    for subelement in el:
        subtext += recursively_convert_xml_element_to_html(subelement)

    if el.tag == "para":
        # Certain HTML elements shouldn't be wrapped in <p> although the XML wraps then in <para>.
        if (re.match(r"^<h\d ?.*?>", subtext) or     # Headers.
            re.match(r"^<(o|u)l ?.*?>", subtext) or  # Ordered/unordered lists.
            re.match(r"^<pre ?.*?>", subtext) or     # Code listings.
            (re.match(r"^<a ?.*?>", subtext) and not str.strip(elText + elTail))): # <p><a>...</a></p> Only wrapping a link, with no other content.
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
    elif el.tag == "detaileddescription":
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
        text = elText + elTail
    elif el.tag == "sp":
        text = " " + elTail
    elif el.tag == "ref":
        text = "<a href='#{}'>{}{}</a>{}".format(el.attrib["refid"], elText, subtext, elTail)
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
    else:
        print("Unrecognized tag:", el.tag, file=sys.stderr)
        text = "<i style='background-color: crimson; color: white; padding: 10px 15px; display: inline-block; margin: 5px;'>&lt;{}&gt;</i>".format(el.tag)

    return text

tree = ElementTree.parse("capture_8h.xml")

html = ""
html += build_brief_description(tree) + "\n"
html += build_enum_declaractions(tree) + "\n"
html += build_function_declaractions(tree) + "\n"
html += build_detailed_description(tree) + "\n"
html += build_enum_documentation(tree) + "\n"
html += build_function_documentation(tree) + "\n"

print(html)
