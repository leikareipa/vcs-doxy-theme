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
HTML_DST_PATH = "./html"
XML_SRC_PATH = "./xml"
XML_INDEX:Final = ElementTree.parse(f"{XML_SRC_PATH}/index.xml")

# Remove any previous doc files. This is a bit dangerous, since the directory
# could contain other files as well, but hey.
if os.path.exists(HTML_DST_PATH):
    shutil.rmtree(HTML_DST_PATH)
os.mkdir(HTML_DST_PATH)

# The source XML elements we'll produce HTML output for.
docElements = XML_INDEX.findall("./compound")
docElements = list(filter(lambda x: x.attrib["kind"] in ["page", "file", "struct", "class"], docElements))

for el in docElements:
    refid = el.attrib['refid']

    if el.attrib["kind"] == "file":
        fileXml = ElementTree.parse(f"{XML_SRC_PATH}/{refid}.xml")
        filePath = fileXml.find('./compounddef/location').attrib['file']
        filePath = re.sub(r"[^\w]", "_", filePath) # May cause duplicate strings for filenames that use non-ASCII characters.
        dstPath = f"file_{filePath}.html"
    else:
        dstPath = f"{el.attrib['kind']}_{el.find('./name').text}.html"

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
