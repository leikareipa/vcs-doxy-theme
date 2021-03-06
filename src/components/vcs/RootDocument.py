#
# 2021 Tarpeeksi Hyvae Soft
#
# Software: VCS Doxygen theme
#

from xml.etree import ElementTree
from src.components.vcs import (
    ReferenceArticle,
    MarkdownArticle,
    RootDocumentHeader,
    IndexArticle,
    ResponsiveStyling,
    BriefDescription,
)
from typing import Final
from functools import reduce

# The sub-components used in this component.
childComponents:Final = [
    ReferenceArticle,
    MarkdownArticle,
    RootDocumentHeader,
    IndexArticle,
    BriefDescription,
]

# Iterates through all child components and their child components, and returns
# all visited components as a set.
def _get_dependent_components(componentTree:list, components:set = set()):
    for child in componentTree:
        components.add(child)
        if child.childComponents:
            _get_dependent_components(child.childComponents, components)
    return components

def html(xmlTree:ElementTree, auxiliaryData:list = []):
    articleType = xmlTree.find("./compounddef").attrib["kind"]
    articleName = xmlTree.find("./compounddef/compoundname").text
    articleDescription = BriefDescription.string(xmlTree)
    article = ""

    if articleType == "doxy2custom":
        article = IndexArticle.html(xmlTree, auxiliaryData)
        articleName = f"Index: {articleName}"
    else:
        if articleName.endswith(".md") or articleName == "index":
            article = MarkdownArticle.html(xmlTree)
            if xmlTree.find("./compounddef/title") != None:
                articleName = xmlTree.find("./compounddef/title").text
        else:
            article = ReferenceArticle.html(xmlTree)

    return f"""
    <!DOCTYPE html>
    <html lang="en" data-theme="light">
        <head>
            <title>{articleName} - VCS Dev Docs</title>
            <meta name="description" content="{articleDescription}">
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <script defer src="./js/highlight.min.js"></script>
            <script>
                window.addEventListener("DOMContentLoaded", ()=>hljs.highlightAll?.());
            </script>
            <script>
                window.VCSDoxy = {{}};

                window.VCSDoxy.set_theme = function(theme = "")
                {{
                    console.assert(["dark", "light"].includes(theme));

                    // Workaround to force elements that have a transition to adopt the new
                    // theme immediately instead of transitioning it.
                    {{
                        const highlightingElems = document.body.querySelectorAll(".highlightable");

                        highlightingElems.forEach(e=>{{
                            e.style.$oldTransition = e.style.transition;
                            e.style.transition = "none";
                        }});

                        // Queue the transition to be restored once the theme has been applied.
                        setTimeout(()=>{{
                            highlightingElems.forEach(e=>{{
                                e.style.transition = e.style.$oldTransition;
                            }});
                        }}, 0);
                    }}

                    const themeEl = document.querySelector("#theme-selector");
                    themeEl.textContent = ((theme === "light")? "Dark mode" : "Light mode");

                    document.documentElement.dataset.theme = theme;
                    window.localStorage.setItem("VCSDoxy:theme", theme);
                }}
            </script>
            <script>
                function highlight_hash_target_elem()
                {{
                    if (window.location.hash.length <= 1) {{
                        return;
                    }}

                    const elem = document.querySelector(window.location.hash);

                    if (elem && !elem.classList.contains('highlight')) {{
                        elem.classList.add('highlight');
                        setTimeout(()=>elem.classList.remove('highlight'), 1500);
                    }}
                }}

                // Highlight the target element on anchor navigation.
                window.addEventListener('hashchange', highlight_hash_target_elem);

                // Highlight the element that the hash pointed to on page load, if any.
                window.addEventListener('DOMContentLoaded', highlight_hash_target_elem);
                
                document.documentElement.dataset.theme = (window.localStorage.getItem("VCSDoxy:theme") || "light")
                window.addEventListener('DOMContentLoaded', ()=>{{
                    theme = document.documentElement.dataset.theme;
                    window.VCSDoxy.set_theme(theme);
                }});
            </script>
            <link rel="stylesheet" href="./font-awesome/css/all.min.css">
            <link rel="stylesheet" href="./css/index.css">
        </head>
        <body>
            <aside>
                {RootDocumentHeader.html(xmlTree)}
            </aside>
            <main>
                {article}
            </main>
        </body>
    </html>
    """

def css():
    selfSheet = """
    /* Roboto */
    @font-face
    {
        font-family: "Roboto";
        src: url("../fonts/Roboto/woff2/Roboto-Regular.woff2") format("woff2"),
             url("../fonts/Roboto/woff/Roboto-Regular.woff") format("woff");
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }
    @font-face
    {
        font-family: "Roboto";
        src: url("../fonts/Roboto/woff2/Roboto-Italic.woff2") format("woff2"),
             url("../fonts/Roboto/woff/Roboto-Italic.woff") format("woff");
        font-weight: 400;
        font-style: italic;
        font-display: swap;
    }
    @font-face
    {
        font-family: "Roboto";
        src: url("../fonts/Roboto/woff2/Roboto-Medium.woff2") format("woff2"),
             url("../fonts/Roboto/woff/Roboto-Medium.woff") format("woff");
        font-weight: 500 700;
        font-style: normal;
        font-display: swap;
    }
    @font-face
    {
        font-family: "Roboto";
        src: url("../fonts/Roboto/woff2/Roboto-MediumItalic.woff2") format("woff2"),
             url("../fonts/Roboto/woff/Roboto-MediumItalic.woff") format("woff");
        font-weight: 500 700;
        font-style: italic;
        font-display: swap;
    }

    /* JetBrains Mono */
    @font-face
    {
        font-family: "JetBrains Mono";
        src: url("../fonts/JetBrainsMono/woff2/JetBrainsMono-Regular.woff2") format("woff2"),
             url("../fonts/JetBrainsMono/woff/JetBrainsMono-Regular.woff") format("woff");
        font-weight: 400;
        font-style: normal;
        font-display: swap;
    }
    @font-face
    {
        font-family: "JetBrains Mono";
        src: url("../fonts/JetBrainsMono/woff2/JetBrainsMono-Italic.woff2") format("woff2"),
             url("../fonts/JetBrainsMono/woff/JetBrainsMono-Italic.woff") format("woff");
        font-weight: 400;
        font-style: italic;
        font-display: swap;
    }
    @font-face
    {
        font-family: "JetBrains Mono";
        src: url("../fonts/JetBrainsMono/woff2/JetBrainsMono-Bold.woff2") format("woff2"),
             url("../fonts/JetBrainsMono/woff/JetBrainsMono-Bold.woff") format("woff");
        font-weight: 500 700;
        font-style: normal;
        font-display: swap;
    }
    @font-face
    {
        font-family: "JetBrains Mono";
        src: url("../fonts/JetBrainsMono/woff2/JetBrainsMono-BoldItalic.woff2") format("woff2"),
             url("../fonts/JetBrainsMono/woff/JetBrainsMono-BoldItalic.woff") format("woff");
        font-weight: 500 700;
        font-style: italic;
        font-display: swap;
    }

    :root
    {
        --section-vertical-margin: 16px;
        --article-horizontal-padding: 30px;
        --article-vertical-padding: 30px;
        --content-spacing: 30px;
        --header-height: 4rem;
        --article-header-height: 70px;
        --article-width: 60%;
        --article-max-width: 1100px;
    }

    html[data-theme="light"]
    {
        --document-background-color: white;
        --article-background-color: var(--document-background-color);
        --element-border-color: #e0e0e0;
        --link-color: #0c64ee;
        --secondary-background-color: #f7f7f7;
        --text-color: rgba(50, 50, 50);
        --inactive-text-color: #717171;
        --heading-text-color: rgba(30, 30, 30);
        --code-background-color: white;
        --code-text-color: var(--text-color);
        --code-comment-text-color: #3e8220;
        --highlight-glow-color: #0c64ee25;
    }

    html[data-theme="dark"]
    {
        --document-background-color: #1b1b1b;
        --article-background-color: var(--document-background-color);
        --element-border-color: black;
        --link-color: #f2ac2d;
        --secondary-background-color: #282828;
        --text-color: #aaaaaa;
        --inactive-text-color: #858585;
        --heading-text-color: #c8c8c8;
        --code-background-color: #1d1d1d;
        --code-text-color: var(--text-color);
        --code-comment-text-color: #00aeae;
        --highlight-glow-color: #f2ac2d30;
    }

    body
    {
        font-family: Roboto, sans-serif;
        margin: 0;
        padding: 0;
        background-color: var(--document-background-color);
        color: var(--text-color);
        margin-bottom: var(--content-spacing);
    }

    p,
    .interjection
    {
        line-height: 1.35em;
    }

    main
    {
        top: var(--header-height);
        bottom: 0;
        width: 100%;
        overflow: auto;
    }

    main a,
    main a:visited
    {
        font-weight: 500;
	    color: var(--link-color);
        text-decoration: none;
    }

    main a:not([href]),
    main a:not([href]):visited
    {
        color: inherit;
        text-decoration: none;
        font-weight: inherit;
    }

    main a:hover,
    main a:visited:hover
    {
        text-decoration: underline;
    }

    main a:not([href]):hover,
    main a:not([href]):visited:hover
    {
        text-decoration: none;
    }

    main > article
    {
        margin: 0 auto;
        width: var(--article-width);
        max-width: var(--article-max-width);
    }

    article section header
    {
        color: var(--heading-text-color);
    }

    article h1,
    article h2,
    article h3,
    article h4,
    article h5
    {
        color: var(--heading-text-color);
    }

    article h1
    {
        margin-top: var(--content-spacing);
    }

    article .contents > h1:first-child
    {
        margin-top: 0;
    }

    article h2,
    article h3,
    article h4,
    article h5
    {
        margin-top: 16px;
    }

    article h1
    {
        font-size: 160%;
        font-weight: 500;
    }

    article h2
    {
        font-size: 125%;
        font-weight: 500;
    }

    article h3
    {
        font-size: 100%;
        font-weight: 500;
    }

    article h4
    {
        font-size: 100%;
        font-weight: normal;
        font-style: italic;
    }

    article .interjection > .label
    {
        font-weight: 500;
    }

    article .interjection > *
    {
        display: inline;
    }

    article .interjection
    {
        margin: 16px 0;
    }

    article li
    {
        padding: 5px 0;
    }
    
    .anchor
    {
        scroll-margin-top: 24px;
    }

    .highlightable
    {
        transition: background-color 0.5s ease;
    }

    .highlightable.highlight
    {
        transition: background-color 0s ease;
    }

    .highlightable.highlight
    {
        background-color: var(--highlight-glow-color) !important;
    }
    """

    subComponents = _get_dependent_components(childComponents)

    return (
        reduce(lambda styleSheet, child: (styleSheet + child.css()), subComponents, selfSheet) +
        ResponsiveStyling.css()
    )
