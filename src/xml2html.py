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
        text = "<code>{}{}</code>{}".format(elText or " ", subtext, elTail)
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
