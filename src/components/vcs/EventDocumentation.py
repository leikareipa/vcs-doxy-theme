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

    def make_documentation(eventElems:ElementTree.Element):
        nonlocal html

        for eventEl in eventElems:
            assert xml2html.is_element_documented(eventEl), "Expected only documented elements"

            param = xml2html.xml_element_to_html(eventEl.find("./type")).strip()
            param = xml2html.strip_angle_bracket_spaces(param)
            param = re.sub(r"^vcs_event_c(.*)", r"\1", param)
            name = xml2html.xml_element_to_html(eventEl.find("./name"))

            html += "<section class='event {}'>".format(name)
            html += "<header id='{}' class='anchor highlightable'>".format(eventEl.attrib["id"])
            html += f"""
            event
            <span class='name'>{name}</span>
            &rrarr;
            <span class='param'>{param}</span>
            """
            html += "</header>"

            html += "<article class='description'>"
            for brief in eventEl.findall("./briefdescription/*"):
                html += xml2html.xml_element_to_html(brief)
            for detailed in eventEl.findall("./detaileddescription/*"):
                html += xml2html.xml_element_to_html(detailed)
            html += "</article>"

            html += "</section>\n"

        return html

    events = tree.findall("./compounddef/sectiondef[@kind='var']/memberdef")
    events = filter(lambda el: xml2html.is_element_documented(el), events)
    events = filter(lambda el: el.find("./definition").text.startswith("vcs_event_c"), events)
    if any(events):
        html += f"""
        <section id='event-documentation'>
            <header>
                <h1>Event documentation</h1>
            </header>
            {make_documentation(events)}
        </section>
        """

    return html

def css():
    return """
    section.event
    {
        border: 1px solid var(--element-border-color);
    }

    section.event:not(:last-child)
    {
        margin-bottom: var(--content-spacing);
    }

    section.event > header
    {
        padding: 16px;
    }
    
    section.event > article
    {
        padding: 0 16px;
    }

    section.event > header
    {
        border-bottom: 1px solid var(--element-border-color);
        background-color: var(--secondary-background-color);
    }

    section.event .interjection > .label
    {
        font-weight: 500;
    }

    section.event .interjection > *
    {
        display: inline;
    }

    section.event .interjection
    {
        margin: 16px 0;
    }
    """
