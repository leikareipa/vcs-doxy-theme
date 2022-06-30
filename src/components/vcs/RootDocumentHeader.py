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
        <div class='title'>
            <h1>
                <a href='./index.html'>
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA+gD6APoe/B6HAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5gYeBBoMjd2ZHwAAAIxJREFUOMtj2LNj/X8GBgYGdPrpg6tYaXR1jMgcdKCpoYZNmOH6jVtwNiMuzcQY4uIRyIjXBcQYwgjzG7KziDVEWkEb4gJKDIG7AFsAETIEwwXkGILhAlIMwekCUgxh2rNj/X9cCnFFH0YYwNIBMSkPIxbQExEphuBMiaQYwkhJRnLxCGRkwJZFScnSADfUkdbcS16BAAAAAElFTkSuQmCC">
                    VCS Dev Docs
                </a>
            </h1>
            <span class='separator'></span>
            <div class='header-navi button-bar'>
                <a href='./index=files.html'>
                    Files
                </a>
                <span class='separator'>&bull;</span>
                <a href='./index=structures.html'>
                    Data structures
                </a>
                <span class='separator'>&bull;</span>
                <a href='./index=pages.html'>
                    Pages
                </a>
            </div>
        </div>
        <aside class='icon button-bar'>
            <div title='Toggle lighting'
                 onclick='toggle_theme()'
                 id='theme-selector'>
                <i class='far fa-adjust'></i>
            </div>
        </aside>
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
        font-size: 90%;
        display: flex;
        align-items: center;
        height: var(--header-height);
        padding: 0 1em;
        background-color: var(--document-background-color);
        z-index: 1;
        position: relative;
    }

    .document-header .title > .separator
    {
        color: #cecece;
        margin: 0 1em;
    }

    .document-header .title > .button-bar > .separator
    {
        margin: 0 6px;
    }

    .document-header .title
    {
        display: flex;
        align-items: center;
    }
    
    .document-header .title > h1
    {
        font-size: 100%;
        font-weight: 500;
        margin: 0;
        text-transform: uppercase;
        font-weight: bold;
        font-size: 110%;
    }

    .document-header .title > h1 > a
    {
        display: flex;
        align-items: center;
    }

    .document-header .title > h1 > a > img
    {
        margin-right: 0.35em;
    }

    .document-header .button-bar.header-navi
    {
        font-size: 100%;
    }

    .document-header .button-bar.header-navi a
    {
        color: inherit;
        text-decoration: none;
        text-transform: uppercase;
    }

    .document-header .button-bar.icon
    {
        font-size: 135%;
        margin-left: auto;
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
