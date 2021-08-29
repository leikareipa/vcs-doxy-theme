#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
from src import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html(tree:ElementTree):
    return ""

def css():
    return """
    @media only screen and (max-width: 1400px)
    {
        main > article
        {
            width: 80% !important;
        }
    }

    @media only screen and (max-width: 1100px)
    {
        main > article
        {
            width: 95% !important;
        }
    }

    @media only screen and (max-width: 870px)
    {
        :root
        {
            --article-horizontal-padding: 20px
        }
        
        main > article
        {
            width: 100% !important;
            padding-bottom: 0 !important;
        }

        main > article > .contents
        {
            border-radius: 0 !important;
            box-shadow: none !important;
        }

        main > article > header
        {
            padding: 0 10px !important;
        }
    }

    @media only screen and (max-width: 500px)
    {
        :root
        {
            --article-horizontal-padding: 10px;
            --article-header-height: 60px;
        }

        main > article
        {
            width: 100% !important;
        }

        .document-header .icon.button-bar
        {
            display: none;
        }
    }
    """
