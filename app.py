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
import pytesseract
register_heif_opener()
from gtts import gTTS
from PIL import ImageDraw
from PIL import ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import csv
import io
import json
import xmltodict
import yaml
from dicttoxml import dicttoxml

from google import genai
from dotenv import load_dotenv

import requests

from fastapi.responses import Response

from rembg import remove
import uuid
import os
import qrcode
import base64


templates = Jinja2Templates(directory="templates")

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

from datetime import datetime

from pypdf import PdfReader, PdfWriter
from docx2pdf import convert

import subprocess
from PIL import Image
from reportlab.pdfgen import canvas
from pypdf import PdfReader
from pypdf import PdfWriter



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

@app.get("/ai-summarizer")
async def ai_summarizer_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="ai_summarizer.html"
    )

@app.get("/test-models")
async def test_models():

    models = []

    for model in client.models.list():
        models.append(model.name)

    return {
        "models": models
    }

@app.post("/ai-summarizer")
async def ai_summarizer(
    text: str = Form(...)
):

    try:

        response = client.models.generate_content(

            model="gemini-flash-lite-latest",

            contents=f"""
            Summarize the text below.

            Provide:

            Summary
            Key Points
            Action Items

            Text:
            {text}
            """
        )

        return {
            "result": response.text
        }

    except Exception as e:

        print(e)

        return {
            "error": str(e)
        }

@app.get("/barcode-generator")
async def barcode_generator_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="barcode_generator.html"
    )

@app.get("/text-to-speech")
async def text_to_speech_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="text_to_speech.html"
    )

@app.post("/text-to-speech")
async def text_to_speech(

    text: str = Form(...)

):

    output_file = (
        f"output/{uuid.uuid4()}.mp3"
    )

    tts = gTTS(
        text=text,
        lang="en"
    )

    tts.save(output_file)

    return FileResponse(
        output_file,
        media_type="audio/mpeg",
        filename="speech.mp3"
    )


@app.get("/powerpoint-to-pdf")
async def powerpoint_to_pdf_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="powerpoint_to_pdf.html"
    )

@app.post("/powerpoint-to-pdf")
async def powerpoint_to_pdf(
    file: UploadFile = File(...)
):

    input_file = (
        f"uploads/{uuid.uuid4()}_{file.filename}"
    )

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
        os.path.splitext(
            os.path.basename(input_file)
        )[0] + ".pdf"
    )

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="converted.pdf"
    )


@app.post("/generate-barcode")
async def generate_barcode(

    content: str = Form(...)

):

    filename = (
        f"output/{uuid.uuid4()}"
    )

    code128 = barcode.get(
        "code128",
        content,
        writer=ImageWriter()
    )

    code128.save(filename)

    return FileResponse(
        filename + ".png",
        media_type="image/png",
        filename="barcode.png"
    )

@app.get("/date-difference")
async def date_difference_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="date_difference.html"
    )

@app.get("/sitemap.xml")
async def sitemap():

    urls = [

        "/",
        "/merge",
        "/split",
        "/compress",
        "/images-to-pdf",
        "/pdf-to-jpg",
        "/rotate",
        "/delete-pages",
        "/extract-pages",
        "/protect-pdf",

        "/excel_to_pdf",
        "/unlock_pdf",
        "/sign_pdf",
        "/pdf_watermark",
        "/powerpoint_to_pdf",

        "/word-to-pdf",
        "/pdf-to-word",
        "/ocr-pdf-page",

        "/remove-background",
        "/resize_image",
        "/image_converter",
        "/image_watermark",
        "/heic-to-jpg",
        "/webp-to-jpg",
        "/svg-to-png",
        "/jfif-to-jpg",
        "/image-compressor",

        "/json-formatter",
        "/base64-tool",
        "/ai_summarizer",
        "/ai_prompt_generator",
        "/qr-generator",

        "/csv-to-json",
        "/json-to-csv",
        "/xml-to-json",
        "/json-to-xml",
        "/yaml-to-json",
        "/json-to-yaml",
        "/text_to_speech",
        "/speech_to_text",
        "/date_difference",
        "/barcode_generator",
        "/signature_generator",
        "/password_generator",
        "/weather",
        "/holidays",
        "/converters",
        "/text-compare",
        "/url_encoder",
        "/jason-validator",
        "/jwt-decoder",
        "/timestamp_converter",
        "/cron_generator",

        "/text-compare",
        "/text-utilities",

        "/age-calculator",
        "/emi-calculator",


        "/exchange-rate",
        "/timezone-converter",
        "/weather",
        "/ip-lookup"
    ]

    base = "https://utilitiesdocker.com"

    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

    for url in urls:

        xml += f"""
        <url>
            <loc>{base}{url}</loc>
        </url>
        """

    xml += "</urlset>"

    return Response(
        content=xml,
        media_type="application/xml"
    )



@app.get("/robots.txt")
async def robots_txt():

    return Response(
        content="""User-agent: *
Allow: /

Sitemap: https://utilitiesdocker.com/sitemap.xml
""",
        media_type="text/plain"
    )

@app.get("/exchange-rate", response_class=HTMLResponse)
async def exchange_rate(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="exchange_rate.html"
    )

@app.get("/sign-pdf")
async def sign_pdf_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="sign_pdf.html"
    )

@app.post("/sign-pdf")
async def sign_pdf(

    pdf_file: UploadFile = File(...),

    signature_file: UploadFile = File(...)

):

    pdf_path = (
        f"uploads/{uuid.uuid4()}.pdf"
    )

    sig_path = (
        f"uploads/{uuid.uuid4()}.png"
    )

    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())

    with open(sig_path, "wb") as f:
        f.write(await signature_file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_file = (
        f"output/{uuid.uuid4()}.pdf"
    )

    with open(output_file, "wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        filename="signed.pdf"
    )


@app.get("/speech-to-text")
async def speech_to_text_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="speech_to_text.html"
    )

@app.get("/converters", response_class=HTMLResponse)
async def converters(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="converters.html"
    )


@app.get("/password-generator", response_class=HTMLResponse)
async def password_generator(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="password_generator.html"
    )

@app.get("/url-encoder", response_class=HTMLResponse)
async def url_encoder_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="url_encoder.html"
    )

@app.get("/unlock-pdf")
async def unlock_pdf(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="unlock_pdf.html"
    )

@app.get("/resize-image")
async def resize_image_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="resize_image.html"
    )

@app.post("/resize-image")
async def resize_image(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):

    input_file = (
        f"uploads/{uuid.uuid4()}_{file.filename}"
    )

    with open(input_file, "wb") as f:
        f.write(await file.read())

    img = Image.open(input_file)

    resized = img.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    ext = img.format.lower()

    output_file = (
        f"output/{uuid.uuid4()}.{ext}"
    )

    resized.save(output_file)

    return FileResponse(
        output_file,
        filename=f"resized.{ext}"
    )

@app.get("/image-converter")
async def image_converter_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="image_converter.html"
    )

@app.post("/image-converter")
async def image_converter(
    file: UploadFile = File(...),
    output_format: str = Form(...)
):

    input_file = (
        f"uploads/{uuid.uuid4()}_{file.filename}"
    )

    with open(input_file, "wb") as f:
        f.write(await file.read())

    image = Image.open(input_file)

    if output_format in ["jpg", "jpeg"]:
        image = image.convert("RGB")

    output_file = (
        f"output/{uuid.uuid4()}.{output_format}"
    )

    image.save(
        output_file,
        output_format.upper()
        if output_format != "jpg"
        else "JPEG"
    )

    return FileResponse(
        output_file,
        filename=f"converted.{output_format}"
    )

@app.get("/json-validator")
async def json_validator_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="json_validator.html"
    )

@app.get("/jwt-decoder")
async def jwt_decoder(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jwt_decoder.html"
    )

@app.get("/pdf-watermark")
async def pdf_watermark(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="pdf_watermark.html"
    )


@app.post("/pdf-watermark")
async def pdf_watermark(

    file: UploadFile = File(...),

    watermark: str = Form(...)

):

    pdf_path = (
        f"uploads/{uuid.uuid4()}.pdf"
    )

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    watermark_pdf = (
        f"output/{uuid.uuid4()}_watermark.pdf"
    )

    c = canvas.Canvas(watermark_pdf)

    c.setFont(
        "Helvetica-Bold",
        40
    )

    c.setFillGray(
        0.5,
        0.5
    )

    c.drawString(
        150,
        400,
        watermark
    )

    c.save()

    reader = PdfReader(pdf_path)

    watermark_reader = PdfReader(
        watermark_pdf
    )

    writer = PdfWriter()

    watermark_page = (
        watermark_reader.pages[0]
    )

    for page in reader.pages:

        page.merge_page(
            watermark_page
        )

        writer.add_page(page)

    output_file = (
        f"output/{uuid.uuid4()}.pdf"
    )

    with open(output_file, "wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="watermarked.pdf"
    )

@app.get("/timestamp-converter")
async def timestamp_converter(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="timestamp_converter.html"
    )

@app.get("/signature-generator")
async def signature_generator(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="signature_generator.html"
    )

@app.get("/image-watermark")
async def image_watermark(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="image_watermark.html"
    )

@app.post("/image-watermark")
async def image_watermark(

    file: UploadFile = File(...),

    watermark: str = Form(...)

):

    input_file = (
        f"uploads/{uuid.uuid4()}_{file.filename}"
    )

    with open(input_file, "wb") as f:
        f.write(await file.read())

    image = Image.open(input_file)

    draw = ImageDraw.Draw(image)

    width, height = image.size

    try:

        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            max(25, width // 15)
        )

    except:

        font = ImageFont.load_default()

    # Center position
    x = width // 4
    y = height // 2

    # Shadow
    draw.text(
        (x + 2, y + 2),
        watermark,
        fill=(255, 255, 255),
        font=font
    )

    # Main watermark
    draw.text(
        (x, y),
        watermark,
        fill=(255, 0, 0),
        font=font
    )

    output_file = (
        f"output/{uuid.uuid4()}.png"
    )

    image.save(output_file)

    return FileResponse(
        output_file,
        media_type="image/png",
        filename="watermarked.png"
    )

@app.get("/cron-generator")
async def cron_generator(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="cron_generator.html"
    )

@app.post("/unlock-pdf")
async def unlock_pdf(
    file: UploadFile = File(...),
    password: str = Form(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    # unlock
    reader.decrypt(password)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_file = f"output/{uuid.uuid4()}.pdf"

    with open(output_file, "wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="unlocked.pdf"
    )


@app.get("/ai-prompt-generator", response_class=HTMLResponse)
async def ai_prompt_generator_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="ai_prompt_generator.html"
    )


@app.get("/excel-to-pdf")
async def excel_to_pdf_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="excel_to_pdf.html"
    )

@app.post("/excel-to-pdf")
async def excel_to_pdf(
    file: UploadFile = File(...)
):

    input_file = (
        f"uploads/{uuid.uuid4()}_{file.filename}"
    )

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
        os.path.splitext(
            os.path.basename(input_file)
        )[0] + ".pdf"
    )

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="converted.pdf"
    )

@app.get("/holidays", response_class=HTMLResponse)
async def holidays_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="holidays.html"
    )


@app.get("/api/holidays/{country}/{year}")
async def get_holidays(
    country: str,
    year: int
):

    url = (
        f"https://date.nager.at/api/v3/"
        f"publicholidays/{year}/{country}"
    )

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code == 204:

        return []

    if response.status_code != 200:

        return []

    return response.json()

@app.get("/weather", response_class=HTMLResponse)
async def weather(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="weather.html"
    )

@app.get("/ip-lookup", response_class=HTMLResponse)
async def ip_lookup(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ip_lookup.html"
    )

@app.get("/timezone-converter", response_class=HTMLResponse)
async def timezone_converter(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="timezone_converter.html"
    )


@app.post("/ip-lookup")
async def ip_lookup(
    ip: str = Form(...)
):
    response = requests.get(
        f"https://ipwho.is/{ip}"
    )

    return response.json()

@app.post("/api/exchange-rate")
async def exchange_rate(
    amount: float = Form(...),
    from_currency: str = Form(...),
    to_currency: str = Form(...)
):

    try:

        url = f"https://open.er-api.com/v6/latest/{from_currency}"

        response = requests.get(url)

        data = response.json()

        rate = data["rates"][to_currency]

        converted = round(amount * rate, 2)

        return {
            "success": True,
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "converted": converted
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

@app.post("/csv-to-json")
async def csv_to_json(file: UploadFile = File(...)):

    content = await file.read()

    csv_text = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(csv_text))

    data = list(reader)

    output_file = f"output/{uuid.uuid4()}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return FileResponse(
        output_file,
        media_type="application/json",
        filename="converted.json"
    )


@app.post("/json-to-csv")
async def json_to_csv(file: UploadFile = File(...)):

    data = json.loads(
        (await file.read()).decode("utf-8")
    )

    output_file = f"output/{uuid.uuid4()}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)

    return FileResponse(
        output_file,
        media_type="text/csv",
        filename="converted.csv"
    )

@app.post("/xml-to-json")
async def xml_to_json(file: UploadFile = File(...)):

    xml_data = await file.read()

    data = xmltodict.parse(xml_data)

    output_file = f"output/{uuid.uuid4()}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return FileResponse(
        output_file,
        media_type="application/json",
        filename="converted.json"
    )

@app.post("/json-to-xml")
async def json_to_xml(file: UploadFile = File(...)):

    data = json.loads(
        (await file.read()).decode("utf-8")
    )

    xml_data = dicttoxml(data)

    output_file = f"output/{uuid.uuid4()}.xml"

    with open(output_file, "wb") as f:
        f.write(xml_data)

    return FileResponse(
        output_file,
        media_type="application/xml",
        filename="converted.xml"
    )

@app.post("/yaml-to-json")
async def yaml_to_json(file: UploadFile = File(...)):

    yaml_data = await file.read()

    data = yaml.safe_load(yaml_data)

    output_file = f"output/{uuid.uuid4()}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return FileResponse(
        output_file,
        media_type="application/json",
        filename="converted.json"
    )


@app.post("/json-to-yaml")
async def json_to_yaml(file: UploadFile = File(...)):

    data = json.loads(
        (await file.read()).decode("utf-8")
    )

    output_file = f"output/{uuid.uuid4()}.yaml"

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f)

    return FileResponse(
        output_file,
        filename="converted.yaml"
    )



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

@app.get("/ocr-pdf-page", response_class=HTMLResponse)
async def ocr_pdf_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ocr_pdf.html"
    )

@app.get("/text-utilities", response_class=HTMLResponse)
async def text_utilities_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="text_utilities.html"
    )

@app.get("/developer-tools", response_class=HTMLResponse)
async def developer_tools_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="developer_tools.html"
    )

@app.get("/csv-to-json", response_class=HTMLResponse)
async def csv_to_json_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="csv_to_json.html"
    )

@app.get("/json-to-csv", response_class=HTMLResponse)
async def json_to_csv_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="json_to_csv.html"
    )

@app.get("/xml-to-json", response_class=HTMLResponse)
async def xml_to_json_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="xml_to_json.html"
    )

@app.get("/json-to-xml", response_class=HTMLResponse)
async def json_to_xml_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="json_to_xml.html"
    )

@app.get("/yaml-to-json", response_class=HTMLResponse)
async def yaml_to_json_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="yaml_to_json.html"
    )

@app.get("/json-to-yaml", response_class=HTMLResponse)
async def json_to_yaml_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="json_to_yaml.html"
    )

@app.post("/ocr-pdf")
async def ocr_pdf(
    file: UploadFile = File(...)
):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    images = convert_from_path(pdf_path)

    extracted_text = ""

    for image in images:
        extracted_text += pytesseract.image_to_string(image)
        extracted_text += "\n\n"

    output_file = f"output/{uuid.uuid4()}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    return FileResponse(
        output_file,
        media_type="text/plain",
        filename="ocr-result.txt"
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

@app.get("/merge", response_class=HTMLResponse)
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

@app.get("/split", response_class=HTMLResponse)
async def split_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="split.html"
    )

@app.get("/pdf-to-jpg", response_class=HTMLResponse)
async def pdf_to_jpg_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pdf_to_jpg.html"
    )


@app.get("/rotate", response_class=HTMLResponse)
async def rotate_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="rotate.html"
    )


@app.get("/delete-pages", response_class=HTMLResponse)
async def delete_pages_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="delete_pages.html"
    )


@app.get("/extract-pages", response_class=HTMLResponse)
async def extract_pages_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="extract_pages.html"
    )


@app.get("/protect-pdf", response_class=HTMLResponse)
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

@app.get("/compress", response_class=HTMLResponse)
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

@app.get("/images-to-pdf", response_class=HTMLResponse)
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