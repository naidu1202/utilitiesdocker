from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
from pdf2image import convert_from_path

from fastapi import Form
from datetime import datetime

from pypdf import PdfReader, PdfWriter
from docx2pdf import convert

import os
import uuid
import subprocess
from PIL import Image




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

@app.get("/pdf-to-jpg-page", response_class=HTMLResponse)
async def pdf_to_jpg_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pdf_to_jpg.html"
    )


@app.get("/rotate-page", response_class=HTMLResponse)
async def rotate_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="rotate.html"
    )


@app.get("/delete-pages-page", response_class=HTMLResponse)
async def delete_pages_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="delete_pages.html"
    )


@app.get("/extract-pages-page", response_class=HTMLResponse)
async def extract_pages_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="extract_pages.html"
    )


@app.get("/protect-pdf-page", response_class=HTMLResponse)
async def protect_pdf_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="protect_pdf.html"
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

@app.get("/compress-page", response_class=HTMLResponse)
async def compress_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="compress.html"
    )

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="compressed.pdf"
    )

@app.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...)
):
    input_file = f"uploads/{uuid.uuid4()}.pdf"

    with open(input_file, "wb") as f:
        f.write(await file.read())

    output_file = f"output/{uuid.uuid4()}.pdf"

    subprocess.run([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_file}",
        input_file
    ])

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="compressed.pdf"
    )

@app.get("/images-to-pdf-page", response_class=HTMLResponse)
async def images_to_pdf_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="images_to_pdf.html"
    )

@app.post("/images-to-pdf")
async def images_to_pdf(
    files: list[UploadFile] = File(...)
):

    images = []

    for file in files:
        path = f"uploads/{uuid.uuid4()}_{file.filename}"

        with open(path, "wb") as f:
            f.write(await file.read())

        img = Image.open(path).convert("RGB")
        images.append(img)

    output = f"output/{uuid.uuid4()}.pdf"

    images[0].save(
        output,
        save_all=True,
        append_images=images[1:]
    )

    return FileResponse(
        output,
        media_type="application/pdf",
        filename="images.pdf"
    )

@app.post("/pdf-to-jpg")
async def pdf_to_jpg(
    file: UploadFile = File(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    images = convert_from_path(pdf_path)

    jpg_file = f"output/{uuid.uuid4()}.jpg"

    images[0].save(jpg_file)

    return FileResponse(
        jpg_file,
        media_type="image/jpeg",
        filename="page1.jpg"
    )

@app.post("/rotate")
async def rotate_pdf(
    file: UploadFile = File(...),
    degrees: int = Form(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)

    output = f"output/{uuid.uuid4()}.pdf"

    with open(output, "wb") as f:
        writer.write(f)

    return FileResponse(
        output,
        filename="rotated.pdf"
    )

@app.post("/delete-pages")
async def delete_pages(
    file: UploadFile = File(...),
    pages: str = Form(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    delete_list = [int(x) for x in pages.split(",")]

    for i, page in enumerate(reader.pages, start=1):

        if i not in delete_list:
            writer.add_page(page)

    output = f"output/{uuid.uuid4()}.pdf"

    with open(output, "wb") as f:
        writer.write(f)

    return FileResponse(
        output,
        filename="updated.pdf"
    )


@app.post("/extract-pages")
async def extract_pages(
    file: UploadFile = File(...),
    pages: str = Form(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    extract_list = [int(x) for x in pages.split(",")]

    for p in extract_list:
        writer.add_page(reader.pages[p - 1])

    output = f"output/{uuid.uuid4()}.pdf"

    with open(output, "wb") as f:
        writer.write(f)

    return FileResponse(
        output,
        filename="extracted.pdf"
    )

@app.post("/protect-pdf")
async def protect_pdf(
    file: UploadFile = File(...),
    password: str = Form(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output = f"output/{uuid.uuid4()}.pdf"

    with open(output, "wb") as f:
        writer.write(f)

    return FileResponse(
        output,
        filename="protected.pdf"
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