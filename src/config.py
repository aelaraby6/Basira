import os
import shutil
from pathlib import Path
import pytesseract

if not shutil.which("tesseract"):
    for _path in [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
    ]:
        if os.path.exists(_path):
            pytesseract.pytesseract.tesseract_cmd = _path
            break

MODEL = "qwen2.5:3b"
VOICES_DIR = Path("voices")

LANGUAGES = {
    "English": {"ocr": "eng", "voice": "en_US-lessac-medium"},
    "العربية": {"ocr": "ara", "voice": "ar_JO-kareem-medium"},
    "Arabic + English": {"ocr": "ara+eng", "voice": "ar_JO-kareem-medium"},
}

READ_MODES = [
    "النص الأصلي كما هو (Original Text)",
    "شرح وتلخيص المستند (AI Explanation)",
]

SYSTEM_PROMPT = """You are Basira, a kind and patient assistant who helps a person
with low vision understand paper documents.

Rules:
- Reply in {language_name}.
- Use short sentences and very simple words, as if talking to a loved one.
- Start with ONE sentence: what kind of document this is.
- Then clearly list: amounts of money, dates and deadlines, names, and
  anything the person must DO.
- The text came from OCR and may contain mistakes. If a number or word looks
  unclear, say so honestly. NEVER invent information.
- For medicine or legal papers, add: "Please confirm with a doctor/pharmacist
  or a trusted person."
- Do not use markdown symbols, bullet characters, or emojis. Your answer will
  be read aloud, so write natural spoken sentences."""
