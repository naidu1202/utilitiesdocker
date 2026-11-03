from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
from pdf2image import convert_from_path
from pydantic import BaseModel
from difflib import HtmlDiff
from pdf2docx import Converter
from pillow_heif import register_heif_opener
import cairosvg
register_heif_opener()


from rembg import remove
import uuid
import os
import qrcode
import base64


templates = Jinja2Templates(directory="templates")


from datetime import datetime

from pypdf import PdfReader, PdfWriter
from docx2pdf import convert

import subprocess
from PIL import Image




app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


from fastapi.responses import HTMLResponse

class EncodeRequest(BaseModel):
    text: str

@app.post("/api/base64/encode")
def encode_base64(req: EncodeRequest):
    encoded = base64.b64encode(
        req.text.encode("utf-8")
    ).decode("utf-8")

    return {
        "encoded": encoded
    }

class DecodeRequest(BaseModel):
    text: str

@app.post("/api/base64/decode")
def decode_base64(req: DecodeRequest):

    decoded = base64.b64decode(
        req.text
    ).decode("utf-8")

    return {
        "decoded": decoded
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )

@app.get("/svg-to-png", response_class=HTMLResponse)
async def svg_to_png_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="svg_to_png.html"
    )

@app.post("/svg-to-png")
async def svg_to_png(
    file: UploadFile = File(...)
):

    svg_data = await file.read()

    output_file = f"output/{uuid.uuid4()}.png"

    cairosvg.svg2png(
        bytestring=svg_data,
        write_to=output_file
    )

    return FileResponse(
        output_file,
        media_type="image/png",
        filename="converted.png"
    )

@app.get("/jfif-to-jpg", response_class=HTMLResponse)
async def jfif_to_jpg_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jfif_to_jpg.html"
    )



@app.post("/jfif-to-jpg")
async def jfif_to_jpg(
    file: UploadFile = File(...)
):

    input_file = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(input_file, "wb") as f:
        f.write(await file.read())

    image = Image.open(input_file)

    output_file = f"output/{uuid.uuid4()}.jpg"

    image.save(output_file, "JPEG")

    return FileResponse(
        output_file,
        media_type="image/jpeg",
        filename="converted.jpg"
    )

@app.get("/heic-to-jpg", response_class=HTMLResponse)
async def heic_to_jpg_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="heic_to_jpg.html"
    )

@app.post("/heic-to-jpg")
async def heic_to_jpg(
    file: UploadFile = File(...)
):

    input_file = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(input_file, "wb") as f:
        f.write(await file.read())

    image = Image.open(input_file)

    output_file = f"output/{uuid.uuid4()}.jpg"

    image.convert("RGB").save(
        output_file,
        "JPEG"
    )

    return FileResponse(
        output_file,
        media_type="image/jpeg",
        filename="converted.jpg"
    )

@app.get("/age-calculator", response_class=HTMLResponse)
async def age_calculator():
    with open("templates/age-calculator.html") as f:
        return HTMLResponse(f.read())

@app.get("/emi-calculator", response_class=HTMLResponse)
async def emi_calculator():
    with open("templates/emi-calculator.html") as f:
        return HTMLResponse(f.read())

@app.get("/merge-page", response_class=HTMLResponse)
async def merge_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="merge.html"
    )

@app.get("/text-compare", response_class=HTMLResponse)
async def text_compare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="text-compare.html"
    )

@app.post("/text-compare", response_class=HTMLResponse)
async def compare_text(
    request: Request,
    text1: str = Form(...),
    text2: str = Form(...)
):
    diff = HtmlDiff()

    result = diff.make_table(
        text1.splitlines(),
        text2.splitlines(),
        "Text 1",
        "Text 2",
        context=True
    )

    return templates.TemplateResponse(
        request=request,
        name="text-compare.html",
        context={
            "result": result,
            "text1": text1,
            "text2": text2
        }
    )

@app.get("/remove-background")
async def remove_background_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="remove_background.html"
    )

@app.get("/word-to-pdf")
async def word_to_pdf_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="word_to_pdf.html"
    )

@app.get("/webp-to-jpg")
async def webp_to_jpg_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="webp_to_jpg.html"
    )

@app.post("/webp-to-jpg")
async def webp_to_jpg(file: UploadFile = File(...)):

    input_file = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(input_file, "wb") as f:
        f.write(await file.read())

    image = Image.open(input_file)

    output_file = f"output/{uuid.uuid4()}.jpg"

    image.convert("RGB").save(output_file)

    return FileResponse(
        output_file,
        media_type="image/jpeg",
        filename="converted.jpg"
    )



@app.post("/word-to-pdf")
async def word_to_pdf(
    file: UploadFile = File(...)
):
    input_file = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(input_file, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        input_file,
        "--outdir",
        "output"
    ])

    pdf_file = os.path.join(
        "output",
        os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
    )

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="converted.pdf"
    )


@app.get("/pdf-to-word")
async def pdf_to_word_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pdf_to_word.html"
    )

@app.post("/pdf-to-word")
async def pdf_to_word(
    file: UploadFile = File(...)
):
    pdf_file = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_file, "wb") as f:
        f.write(await file.read())

    docx_file = f"output/{uuid.uuid4()}.docx"

    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()

    return FileResponse(
        docx_file,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="converted.docx"
    )

@app.get("/json-formatter", response_class=HTMLResponse)
async def json_formatter_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="json_formatter.html"
    )

@app.get("/qr-generator", response_class=HTMLResponse)
async def qr_generator_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="qr_generator.html"
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

@app.get("/image-compressor", response_class=HTMLResponse)
async def image_compressor_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="image_compressor.html"
    )

@app.post("/compress-image")
async def compress_image(
    file: UploadFile = File(...)
):
    input_path = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = (
        f"output/{uuid.uuid4()}_compressed.jpg"
    )

    img = Image.open(input_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img.save(
        output_path,
        "JPEG",
        optimize=True,
        quality=60
    )

    return FileResponse(
        output_path,
        media_type="image/jpeg",
        filename="compressed.jpg"
    )


@app.get("/base64-tool", response_class=HTMLResponse)
async def base64_tool_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="base64_tool.html"
    )


@app.post("/generate-qr")
async def generate_qr(
    content: str = Form(...)
):

    filename = f"output/{uuid.uuid4()}.png"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    img.save(filename)

    return FileResponse(
        filename,
        media_type="image/png",
        filename="qrcode.png"
    )


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):

    input_data = await file.read()

    output_data = remove(input_data)

    filename = f"{uuid.uuid4()}.png"
    output_file = f"outputs/{filename}"

    with open(output_file, "wb") as f:
        f.write(output_data)

    return FileResponse(
        output_file,
        media_type="image/png",
        filename="background_removed.png"
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