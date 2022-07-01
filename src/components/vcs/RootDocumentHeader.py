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

def html(xmlTree:ElementTree):
    return f"""
    <header class='document-header'>
        <a class='link title' href='./index.html'>
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA+gD6APoe/B6HAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5gYeBBoMjd2ZHwAAAIxJREFUOMtj2LNj/X8GBgYGdPrpg6tYaXR1jMgcdKCpoYZNmOH6jVtwNiMuzcQY4uIRyIjXBcQYwgjzG7KziDVEWkEb4gJKDIG7AFsAETIEwwXkGILhAlIMwekCUgxh2rNj/X9cCnFFH0YYwNIBMSkPIxbQExEphuBMiaQYwkhJRnLxCGRkwJZFScnSADfUkdbcS16BAAAAAElFTkSuQmCC">
            VCS Dev Docs
        </a>
        <a class="link files" href='./index=files.html'>
            Files
        </a>
        <a class="link data-structures" href='./index=data_structures.html'>
            Data structures
        </a>
        <a class="link pages" href='./index=pages.html'>
            Pages
        </a>
        <span class="theme-selector" id='theme-selector'>
            <a onclick="toggle_theme()"></a>
        </span>
        <script>
            function toggle_theme()
            {{
                const curTheme = document.documentElement.dataset.theme;
                console.assert(['light', 'dark'].includes(curTheme));

                const newTheme = ((curTheme == "light")? "dark" : "light");
                window.VCSDoxy.set_theme(newTheme);
            }}
        </script>
    </header>
    """

def css():
    return """
    .document-header
    {
        font-weight: 500;
        display: flex;
        align-items: center;
        height: var(--header-height);
        padding: 0 1em;
        background-color: var(--document-background-color);
        border-bottom: 1px solid var(--element-border-color);
        z-index: 1;
        position: relative;
    }

    .document-header .link
    {
        margin-right: 24px;
    }

    .document-header .link.title
    {
        margin-right: 30px;
        display: flex;
        align-items: center;
    }

    .document-header .link.title > img
    {
        margin-right: 0.35em;
    }

    .document-header .link:not(.title),
    .document-header .theme-selector
    {
        color: var(--inactive-text-color);
    }

    .document-header .theme-selector
    {
        margin-left: auto;
        cursor: pointer;
    }

    .document-header .link:hover,
    .document-header .theme-selector:hover
    {
        color: var(--text-color);
    }

    .document-header a
    {
        color: inherit;
        text-decoration: none;
    }

    .document-header a:hover
    {
        text-decoration: underline !important;
    }

    .document-header .button-bar.icon
    {
        color: #cecece;
    }

    .document-header .button-bar.icon #theme-selector
    {
        cursor: pointer;
    }

    .document-header .button-bar.icon #theme-selector i.light
    {
        color: var(--text-color);
    }

    .document-header .button-bar.icon > a
    {
        cursor: pointer;
    }

    .document-header .button-bar.icon > *:not(:first-child)
    {
        margin-left: 5px;
    }

    .document-header .button-bar.icon i
    {
        color: inherit;
        transition: transform 0.02s ease;
    }

    .document-header .button-bar.icon i:hover
    {
        color: whitesmoke;
    }

    .document-header a:hover
    {
        text-decoration: none !important;
    }
    """
