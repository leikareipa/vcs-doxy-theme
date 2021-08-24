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

    if el.attrib["kind"] == "file":
        fileXml = ElementTree.parse(f"{XML_SRC_PATH}/{refid}.xml")
        filePath = fileXml.find('./compounddef/location').attrib['file']
        filePath = re.sub(r"[^\w]", "_", filePath) # May cause duplicate strings for filenames that use non-ASCII (aA-zZ, 0-9) characters.
        dstPath = f"file={filePath}.html"
    else:
        dstPath = f"{el.attrib['kind']}={el.find('./name').text}.html"

    OUTPUT_FILENAMES[refid] = dstPath

def convert_xml_to_html(htmlTemplate):
    for el in docElements:
        refid = el.attrib['refid']
        srcFilename = f"{XML_SRC_PATH}/{refid}.xml"
        dstFilename = f"{HTML_DST_PATH}/{OUTPUT_FILENAMES[refid]}"
        
        # Convert Doxygen's XML into HTML.
        htmlOutput = htmlTemplate.html(srcXmlFilename=srcFilename)
        htmlOutput = "\n".join([x.strip() for x in htmlOutput.splitlines() if x.strip()])

        outFile = open(dstFilename, "w")
        outFile.write(htmlOutput)
        outFile.close()

    css = htmlTemplate.css()
    css = "\n".join([x.strip() for x in css.splitlines() if x.strip()])
    outFile = open(f"{HTML_DST_PATH}/css/index.css",  "w")
    outFile.write(css)
    outFile.close()
