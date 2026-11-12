from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
from pdf2image import convert_from_path
from pydantic import BaseModel
from difflib import SequenceMatcher
from pdf2docx import Converter
from pillow_heif import register_heif_opener
import fitz
import pymupdf as fitz
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

import uuid
import os
from fastapi import UploadFile, File
import uuid
from fastapi import UploadFile, File, Form
from fastapi.responses import FileResponse

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

TOOL_LINKS = {

   "ai-summarizer": "/ai-summarizer",
    "barcode-generator": "/barcode-generator",
    "text-to-speech": "/text-to-speech",
    "powerpoint-to-pdf": "/powerpoint-to-pdf",
    "date-difference": "/date-difference",
    "exchange-rate": "/exchange-rate",
    "sign-pdf": "/sign-pdf",
    "redact-pdf": "/redact-pdf",
    "mp3-cutter": "/mp3-cutter",
    "audio-extractor": "/audio-extractor",
    "compare-pdf": "/compare-pdf",
    "organize-pdf": "/organize-pdf",
    "audio-converter": "/audio-converter",
    "merge-audio": "/merge-audio",
    "video-to-mp3": "/video-to-mp3",
    "add-audio-to-video": "/add-audio-to-video",
    "video-compressor": "/video-compressor",
    "video-to-gif": "/video-to-gif",
    "gif-to-video": "/gif-to-video",
    "photo-to-video": "/photo-to-video",
    "audio-file": "/audio-file",
    "sql-formatter": "/sql-formatter",
    "speech-to-text": "/speech-to-text",
    "converters": "/converters",
    "password-generator": "/password-generator",
    "url-encoder": "/url-encoder",
    "unlock-pdf": "/unlock-pdf",
    "resize-image": "/resize-image",
    "image-converter": "/image-converter",
    "json-validator": "/json-validator",
    "jwt-decoder": "/jwt-decoder",
    "pdf-watermark": "/pdf-watermark",
    "timestamp-converter": "/timestamp-converter",
    "signature-generator": "/signature-generator",
    "image-watermark": "/image-watermark",
    "cron-generator": "/cron-generator",
    "ai-prompt-generator": "/ai-prompt-generator",
    "excel-to-pdf": "/excel-to-pdf",
    "holidays": "/holidays",
    "weather": "/weather",
    "ip-lookup": "/ip-lookup",
    "timezone-converter": "/timezone-converter",
    "svg-to-png": "/svg-to-png",
    "ocr-pdf-page": "/ocr-pdf-page",
    "text-utilities": "/text-utilities",
    "csv-to-json": "/csv-to-json",
    "json-to-csv": "/json-to-csv",
    "xml-to-json": "/xml-to-json",
    "yaml-to-json": "/yaml-to-json",
    "json-to-yaml": "/json-to-yaml",
    "ocr-pdf": "/ocr-pdf",
    "jfif-to-jpg": "/jfif-to-jpg",
    "heic-to-jpg": "/heic-to-jpg",
    "age-calculator": "/age-calculator",
    "emi-calculator": "/emi-calculator",
    "merge": "/merge",
    "text-compare": "/text-compare",
    "remove-background": "/remove-background",
    "word-to-pdf": "/word-to-pdf",
    "webp-to-jpg": "/webp-to-jpg",
    "pdf-to-word": "/pdf-to-word",
    "json-formatter": "/json-formatter",
    "qr-generator": "/qr-generator",
    "split": "/split",
    "pdf-to-jpg": "/pdf-to-jpg",
    "rotate": "/rotate",
    "delete-pages": "/delete-pages",
    "extract-pages": "/extract-pages",
    "protect-pdf": "/protect-pdf",
    "image-compressor": "/image-compressor",
    "base64-tool": "/base64-tool",
    "compress": "/compress",
    "images-to-pdf": "/images-to-pdf",
    "edit-pdf": "/edit-pdf"

}



TOOL_ICONS = {

    "ai-summarizer": "🤖",
    "barcode-generator": "🏷️",
    "text-to-speech": "🔊",
    "speech-to-text": "🎤",
    "ai-prompt-generator": "✨",
    "edit-pdf": "✏️",
    "merge": "📄",
    "split": "✂️",
    "compress": "🗜️",
    "images-to-pdf": "🖼️",
    "pdf-to-jpg": "📸",
    "rotate": "🔄",
    "delete-pages": "🗑️",
    "extract-pages": "📑",
    "protect-pdf": "🔒",
    "unlock-pdf": "🔓",
    "sign-pdf": "✍️",
    "pdf-watermark": "💧",
    "compare-pdf": "⚖️",
    "organize-pdf": "📄",
    "redact-pdf": "🛑",

    "word-to-pdf": "📄",
    "pdf-to-word": "📝",
    "excel-to-pdf": "📊",
    "powerpoint-to-pdf": "📈",

    "remove-background": "🎨",
    "resize-image": "📏",
    "image-converter": "🖼️",
    "image-watermark": "💧",
    "image-compressor": "🗜️",
    "heic-to-jpg": "📱",
    "webp-to-jpg": "🌐",
    "svg-to-png": "🎨",
    "jfif-to-jpg": "🖼️",

    "audio-extractor": "🎵",
    "audio-converter": "🎼",
    "merge-audio": "🎹",
    "mp3-cutter": "✂️",
    "video-to-mp3": "🎬",
    "add-audio-to-video": "🎧",
    "video-compressor": "🎥",
    "video-to-gif": "🎞️",
    "gif-to-video": "📹",
    "photo-to-video": "📸",

    "json-formatter": "📋",
    "json-validator": "✅",
    "json-to-csv": "📊",
    "csv-to-json": "📄",
    "xml-to-json": "🔄",
    "json-to-xml": "🔄",
    "yaml-to-json": "📘",
    "json-to-yaml": "📘",
    "jwt-decoder": "🔐",
    "base64-tool": "🔑",
    "url-encoder": "🌐",
    "sql-formatter": "💻",
    "timestamp-converter": "⏰",
    "cron-generator": "🕒",

    "weather": "☁️",
    "holidays": "🎉",
    "ip-lookup": "🌍",
    "timezone-converter": "🕓",
    "exchange-rate": "💱",
    "qr-generator": "📱",
    "password-generator": "🔑",
    "signature-generator": "✍️",
    "date-difference": "📅",
    "age-calculator": "🎂",
    "emi-calculator": "🏦",
    "text-compare": "📝",
    "text-utilities": "📚"
}

TOOL_NAMES = {
    "ai-summarizer": "🤖 AI Summarizer",
    "barcode-generator": "🏷️ Barcode Generator",
    "text-to-speech": "🔊 Text To Speech",
    "powerpoint-to-pdf": "📊 PowerPoint To PDF",
    "date-difference": "📅 Date Difference",
    "exchange-rate": "💱 Exchange Rate",
    "sign-pdf": "✍️ Sign PDF",
    "edit-pdf": "✏️ Edit PDF",
    "redact-pdf": "🛑 Redact PDF",
    "mp3-cutter": "✂️ MP3 Cutter",
    "audio-extractor": "🎵 Audio Extractor",
    "compare-pdf": "⚖️ Compare PDF",
    "organize-pdf": "📑 Organize PDF",
    "audio-converter": "🎼 Audio Converter",
    "merge-audio": "🎹 Merge Audio",
    "video-to-mp3": "🎬 Video To MP3",
    "add-audio-to-video": "🎧 Add Audio To Video",
    "video-compressor": "🎥 Video Compressor",
    "video-to-gif": "🎞️ Video To GIF",
    "gif-to-video": "📹 GIF To Video",
    "photo-to-video": "📸 Photo To Video",

    "password-generator": "🔑 Password Generator",
    "url-encoder": "🌐 URL Encoder",
    "unlock-pdf": "🔓 Unlock PDF",
    "resize-image": "📏 Resize Image",
    "image-converter": "🖼️ Image Converter",
    "json-validator": "✅ JSON Validator",
    "jwt-decoder": "🔐 JWT Decoder",
    "pdf-watermark": "💧 PDF Watermark",
    "timestamp-converter": "⏰ Timestamp Converter",
    "signature-generator": "✍️ Signature Generator",
    "image-watermark": "💧 Image Watermark",
    "cron-generator": "🕒 Cron Generator",

    "ai-prompt-generator": "🤖 AI Prompt Generator",
    "excel-to-pdf": "📊 Excel To PDF",
    "holidays": "🎉 Holidays",
    "weather": "☁️ Weather",
    "ip-lookup": "🌍 IP Lookup",
    "timezone-converter": "🕒 Timezone Converter",

    "svg-to-png": "🎨 SVG To PNG",
    "ocr-pdf-page": "🔍 OCR PDF",
    "text-utilities": "📝 Text Utilities",

    "csv-to-json": "📄 CSV To JSON",
    "json-to-csv": "📊 JSON To CSV",
    "xml-to-json": "🔄 XML To JSON",
    "yaml-to-json": "📘 YAML To JSON",
    "json-to-yaml": "📘 JSON To YAML",

    "jfif-to-jpg": "🖼️ JFIF To JPG",
    "heic-to-jpg": "📱 HEIC To JPG",

    "age-calculator": "🎂 Age Calculator",
    "emi-calculator": "🏦 EMI Calculator",

    "merge": "📄 Merge PDF",
    "text-compare": "📝 Text Compare",
    "remove-background": "🎨 Remove Background",
    "word-to-pdf": "📄 Word To PDF",
    "webp-to-jpg": "🌐 WEBP To JPG",
    "pdf-to-word": "📝 PDF To Word",
    "json-formatter": "📋 JSON Formatter",
    "qr-generator": "📱 QR Generator",
    "split": "✂️ Split PDF",
    "pdf-to-jpg": "📸 PDF To JPG",
    "rotate": "🔄 Rotate PDF",
    "delete-pages": "🗑️ Delete Pages",
    "extract-pages": "📑 Extract Pages",
    "protect-pdf": "🔒 Protect PDF",
    "image-compressor": "🗜️ Image Compressor",
    "base64-tool": "🔐 Base64 Tool",
    "compress": "🗜️ Compress PDF",
    "images-to-pdf": "🖼️ Images To PDF"
}

import sqlite3



@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return open("templates/privacy.html").read()

def init_db():

    conn = sqlite3.connect("tools.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tool_visits(
            tool_name TEXT PRIMARY KEY,
            visits INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

init_db()


def record_visit(tool_name):

    conn = sqlite3.connect("tools.db")

    conn.execute("""
        INSERT INTO tool_visits(tool_name, visits)
        VALUES(?,1)
        ON CONFLICT(tool_name)
        DO UPDATE SET visits = visits + 1
    """,(tool_name,))

    conn.commit()
    conn.close()

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
    record_visit("ai-summarizer")
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
    record_visit("barcode-generator")
    return templates.TemplateResponse(
        request=request,
        name="barcode_generator.html"
    )

@app.get("/text-to-speech")
async def text_to_speech_page(
    request: Request
):
    record_visit("text-to-speech")
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
    record_visit("powerpoint-to-pdf")
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
    record_visit("date-difference")
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
        "/ip-lookup",
        "/audio_extractor",
        "/audio_converter",
        "/mp3_cutter",
        "/mp3_cutter_editor",
        "/merge_audio",
        "/video_to_mp3",
        "/add_audio_to_video",
        "/video_compressor",
        "/video_to_gif",
        "/gif_to_video",
        "/photo_to_video"
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
    record_visit("exchange-rate")
    return templates.TemplateResponse(
        request=request,
        name="exchange_rate.html"
    )

    
@app.get("/edit-pdf")
async def edit_pdf_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="edit_pdf.html"
    )




@app.post("/api/upload-pdf")
async def upload_pdf(pdf_file: UploadFile = File(...)):

    pdf_id = str(uuid.uuid4())

    pdf_path = f"uploads/{pdf_id}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())

    print("PDF Uploaded:", pdf_path)

    return {
        "pdf_id": pdf_id
    }

@app.get("/sign-pdf")
async def sign_pdf_page(
    request: Request
):
    record_visit("sign-pdf")
    return templates.TemplateResponse(
        request=request,
        name="sign_pdf.html"
    )

from fastapi import Body

from fastapi import Body
from fastapi.responses import FileResponse
import uuid
import fitz
import os

@app.post("/api/save-pdf")
async def save_pdf(data: dict = Body(...)):

    pdf_id = data["pdf_id"]

    objects = data["objects"]

    pdf_path = f"uploads/{pdf_id}.pdf"

    print("PDF PATH:", pdf_path)

    if not os.path.exists(pdf_path):

        return {
            "error": f"PDF not found: {pdf_path}"
        }

    doc = fitz.open(pdf_path)

    for obj in objects:

        page_number = obj.get(
            "page",
            0
        )

        page = doc[page_number]

        if obj["type"] == "text":

            pdf_width = page.rect.width
            pdf_height = page.rect.height

            canvas_width = obj["canvas_width"]
            canvas_height = obj["canvas_height"]

            pdf_x = (
                obj["x"]
                * pdf_width
                / canvas_width
            )

            pdf_y = (
                obj["y"]
                * pdf_height
                / canvas_height
            )

            rect = fitz.Rect(
                pdf_x,
                pdf_y,
                pdf_x + 500,
                pdf_y + 50
            )

            page.insert_textbox(

                rect,

                obj["text"],

                fontsize=obj.get(
                    "font_size",
                    12
                ) * 0.5,

                color=(0,0,0)

            )

        elif obj["type"] == "image":

            image_data = obj["src"]

            image_data = image_data.split(",")[1]

            image_bytes = base64.b64decode(
                image_data
            )

            image_file = (
                f"uploads/{uuid.uuid4()}.png"
            )

            with open(
                image_file,
                "wb"
            ) as f:

                f.write(image_bytes)

            pdf_width = page.rect.width
            pdf_height = page.rect.height

            canvas_width = obj["canvas_width"]
            canvas_height = obj["canvas_height"]

            pdf_x = (
                obj["x"]
                * pdf_width
                / canvas_width
            )

            pdf_y = (
                obj["y"]
                * pdf_height
                / canvas_height
            )

            pdf_w = (
                obj["width"]
                * pdf_width
                / canvas_width
            )

            pdf_h = (
                obj["height"]
                * pdf_height
                / canvas_height
            )

            rect = fitz.Rect(

                pdf_x,
                pdf_y,

                pdf_x + pdf_w,

                pdf_y + pdf_h

            )

            page.insert_image(

                rect,

                filename=image_file

            )

        
    output_file = (
        f"output/{uuid.uuid4()}.pdf"
    )

    doc.save(output_file)

    doc.close()

    print(
        "Saved:",
        output_file
    )

    return FileResponse(
        output_file,
        media_type="application/pdf",
        filename="edited.pdf"
    )


@app.post("/sign-pdf")
async def sign_pdf(

    pdf_file: UploadFile = File(...),

    signature_file: UploadFile = File(...),

    x: float = Form(100),

    y: float = Form(100)

):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"
    sig_path = f"uploads/{uuid.uuid4()}.png"

    with open(pdf_path, "wb") as f:
        f.write(await pdf_file.read())

    with open(sig_path, "wb") as f:
        f.write(await signature_file.read())

    doc = fitz.open(pdf_path)

    page = doc[0]

    signature_width = 140
    signature_height = 60

    rect = fitz.Rect(
        x - signature_width / 2,
        y - signature_height / 2,
        x + signature_width / 2,
        y + signature_height / 2
    )

    page.insert_image(
        rect,
        filename=sig_path
    )

    output_file = f"output/{uuid.uuid4()}.pdf"

    doc.save(output_file)
    doc.close()

    return FileResponse(
        output_file,
        filename="signed.pdf"
    )

@app.get("/redact-pdf")
async def redact_pdf_page(
    request: Request
):
    record_visit("redact-pdf")
    return templates.TemplateResponse(
        request=request,
        name="redact_pdf.html"
    )


@app.post("/redact-pdf")
async def redact_pdf(

    file: UploadFile = File(...),

    find_text: str = Form(...)

):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path,"wb") as f:
        f.write(await file.read())

    doc = fitz.open(pdf_path)

    for page in doc:

        matches = page.search_for(
            find_text
        )

        for rect in matches:

            page.add_redact_annot(
                rect,
                fill=(0,0,0)
            )

        page.apply_redactions()

    output_file = f"output/{uuid.uuid4()}.pdf"

    doc.save(output_file)

    doc.close()

    return FileResponse(
        output_file,
        filename="redacted.pdf"
    )

@app.get("/organize-pdf")
async def organize_pdf_page(
    request: Request
):
    record_visit("organize-pdf")
    return templates.TemplateResponse(
        request=request,
        name="organize_pdf.html"
    )


@app.post("/organize-pdf")
async def organize_pdf(

    file: UploadFile = File(...),

    page_order: str = Form(...)

):

    pdf_path = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf_path,"wb") as f:
        f.write(await file.read())

    reader = PdfReader(pdf_path)

    writer = PdfWriter()

    pages = [
        int(x)
        for x in page_order.split(",")
    ]

    for p in pages:

        writer.add_page(
            reader.pages[p-1]
        )

    output_file = f"output/{uuid.uuid4()}.pdf"

    with open(output_file,"wb") as f:
        writer.write(f)

    return FileResponse(
        output_file,
        filename="organized.pdf"
    )


@app.get("/compare-pdf")
async def compare_pdf_page(
    request: Request
):
    record_visit("compare-pdf")
    return templates.TemplateResponse(
        request=request,
        name="compare_pdf.html"
    )


@app.get("/audio-extractor")
async def audio_extractor_page(
    request: Request
):
    record_visit("audio-extractor")
    return templates.TemplateResponse(
        request=request,
        name="audio_extractor.html"
    )


@app.post("/audio-extractor")
async def audio_extractor(
    file: UploadFile = File(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        output_file = (
            f"output/{uuid.uuid4()}.mp3"
        )

        subprocess.run([
            "ffmpeg",
            "-i",
            input_file,
            "-vn",
            "-acodec",
            "libmp3lame",
            "-q:a",
            "2",
            output_file
        ], check=True)

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="audio.mp3"
        )

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/mp3-cutter")
async def mp3_cutter_page(
    request: Request
):
    record_visit("mp3-cutter")
    return templates.TemplateResponse(
        request=request,
        name="mp3_cutter.html"
    )


@app.post("/mp3-cutter")
async def mp3_cutter_upload(
    request: Request,
    file: UploadFile = File(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                input_file
            ],
            capture_output=True,
            text=True
        )

        duration = round( float(result.stdout.strip()),  2)

        return templates.TemplateResponse(
            request=request,
            name="mp3_cutter_editor.html",
            context={
                "filename": os.path.basename(input_file),
                "duration": duration
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="mp3_cutter.html",
            context={
                "error": str(e)
            }
        )

@app.get("/audio-converter")
async def audio_converter_page(
    request: Request
):
    record_visit("audio-converter")
    return templates.TemplateResponse(
        request=request,
        name="audio_converter.html"
    )


@app.post("/audio-converter")
async def audio_converter(
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        output_file = (
            f"output/{uuid.uuid4()}.{output_format}"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                output_file
            ],
            check=True
        )

        media_types = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "aac": "audio/aac",
            "m4a": "audio/mp4",
            "ogg": "audio/ogg",
            "flac": "audio/flac"
        }

        return FileResponse(
            output_file,
            media_type=media_types.get(
                output_format,
                "application/octet-stream"
            ),
            filename=f"converted.{output_format}"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/merge-audio")
async def merge_audio_page(
    request: Request
):
    record_visit("merge-audio")
    return templates.TemplateResponse(
        request=request,
        name="merge_audio.html"
    )


@app.post("/merge-audio")
async def merge_audio(
    files: list[UploadFile] = File(...)
):
    try:

        audio_files = []

        for file in files:

            filepath = (
                f"uploads/{uuid.uuid4()}_{file.filename}"
            )

            with open(filepath, "wb") as f:
                f.write(await file.read())

            audio_files.append(filepath)

        concat_file = (
            f"uploads/{uuid.uuid4()}_concat.txt"
        )

        with open(concat_file, "w") as f:

            for audio in audio_files:

                abs_path = os.path.abspath(audio)

                f.write(
                    f"file '{abs_path}'\n"
                )

        output_file = (
            f"output/{uuid.uuid4()}.mp3"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_file,
                "-c",
                "copy",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="merged.mp3"
        )

    except Exception as e:

        return {
            "error": str(e)
        }
    

@app.get("/video-to-mp3")
async def video_to_mp3_page(
    request: Request
):
    record_visit("video-to-mp3")
    return templates.TemplateResponse(
        request=request,
        name="video_to_mp3.html"
    )


@app.post("/video-to-mp3")
async def video_to_mp3(
    file: UploadFile = File(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        output_file = (
            f"output/{uuid.uuid4()}.mp3"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-vn",
                "-acodec",
                "libmp3lame",
                "-q:a",
                "2",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="video_audio.mp3"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/add-audio-to-video")
async def add_audio_to_video_page(
    request: Request
):
    record_visit("add-audio-to-video")
    return templates.TemplateResponse(
        request=request,
        name="add_audio_to_video.html"
    )


@app.post("/add-audio-to-video")
async def add_audio_to_video(

    video: UploadFile = File(...),
    audio: UploadFile = File(...)

):
    try:

        video_path = (
            f"uploads/{uuid.uuid4()}_{video.filename}"
        )

        audio_path = (
            f"uploads/{uuid.uuid4()}_{audio.filename}"
        )

        with open(video_path, "wb") as f:
            f.write(await video.read())

        with open(audio_path, "wb") as f:
            f.write(await audio.read())

        output_file = (
            f"output/{uuid.uuid4()}.mp4"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-i",
                audio_path,
                "-c:v",
                "copy",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-shortest",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="video/mp4",
            filename="video_with_audio.mp4"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/video-compressor")
async def video_compressor_page(
    request: Request
):
    record_visit("video-compressor")
    return templates.TemplateResponse(
        request=request,
        name="video_compressor.html"
    )


@app.post("/video-compressor")
async def video_compressor(
    file: UploadFile = File(...),
    quality: str = Form(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        if quality == "high":
            crf = "23"

        elif quality == "max":
            crf = "32"

        else:
            crf = "28"

        output_file = (
            f"output/{uuid.uuid4()}.mp4"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-vcodec",
                "libx264",
                "-crf",
                crf,
                "-preset",
                "medium",
                "-acodec",
                "aac",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="video/mp4",
            filename="compressed_video.mp4"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/video-to-gif")
async def video_to_gif_page(
    request: Request
):
    record_visit("video-to-gif")
    return templates.TemplateResponse(
        request=request,
        name="video_to_gif.html"
    )


@app.post("/video-to-gif")
async def video_to_gif(
    file: UploadFile = File(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        output_file = (
            f"output/{uuid.uuid4()}.gif"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-vf",
                "fps=10,scale=600:-1:flags=lanczos",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="image/gif",
            filename="animated.gif"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/gif-to-video")
async def gif_to_video_page(
    request: Request
):
    record_visit("gif-to-video")
    return templates.TemplateResponse(
        request=request,
        name="gif_to_video.html"
    )

@app.post("/gif-to-video")
async def gif_to_video(
    file: UploadFile = File(...)
):
    try:

        input_file = (
            f"uploads/{uuid.uuid4()}_{file.filename}"
        )

        with open(input_file, "wb") as f:
            f.write(await file.read())

        output_file = (
            f"output/{uuid.uuid4()}.mp4"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-movflags",
                "+faststart",
                "-pix_fmt",
                "yuv420p",
                output_file
            ],
            check=True
        )

        return FileResponse(
            output_file,
            media_type="video/mp4",
            filename="converted.mp4"
        )

    except Exception as e:

        return {
            "error": str(e)
        }

@app.get("/photo-to-video")
async def photo_to_video_page(
    request: Request
):
    record_visit("photo-to-video")
    return templates.TemplateResponse(
        request=request,
        name="photo_to_video.html"
    )

@app.post("/photo-to-video")
async def photo_to_video(
    files: list[UploadFile] = File(...)
):
    try:

        folder = f"uploads/{uuid.uuid4()}"
        os.makedirs(folder, exist_ok=True)

        for idx, file in enumerate(files):

            jpg_path = os.path.join(
                folder,
                f"{idx:03d}.jpg"
            )

            image_data = await file.read()

            with open(jpg_path, "wb") as f:
                f.write(image_data)

            img = Image.open(jpg_path)

            if img.mode != "RGB":
                img = img.convert("RGB")

            # Resize while preserving aspect ratio
            img.thumbnail(
                (1280, 720),
                Image.Resampling.LANCZOS
            )

            # Make width and height even numbers
            width, height = img.size

            width = width if width % 2 == 0 else width - 1
            height = height if height % 2 == 0 else height - 1

            img = img.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            img.save(
                jpg_path,
                "JPEG",
                quality=95
            )

        output_file = (
            f"output/{uuid.uuid4()}.mp4"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                "0.33",          # 3 sec per image
                "-i",
                os.path.join(
                    folder,
                    "%03d.jpg"
                ),
                "-vf",
                "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-c:v",
                "libx264",
                "-r",
                "30",
                "-pix_fmt",
                "yuv420p",
                output_file
            ],
            check=True,
            capture_output=True
        )

        return FileResponse(
            output_file,
            media_type="video/mp4",
            filename="slideshow.mp4"
        )

    except subprocess.CalledProcessError as e:

        return {
            "error": e.stderr.decode()
        }

    except Exception as e:

        return {
            "error": str(e)
        }
            
@app.post("/cut-mp3")
async def cut_mp3(
    filename: str = Form(...),
    start_time: float = Form(...),
    end_time: float = Form(...)
):
    try:

        input_file = os.path.join(
            "uploads",
            filename
        )

        if not os.path.exists(input_file):
            raise Exception(
                "Source audio file not found"
            )

        output_file = os.path.join(
            "output",
            f"{uuid.uuid4()}.mp3"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                str(start_time),
                "-to",
                str(end_time),
                "-i",
                input_file,
                "-c:a",
                "libmp3lame",
                "-q:a",
                "2",
                output_file
            ],
            check=True,
            capture_output=True
        )

        return FileResponse(
            path=output_file,
            media_type="audio/mpeg",
            filename="trimmed.mp3"
        )

    except subprocess.CalledProcessError as e:

        error_message = (
            e.stderr.decode()
            if e.stderr
            else str(e)
        )

        return HTMLResponse(
            content=error_message,
            status_code=500
        )

    except Exception as e:

        return HTMLResponse(
            content=str(e),
            status_code=500
        )


        

@app.get("/audio-file/{filename}")
async def audio_file(
    filename: str
):
    record_visit("audio-file")
    filepath = os.path.join(
        "uploads",
        filename
    )

    if not os.path.exists(filepath):

        return {
            "error": "Audio file not found"
        }

    return FileResponse(
        filepath,
        media_type="audio/mpeg"
    )



@app.post("/compare-pdf")
async def compare_pdf(

    request: Request,

    file1: UploadFile = File(...),

    file2: UploadFile = File(...)

):

    pdf1 = f"uploads/{uuid.uuid4()}.pdf"
    pdf2 = f"uploads/{uuid.uuid4()}.pdf"

    with open(pdf1,"wb") as f:
        f.write(await file1.read())

    with open(pdf2,"wb") as f:
        f.write(await file2.read())

    text1 = ""

    for page in PdfReader(pdf1).pages:

        extracted = page.extract_text()

        if extracted:
            text1 += extracted

    text2 = ""

    for page in PdfReader(pdf2).pages:

        extracted = page.extract_text()

        if extracted:
            text2 += extracted

    similarity = round(

        SequenceMatcher(
            None,
            text1,
            text2
        ).ratio() * 100,

        2

    )

    return templates.TemplateResponse(

        request=request,

        name="compare_pdf.html",

        context={
            "similarity": similarity
        }

    )

    


@app.get("/sql-formatter")
async def sql_formatter_page(request: Request):
    record_visit("sql-formatter")
    return templates.TemplateResponse(
        request=request,
        name="sql_formatter.html"
    )

@app.get("/speech-to-text")
async def speech_to_text_page(
    request: Request
):
    record_visit("speech-to-text")
    return templates.TemplateResponse(
        request=request,
        name="speech_to_text.html"
    )

@app.get("/converters", response_class=HTMLResponse)
async def converters(request: Request):
    record_visit("converters")
    return templates.TemplateResponse(
        request=request,
        name="converters.html"
    )


@app.get("/password-generator", response_class=HTMLResponse)
async def password_generator(request: Request):
    record_visit("password-generator")
    return templates.TemplateResponse(
        request=request,
        name="password_generator.html"
    )

@app.get("/url-encoder", response_class=HTMLResponse)
async def url_encoder_page(request: Request):
    record_visit("url-encoder")
    return templates.TemplateResponse(
        request=request,
        name="url_encoder.html"
    )

@app.get("/unlock-pdf")
async def unlock_pdf(request: Request):
    record_visit("unlock-pdf")
    return templates.TemplateResponse(
        request=request,
        name="unlock_pdf.html"
    )

@app.get("/resize-image")
async def resize_image_page(request: Request):
    record_visit("resize-image")
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
    record_visit("image-converter")

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
    record_visit("json-validator")
    return templates.TemplateResponse(
        request=request,
        name="json_validator.html"
    )

@app.get("/jwt-decoder")
async def jwt_decoder(request: Request):
    record_visit("jwt-decoder")
    return templates.TemplateResponse(
        request=request,
        name="jwt_decoder.html"
    )

@app.get("/pdf-watermark")
async def pdf_watermark(
    request: Request
):
    record_visit("pdf-watermark")
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
    record_visit("timestamp-converter")
    return templates.TemplateResponse(
        request=request,
        name="timestamp_converter.html"
    )

@app.get("/signature-generator")
async def signature_generator(
    request: Request
):
    record_visit("signature-generator")
    return templates.TemplateResponse(
        request=request,
        name="signature_generator.html"
    )

@app.get("/image-watermark")
async def image_watermark(
    request: Request
):
    record_visit("image-watermark")
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
    record_visit("cron-generator")
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
    record_visit("ai-prompt-generator")
    return templates.TemplateResponse(
        request=request,
        name="ai_prompt_generator.html"
    )


@app.get("/excel-to-pdf")
async def excel_to_pdf_page(
    request: Request
):
    record_visit("excel-to-pdf")
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
    record_visit("holidays")
    return templates.TemplateResponse(
        request=request,
        name="holidays.html"
    )


@app.get("/api/holidays/{country}/{year}")
async def get_holidays(
    country: str,
    year: int
):
    record_visit("holidays")
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
    record_visit("weather")

    return templates.TemplateResponse(
        request=request,
        name="weather.html"
    )

@app.get("/ip-lookup", response_class=HTMLResponse)
async def ip_lookup(request: Request):
    record_visit("ip-lookup")
    return templates.TemplateResponse(
        request=request,
        name="ip_lookup.html"
    )

@app.get("/timezone-converter", response_class=HTMLResponse)
async def timezone_converter(request: Request):
    record_visit("timezone-converter")
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

    conn = sqlite3.connect("tools.db")

    popular_tools = conn.execute("""
        SELECT tool_name, visits
        FROM tool_visits
        ORDER BY visits DESC
        LIMIT 8
    """).fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "popular_tools": popular_tools,
            "tool_links": TOOL_LINKS,
            "tool_icons": TOOL_ICONS,
            "tool_names": TOOL_NAMES
        }
    )

@app.get("/svg-to-png", response_class=HTMLResponse)
async def svg_to_png_page(request: Request):
    record_visit("svg-to-png")
    return templates.TemplateResponse(
        request=request,
        name="svg_to_png.html"
    )

@app.get("/ocr-pdf-page", response_class=HTMLResponse)
async def ocr_pdf_page(request: Request):
    record_visit("ocr-pdf-page")
    return templates.TemplateResponse(
        request=request,
        name="ocr_pdf.html"
    )

@app.get("/text-utilities", response_class=HTMLResponse)
async def text_utilities_page(request: Request):
    record_visit("text-utilities")
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
    record_visit("csv-to-json")
    return templates.TemplateResponse(
        request=request,
        name="csv_to_json.html"
    )

@app.get("/json-to-csv", response_class=HTMLResponse)
async def json_to_csv_page(request: Request):
    record_visit("json-to-csv")
    return templates.TemplateResponse(
        request=request,
        name="json_to_csv.html"
    )

@app.get("/xml-to-json", response_class=HTMLResponse)
async def xml_to_json_page(request: Request):
    record_visit("xml-to-json")
    return templates.TemplateResponse(
        request=request,
        name="xml_to_json.html"
    )

@app.get("/json-to-xml", response_class=HTMLResponse)
async def json_to_xml_page(request: Request):
    record_visit("json-to-xml")
    return templates.TemplateResponse(
        request=request,
        name="json_to_xml.html"
    )

@app.get("/yaml-to-json", response_class=HTMLResponse)
async def yaml_to_json_page(request: Request):
    record_visit("yaml-to-json")
    return templates.TemplateResponse(
        request=request,
        name="yaml_to_json.html"
    )

@app.get("/json-to-yaml", response_class=HTMLResponse)
async def json_to_yaml_page(request: Request):
    record_visit("json-to-yaml")
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
    record_visit("jfif-to-jpg")
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
    record_visit("heic-to-jpg")
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

@app.get("/age-calculator")
async def age_calculator(request: Request):
    record_visit("age-calculator")
    return templates.TemplateResponse(
        request,
        "age-calculator.html"
    )

@app.get("/emi-calculator", response_class=HTMLResponse)
async def emi_calculator():
    record_visit("emi-calculator")
    with open("templates/emi-calculator.html") as f:
        return HTMLResponse(f.read())

@app.get("/merge", response_class=HTMLResponse)
async def merge_page(request: Request):
    record_visit("merge")
    return templates.TemplateResponse(
        request=request,
        name="merge.html"
    )



@app.get("/text-compare")
async def text_compare(request: Request):
    record_visit("text-compare")
    return templates.TemplateResponse(
        request=request,
        name="text-compare.html",
        context={
            "text1": "",
            "text2": ""
        }
    )

@app.post("/text-compare")
async def compare_text(
    request: Request,
    text1: str = Form(...),
    text2: str = Form(...)
):

    similarity = round(
        SequenceMatcher(None, text1, text2).ratio() * 100,
        2
    )

    return templates.TemplateResponse(
        request=request,
        name="text-compare.html",
        context={
            "text1": text1,
            "text2": text2,
            "similarity": similarity,
            "chars1": len(text1),
            "chars2": len(text2),
            "lines1": len(text1.splitlines()),
            "lines2": len(text2.splitlines())
        }
    )

@app.get("/remove-background")
async def remove_background_page(request: Request):
    record_visit("remove-background")
    return templates.TemplateResponse(
        request=request,
        name="remove_background.html"
    )

@app.get("/word-to-pdf")
async def word_to_pdf_page(request: Request):
    record_visit("word-to-pdf")
    return templates.TemplateResponse(
        request=request,
        name="word_to_pdf.html"
    )

@app.get("/webp-to-jpg")
async def webp_to_jpg_page(request: Request):
    record_visit("webp-to-jpg")
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
    record_visit("pdf-to-word")
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
    record_visit("json-formatter")
    return templates.TemplateResponse(
        request=request,
        name="json_formatter.html"
    )

@app.get("/qr-generator", response_class=HTMLResponse)
async def qr_generator_page(request: Request):
    record_visit("qr-generator")
    return templates.TemplateResponse(
        request=request,
        name="qr_generator.html"
    )

@app.get("/split", response_class=HTMLResponse)
async def split_page(request: Request):
    record_visit("split")
    return templates.TemplateResponse(
        request=request,
        name="split.html"
    )

@app.get("/pdf-to-jpg", response_class=HTMLResponse)
async def pdf_to_jpg_page(request: Request):
    record_visit("pdf-to-jpg")
    return templates.TemplateResponse(
        request=request,
        name="pdf_to_jpg.html"
    )


@app.get("/rotate", response_class=HTMLResponse)
async def rotate_page(request: Request):
    record_visit("rotate")
    return templates.TemplateResponse(
        request=request,
        name="rotate.html"
    )


@app.get("/delete-pages", response_class=HTMLResponse)
async def delete_pages_page(request: Request):
    record_visit("delete-pages")
    return templates.TemplateResponse(
        request=request,
        name="delete_pages.html"
    )


@app.get("/extract-pages", response_class=HTMLResponse)
async def extract_pages_page(request: Request):
    record_visit("extract-pages")
    return templates.TemplateResponse(
        request=request,
        name="extract_pages.html"
    )


@app.get("/protect-pdf", response_class=HTMLResponse)
async def protect_pdf_page(request: Request):
    record_visit("protect-pdf")
    return templates.TemplateResponse(
        request=request,
        name="protect_pdf.html"
    )

@app.get("/image-compressor", response_class=HTMLResponse)
async def image_compressor_page(request: Request):
    record_visit("image-compressor")
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
    record_visit("base64-tool")
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
    record_visit("compress")
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
    record_visit("images-to-pdf")
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