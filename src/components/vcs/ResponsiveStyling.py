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
        :root
        {
            --article-width: 80%;
        }
    }

    @media only screen and (max-width: 1100px)
    {
        :root
        {
            --article-width: 100%;
        }

        .article-header .crumb.root
        {
            display: none;
        }
    }

    @media only screen and (max-width: 870px)
    {
        :root
        {
            --article-horizontal-padding: 20px;
        }

        main
        {
            position: unset;
        }
        
        main > article
        {
            padding-bottom: 0 !important;
        }

        main > article > .contents
        {
            border-radius: 0 !important;
            box-shadow: none !important;
        }

        main > article > .article-header
        {
            margin-top: 0;
        }
    }

    @media only screen and (max-width: 600px)
    {
        .document-header .menu-hamburger
        {
            display: block;
        }

        .document-header .menu
        {
            font-size: 95%;
            position: absolute;
            display: flex;
            flex-direction: column;
            top: calc(var(--header-height) - 18px);
            right: 1em;
            justify-content: right;
            width: unset;
            background-color: var(--article-background-color);
            padding: 7px 0;
            border: 1px solid var(--element-border-color);
            border-radius: 4px;
            box-shadow: 0 0 0 1px var(--secondary-background-color);
        }

        .document-header .menu:not(.visible)
        {
            visibility: hidden;
        }

        .document-header .menu > hr
        {
            display: unset;
            width: 100%;
            border: none;
            border-bottom: 1px solid var(--element-border-color);
        }

        .document-header .menu > a
        {
            width: 100%;
            padding: 8px 14px;
            box-sizing: border-box;
        }

        .document-header .menu > a:hover
        {
            background-color: var(--secondary-background-color);
        }
    }

    @media only screen and (max-width: 500px)
    {
        :root
        {
            --article-horizontal-padding: 10px;
            --article-header-height: 60px;
            --article-width: 100%;
        }

        main > article > header
        {
            margin-top: 0 !important;
        }
    }
    """
