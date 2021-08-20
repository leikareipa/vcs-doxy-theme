#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from components import vcs
import inspect
import re

doc = vcs.DocPage.html("filter_8h.xml")
doc = "\n".join([x.strip() for x in doc.splitlines() if x.strip()])
print(doc)

