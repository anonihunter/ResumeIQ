from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
def root():
    html_content = """
    <html>
        <head>
            <title>root folder</title>
        </head>
        <body>
            <h1 style="font-size: 50px; text-align: left;">Application Starts Successfully</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)