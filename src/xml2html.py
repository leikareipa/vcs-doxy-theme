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
from functools import reduce

# Returns the filename of - and path to - the  output HTML file generated for
# the Doxygen XML source whose "refid" attribute matches the given refid string.
def get_html_output_filename_for_xml_refid(refId:str):
    from doxy2custom import OUTPUT_FILENAMES, XML_INDEX
    docElems = XML_INDEX.findall("./compound")
    for el in docElems:
        if (el.attrib["refid"] == refId or
            el.find(f"./member[@refid='{refId}']")):
            return OUTPUT_FILENAMES[el.attrib["refid"]]
    assert False, f"Couldn't find a filename for the given refid '{refId}'."

# Returns a path and anchor combination (e.g. "./html/struct_data_structure.html#abcde")
# that points to the location in the output HTML documentation of a given element from
# Doxygen's original XML format. The refId argument identifies the XML "refid" attribute
# of the target element (e.g. "capture_8h" for a header file called "capture.h"). The
# return string can be used e.g. as the "href" attribute in an <a> element.
def make_inter_doc_href_link(refId:str):
    srcFilename = get_html_output_filename_for_xml_refid(refId)
    return f"./{srcFilename}#{refId}"

def is_element_documented(el:ElementTree.Element):
    return len(el.find("./briefdescription")) or len(el.find("./detaileddescription"))

# Removes spaces around the insides of angle brackets. E.g. "std::vector< int >" ->
# "std::vector<int>"; "std::vector<const int * >" -> "std::vector<const int*>".
def strip_angle_bracket_spaces(string:str):
    string = re.sub(r"&lt; +", "&lt;", string)
    string = re.sub(r" +&gt;", "&gt;", string)
    string = re.sub(r" +((\*|&amp;)+)&gt;", r"\2&gt;", string)
    return string

# E.g. "const int &" -> "const int&".
def strip_leading_address_operator_spaces(string:str):
    string = re.sub(r" +((\*|&amp;)+)$", r"\2", string)
    return string

def xml_element_to_html(el:ElementTree.Element):
    if el == None:
        return ""

    text = ""
    subtext = ""

    elText = escape(el.text if el.text else "").replace("\n", "")
    elTail = escape(el.tail if el.tail else "").replace("\n", "")

    for subelement in el:
        subtext += xml_element_to_html(subelement)

    if el.tag == "para":
        # Certain HTML elements shouldn't be wrapped in <p> although the XML wraps then in <para>.
        if ((re.match(r"^<h\d ?.*?>", subtext) or    # Only a heading: e.g. <p><h1>...</h1></p>.
             re.match(r"^<(o|u)l ?.*?>", subtext) or # Only an ordered/unordered list: e.g. <p><ul>...</ul></p>.
             re.match(r"^<pre ?.*?>", subtext) or    # Only a code listing: <p><pre>...</pre></p>.
             re.match(r"^<a ?.*?>", subtext) or      # Only a link: <p><a>...</a></p>.
             re.match(r"^<div ?.*?>", subtext) or    # Only a block div: <p><div>...</div></p>.
             re.match(r"^<p ?.*?>", subtext))        # Nested <p>: <p><p>...</p></p>.
           and not str.strip(elText + elTail)):      # No other text, just the other wrapped element.
            text = subtext
        elif str.strip(elText + subtext):
            text = "<p>{}{}</p>".format(elText, subtext)
    elif el.tag == "orderedlist":
        text = "<ol>{}{}</ol>".format(elText, subtext)
    elif el.tag == "listitem":
        noParagrSubtext = re.sub(r"^<p>(.*?)</p>$", r"\1", subtext)
        text = "<li>{}{}</li>".format(elText, noParagrSubtext)
    elif el.tag == "name":
        text = elText
    elif el.tag == "memberdef":
        if str.strip(elText + subtext + elTail):
            text = "<p>{}{}{}</p>".format(elText, subtext, elTail)
    elif el.tag == "enumvalue":
        if str.strip(elText + subtext + elTail):
            text = "<p>{}{}{}</p>".format(elText, subtext, elTail)
    elif el.tag == "detaileddescription" or el.tag == "briefdescription":
        text = elText + subtext + elTail
    elif el.tag == "programlisting":
        text = "<pre class='program-listing'>{}{}</pre>{}".format(elText, subtext, elTail)
    elif el.tag == "codeline":
        text = "<code class='language-cpp'>{}{}</code>{}".format(elText or " ", subtext, elTail)
    elif el.tag == "highlight":
        text = elText + subtext + elTail
    elif el.tag == "ndash":
        text = "&ndash;" + elTail
    elif el.tag == "sp":
        text = " " + elTail
    elif el.tag == "ref":
        href = make_inter_doc_href_link(el.attrib["refid"])
        text = "<a href='{}'>{}{}</a>{}".format(href, elText, subtext, elTail)
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
    
    # For Markdown tables.
    elif el.tag == "table":
        text = f"{elText}<table>{subtext}</table>{elTail}"
    elif el.tag == "row":
        text = f"<tr>{subtext}</tr>"
    elif el.tag == "entry":
        if el.attrib["thead"] == "yes":
            text = f"<th>{subtext}</th>"
        else:
            text = f"<td>{subtext}</td>"

    # For function parameters.
    elif el.tag == "declname":
        text = elText + subtext + elTail
    elif el.tag == "type":
        text = elText + subtext + elTail

    elif el.tag == "image":
        text = "<img src='{}'>".format(el.attrib["name"])
    else:
        print("Unrecognized tag:", el.tag, file=sys.stderr)
        text = "<i style='background-color: crimson; color: white; padding: 10px 15px; display: inline-block; margin: 5px;'>&lt;{}&gt;</i>".format(el.tag)

    return text
