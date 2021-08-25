#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

import re
import sys
import shutil
import os
from xml.etree import ElementTree
from typing import Final

OUTPUT_FILENAMES = {}
HTML_DST_PATH = "./doc"
XML_SRC_PATH = "./xml"
XML_INDEX:Final = ElementTree.parse(f"{XML_SRC_PATH}/index.xml")

# Remove any previous doc files. This is a bit dangerous, since the directory
# could contain other files as well, but hey.
if os.path.exists(HTML_DST_PATH):
    shutil.rmtree(HTML_DST_PATH)

# Recreate the output directory structure.
os.mkdir(HTML_DST_PATH)
os.makedirs(f"{HTML_DST_PATH}/js/")
os.makedirs(f"{HTML_DST_PATH}/css/")

# Copy external resource files.
shutil.copy2(f"./highlight.min.js", f"{HTML_DST_PATH}/js/")

# The source XML elements we'll produce HTML output for.
docElements = XML_INDEX.findall("./compound")
docElements = list(filter(lambda x: x.attrib["kind"] in ["page", "file", "struct", "class"], docElements))

# Map our custom output filenames to Doxygen's XML reference ids, so we'll know
# which output file corresponds to a given XML element.
for el in docElements:
    refid = el.attrib['refid']
    srcFilename = f"{XML_SRC_PATH}/{refid}.xml"

    if el.attrib["kind"] == "file":
        fileXml = ElementTree.parse(srcFilename)
        filePath = fileXml.find('./compounddef/location').attrib['file']
        filePath = re.sub(r"[^\w]", "_", filePath) # May cause duplicate strings for filenames that use non-ASCII (aA-zZ, 0-9) characters.
        dstPath = f"file={filePath}.html"
    else:
        if refid == "indexpage":
            dstPath = "index.html"
        else:
            dstPath = f"{el.attrib['kind']}={el.find('./name').text}.html"

    OUTPUT_FILENAMES[refid] = {
        "src": srcFilename,
        "dst": dstPath
    }

def convert_xml_to_html(htmlTemplate):
    def output(html:str, outputFilename:str):
        html = "\n".join([x.strip() for x in html.splitlines() if x.strip()])
        outFile = open(outputFilename, "w")
        outFile.write(html)
        outFile.close()

    for el in docElements:
        refid = el.attrib['refid']
        srcFilename = f"{XML_SRC_PATH}/{refid}.xml"
        dstFilename = f"{HTML_DST_PATH}/{OUTPUT_FILENAMES[refid]['dst']}"
        xmlTree = ElementTree.parse(srcFilename)
        output(htmlTemplate.html(xmlTree), dstFilename)

    # Generate a header file index.
    index = ElementTree.fromstring("""
    <doxygen>
        <compounddef kind='doxy2custom'>
            <compoundname>Header files</compoundname>
            <briefdescription><para>The following header files appear to have been documented.</para></briefdescription>
        </compounddef>
    </doxygen>
    """)
    files = list(filter(lambda el: el.attrib["kind"] in ["file"], docElements))
    files = list(filter(lambda el: el.find("./name").text.endswith(".h"), docElements))
    html = htmlTemplate.html(index, files)
    output(html, f"{HTML_DST_PATH}/index=files.html")

    # Generate a page index.
    index = ElementTree.fromstring("""
    <doxygen>
        <compounddef kind='doxy2custom'>
            <compoundname>Pages</compoundname>
            <briefdescription><para>The following thematic pages are available.</para></briefdescription>
        </compounddef>
    </doxygen>
    """)
    pages = list(filter(lambda el: el.attrib["kind"] in ["page"], docElements))
    html = htmlTemplate.html(index, pages)
    output(html, f"{HTML_DST_PATH}/index=pages.html")

    # Generate a struct/class index.
    index = ElementTree.fromstring("""
    <doxygen>
        <compounddef kind='doxy2custom'>
            <compoundname>Structures</compoundname>
            <briefdescription><para>The following classes and structs appear to have been documented.</para></briefdescription>
        </compounddef>
    </doxygen>
    """)
    structures = list(filter(lambda el: el.attrib["kind"] in ["struct", "class"], docElements))
    html = htmlTemplate.html(index, structures)
    output(html, f"{HTML_DST_PATH}/index=structures.html")
    
    # Note: We expect that the given HTML template exports a style sheet that
    # includes the CSS of all of its sub-components as well.
    css = htmlTemplate.css()
    css = "\n".join([x.strip() for x in css.splitlines() if x.strip()])
    outFile = open(f"{HTML_DST_PATH}/css/index.css", "w")
    outFile.write(css)
    outFile.close()
