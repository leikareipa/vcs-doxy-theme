#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from typing import Final
import xml2html

# The sub-components used in this component.
childComponents:Final = [
]

def html():
    return f"""
    <header class='document-header'>
        <div class='title'>
            <h1>
                VCS Dev Docs
            </h1>
            <i class='separator fas fa-chevron-right'></i>
            <div class='header-navi button-bar'>
                <span>Lorem</span>
                <span>Ipsum</span>
                <span>Dolor</span>
            </div>
        </div>
        <aside class='icon button-bar'>
            <a href='mailto:sw@tarpeeksihyvaesoft.com'
               title='Email'>
                <i class='fas fa-envelope-square'></i>
            </a>
            <a href='https://github.com/leikareipa/vcs'
               title='GitHub'>
                <i class='fab fa-github-square'></i>
            </a>
        </aside>
    </header>
    """

def css():
    return """
    .document-header
    {
        color: whitesmoke;
        display: flex;
        align-items: center;
        height: var(--header-height);
        padding: 0 15px;
        box-sizing: border-box;
        background-color: #3c3c3c;
    }

    .document-header .title > .separator
    {
        display: inherit;
        margin: 0 12px;
    }

    .document-header .title
    {
        display: flex;
    }
    
    .document-header .title > .button-bar.header-navi *:not(:first-child)
    {
        margin-left: 6px;
    }

    .document-header .title > h1
    {
        font-size: 100%;
        font-weight: 500;
        margin: 0;
    }

    .document-header .button-bar.header-navi
    {
        font-size: 100%;
        color: #cecece;
    }

    .document-header .button-bar.icon
    {
        font-size: 125%;
        margin-left: auto;
    }

    .document-header .button-bar.icon a
    {
        color: inherit;
        text-decoration: none;
    }

    .document-header .button-bar.icon > *:not(:first-child)
    {
        margin-left: 4px;
    }

    .document-header .button-bar.icon i
    {
        transition: transform 0.05s ease;
    }

    .document-header .button-bar.icon i:hover
    {
        transform: scale(1.2) rotateZ(3deg);
    }
    """
