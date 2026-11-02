from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


from fastapi import Form
from datetime import datetime

from pypdf import PdfReader, PdfWriter

import os
import uuid



app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


@app.get("/merge-page", response_class=HTMLResponse)
async def merge_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="merge.html"
    )


@app.get("/split-page", response_class=HTMLResponse)
async def split_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="split.html"
    )


@app.post("/merge")
async def merge(files: list[UploadFile] = File(...)):

    writer = PdfWriter()

    for file in files:

        temp_path = f"uploads/{file.filename}"

        with open(temp_path, "wb") as f:
            f.write(await file.read())

        reader = PdfReader(temp_path)

        for page in reader.pages:
            writer.add_page(page)

    output_file = f"output/{uuid.uuid4()}.pdf"

    with open(output_file, "wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="merged.pdf"
    )


@app.post("/split")
async def split(
    file: UploadFile = File(...),
    page: int = 1
):

    temp_path = f"uploads/{file.filename}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(temp_path)

    writer = PdfWriter()

    writer.add_page(reader.pages[page - 1])

    output_file = f"output/{uuid.uuid4()}.pdf"

    with open(output_file, "wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename=f"page_{page}.pdf"
    )

@app.post("/feedback")
async def feedback(
    feedback_type: str = Form(...),
    message: str = Form(...),
    email: str = Form("")
):

    with open("feedback.csv", "a", encoding="utf-8") as f:

        f.write(
            f"{datetime.now()},"
            f"{feedback_type},"
            f"{email},"
            f"{message}\n"
        )

    return HTMLResponse("""
        <h2>✅ Thank you for your feedback!</h2>
        <a href="/">Return Home</a>
    """)