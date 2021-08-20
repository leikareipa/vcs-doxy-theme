from components import vcs

def html(articleXmlFilename:str):
    article = vcs.ReferenceArticle.html(articleXmlFilename)
    styleSheet = (css() + vcs.ReferenceArticle.css())

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>VCS Dev Docs</title>
            <meta name="viewport" content="width=device-width">
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono&display=swap">
            <style>
                {styleSheet}
            </style>
        </head>
        <body>
            <aside>
                <header class='grand-header'>
                    <h1>VCS Dev Docs</h1>
                </header>
            </aside>
            <main>
                {article}
            </main>
        </body>
    </html>
    """

def css():
    return """
    """

def js():
    return """
    """
