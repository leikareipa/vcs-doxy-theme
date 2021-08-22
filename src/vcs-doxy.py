#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

import re
from components.vcs.Document import html as VCSDocPage

doc = VCSDocPage(srcXmlFilename="capture_8h.xml")
doc = "\n".join([x.strip() for x in doc.splitlines() if x.strip()])
print(doc)
