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

    /* Narrow portrait mode (e.g. phones).*/
    @media only screen and (max-width: 700px)
    {
        section > header,
        section > article
        {
            overflow-x: auto;
        }
        
        table,
        thead,
        tbody,
        th,
        td,
        tr
        {
            display: block !important;
            text-align: left !important;
            padding: 0 !important;
        }

        th,
        td
        {
            border: none !important;
            word-break: break-word;
        }

        tr
        {
            padding: 10px !important;
        }

        td + td
        {
            margin-top: 3px !important;
        }

        .document-header .menu-hamburger
        {
            display: block;
        }

        .document-header .menu
        {
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
            color: var(--text-color) !important;
            font-weight: normal;
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
            --article-width: 100%;
        }

        main > article > header
        {
            margin-top: 0 !important;
        }
    }
    """
