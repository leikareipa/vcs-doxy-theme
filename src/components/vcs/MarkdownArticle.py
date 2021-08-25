#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from src.components.vcs import (
    ArticleHeader,
)
from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
    ArticleHeader,
]

def html(xmlTree:ElementTree):
    targetEl = xmlTree.find("./compounddef/detaileddescription")
    if not targetEl:
        return ""

    description = "\n".join(map(xml2html.xml_element_to_html, targetEl))

    return f"""
    <article class='page'>
        {ArticleHeader.html(xmlTree)}
        <div class='contents page'>
            {description}
        </div>
    </article>
    """

def css():
    return """
    .contents.page
    {
        width: 100%;
        background-color: white;
        box-sizing: border-box;
        padding: var(--article-vertical-padding) var(--article-horizontal-padding);
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3), 0 0 18px white;
        border-radius: 7px;
        border: 1px solid lightgray;
    }
    """
