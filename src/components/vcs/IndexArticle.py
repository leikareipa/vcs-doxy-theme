#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from src.components.vcs import (
    ArticleHeader,
    BriefDescription,
)
from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
    ArticleHeader,
    BriefDescription,
]

def _file_row(el:ElementTree.Element):
    from src.doxy2custom import OUTPUT_FILENAMES

    refid = el.attrib["refid"]
    xmlTree = ElementTree.parse(OUTPUT_FILENAMES[refid]["src"])
    brief = xml2html.xml_element_to_html(xmlTree.find("./compounddef/briefdescription"))
    path = xmlTree.find("./compounddef/location").attrib["file"]
    href = xml2html.make_inter_doc_href_link(refid)

    return f"""
    <tr>
        <td class='name'><a href='{href}'>{path}</a></td>
        <td class='description'>{brief}</td>
    </tr>
    """

def _page_row(el:ElementTree.Element):
    from src.doxy2custom import OUTPUT_FILENAMES

    refid = el.attrib["refid"]
    xmlTree = ElementTree.parse(OUTPUT_FILENAMES[refid]["src"])
    brief = xml2html.xml_element_to_html(xmlTree.find("./compounddef/briefdescription"))
    name = xmlTree.find("./compounddef/title").text
    href = xml2html.make_inter_doc_href_link(refid)

    return f"""
    <tr>
        <td class='name'><a href='{href}'>{name}</a></td>
    </tr>
    """

def _structure_row(el:ElementTree.Element):
    from src.doxy2custom import OUTPUT_FILENAMES

    refid = el.attrib["refid"]
    xmlTree = ElementTree.parse(OUTPUT_FILENAMES[refid]["src"])
    brief = xml2html.xml_element_to_html(xmlTree.find("./compounddef/briefdescription"))
    name = el.find("./name").text
    href = xml2html.make_inter_doc_href_link(refid)

    return f"""
    <tr>
        <td class='name'><a href='{href}'>{name}</a></td>
        <td class='description'>{brief}</td>
    </tr>
    """

def html(xmlTree:ElementTree, data:list):
    article = ""
    seeAlso = ""
    indexType = xmlTree.find("./compounddef/compoundname").text

    if indexType == "Files":
        article = "".join(list(map(_file_row, data)))
        seeAlso = """
            <span>See also <a href='./index=structures.html'>Index:Structures</a>
            and
            <a href='./index=pages.html'>Index:Pages</a>.</span>
        """
    elif indexType == "Structures":
        article = "".join(list(map(_structure_row, data)))
        seeAlso = """
            <span>See also <a href='./index=files.html'>Index:Files</a>
            and
            <a href='./index=pages.html'>Index:Pages</a>.</span>
        """
    elif indexType == "Pages":
        article = "".join(list(map(_page_row, data)))
        seeAlso = """
            <span>See also <a href='./index=files.html'>Index:Files</a>
            and
            <a href='./index=structures.html'>Index:Structures</a>.</span>
        """
    
    return f"""
    <article class='index file'>
        {ArticleHeader.html(xmlTree)}
        <div class='contents index'>
            {BriefDescription.html(xmlTree)}
            {seeAlso}
            <section id='index'>
                <table class='file-list'>
                    <tbody>
                        {article}
                    </tbody>
                </table>
            </section>
        </div>
    </article>
    """

def css():
    return """
    .contents.index
    {
        width: 100%;
        background-color: white;
        box-sizing: border-box;
        padding: var(--article-vertical-padding) var(--article-horizontal-padding);
        border-radius: 4px;
        overflow: hidden;
        box-shadow: inset 0 0 11px rgba(0, 0, 0, 0.5);
        min-height: calc(100vh - var(--article-header-height) - var(--header-height) - var(--content-spacing));
    }

    article.index #brief-description
    {
        display: inline;
    }
    
    article.index tr:not(.highlightable):hover
    {
        background-color: var(--secondary-background-color);
    }

    article.index td > p
    {
        margin: 0;
    }

    article.index h1
    {
        font-size: 160%;
        font-weight: 500;
    }

    article.index h2
    {
        font-size: 125%;
        font-weight: 500;
    }

    article.index h3
    {
        font-size: 100%;
        font-weight: 500;
    }

    article.index h4
    {
        font-size: 100%;
        font-weight: normal;
        font-style: italic;
    }

    article.index table
    {
        margin-top: var(--content-spacing);
        width: 100%;
        border: 1px solid var(--element-border-color);
        border-collapse: collapse;
    }

    article.index table tr:not(:last-child)
    {
        border-bottom: 1px solid var(--element-border-color);
    }

    article.index table td:not(:last-child)
    {
        border-right: 1px solid var(--element-border-color);
    }

    article.index table td
    {
        padding: 6px;
    }

    article.index table td.name
    {
        white-space: nowrap;
    }

    article.index table td.description
    {
        padding-left: 12px;
        width: 100%;
    }
    """
