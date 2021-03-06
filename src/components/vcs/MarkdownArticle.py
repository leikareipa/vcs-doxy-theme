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
    {ArticleHeader.html(xmlTree)}
    <article class='page'>
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
        background-color: var(--article-background-color);
        box-sizing: border-box;
        overflow: hidden;
        padding: 0 1rem;
    }

    .contents.page *:last-child
    {
        margin-bottom: 0;
    }
    """
