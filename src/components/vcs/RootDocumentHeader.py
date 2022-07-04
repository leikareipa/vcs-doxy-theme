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
            <img alt="VCS logo" width="16" height="16" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA+gD6APoe/B6HAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5gYeBBoMjd2ZHwAAAIxJREFUOMtj2LNj/X8GBgYGdPrpg6tYaXR1jMgcdKCpoYZNmOH6jVtwNiMuzcQY4uIRyIjXBcQYwgjzG7KziDVEWkEb4gJKDIG7AFsAETIEwwXkGILhAlIMwekCUgxh2rNj/X9cCnFFH0YYwNIBMSkPIxbQExEphuBMiaQYwkhJRnLxCGRkwJZFScnSADfUkdbcS16BAAAAAElFTkSuQmCC">
            VCS Dev Docs
        </a>
        <div class="menu">
            <a class="menu-action link files" href='./index=files.html'>
                Files
            </a>
            <a class="menu-action link data-structures" href='./index=data_structures.html'>
                Data structures
            </a>
            <a class="menu-action link pages" href='./index=pages.html'>
                Pages
            </a>
            <hr>
            <a class="menu-action theme-selector" id='theme-selector' onclick="toggle_theme()" href='javascript:;'>
            </a>
        </div>
        <a class="menu-hamburger" onclick='show_menu()' href='javascript:;'>
            <i class="fas fa-bars"></i>
        </a>
    </header>
    <script>
        function toggle_theme()
        {{
            const curTheme = document.documentElement.dataset.theme;
            console.assert(['light', 'dark'].includes(curTheme));

            const newTheme = ((curTheme == "light")? "dark" : "light");
            window.VCSDoxy.set_theme(newTheme);
        }}

        const headerEl = document.querySelector(".document-header");
        const menuEl = headerEl.querySelector(".menu");
        const hamburgerEl = headerEl.querySelector(".menu-hamburger");

        window.addEventListener("click", (event)=>{{
            const isOutsideMenu = [menuEl, hamburgerEl].every(el=>(el !== event.target) && (!el.contains(event.target)));
            const isOnActionItem = event.composedPath().some(el=>el.classList?.contains("menu-action"));
            if (isOutsideMenu || isOnActionItem) {{
                menuEl.classList.remove("visible");
            }}
        }});

        function show_menu(show = undefined)
        {{
            const classListFnName = (
                (show === undefined)? "toggle"
                : show? "add"
                : "remove"
            );

            menuEl.classList[classListFnName]("visible");
        }}
    </script>
    """

def css():
    return """
    .document-header
    {
        font-weight: 500;
        display: flex;
        align-items: center;
        min-height: var(--header-height);
        padding: 0 1em;
        background-color: var(--document-background-color);
        border-bottom: 1px solid var(--element-border-color);
        z-index: 1;
        position: relative;
    }

    .document-header .menu-hamburger
    {
        display: none;
        color: var(--inactive-text-color);
        margin-left: auto;
    }

    .document-header .menu
    {
        width: 100%;
    }

    .document-header .menu > hr
    {
        display: none;
    }

    .document-header .link
    {
        margin-right: 20px;
    }

    .document-header .link.title
    {
        margin-right: 30px;
        display: flex;
        align-items: center;
        flex-shrink: 0;
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
        float: right;
        cursor: pointer;
        white-space: nowrap;
    }

    .document-header a
    {
        color: inherit;
        text-decoration: none;
    }

    .document-header a:hover
    {
        color: var(--text-color) !important;
        cursor: pointer;
        text-decoration: none !important;
    }
    """
