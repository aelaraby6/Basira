"""
Basira - a private, offline document reader for people with low vision.
OCR (Tesseract) -> explanation (Ollama) -> speech (Piper) -> Gradio UI
"""

import tempfile
import wave
from pathlib import Path

import gradio as gr
import ollama
import pytesseract
from PIL import Image, ImageOps
from piper.voice import PiperVoice

# ---------------------------------------------------------------
# SETTINGS - change these to fit your setup
# ---------------------------------------------------------------

# Windows only: uncomment and fix the path if Tesseract isn't found
import shutil
import os

if not shutil.which("tesseract"):
    for _path in [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
    ]:
        if os.path.exists(_path):
            pytesseract.pytesseract.tesseract_cmd = _path
            break

MODEL = "qwen2.5:3b"          # any model you pulled with `ollama pull`
VOICES_DIR = Path("voices")

LANGUAGES = {
    "English": {"ocr": "eng", "voice": "en_US-lessac-medium"},
    "العربية": {"ocr": "ara", "voice": "ar_JO-kareem-medium"},
    "Arabic + English": {"ocr": "ara+eng", "voice": "ar_JO-kareem-medium"},
}

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


# ---------------------------------------------------------------
# 1) OCR
# ---------------------------------------------------------------
def prepare_image(img: Image.Image) -> Image.Image:
    """Clean the image to help OCR: fix rotation, grayscale, boost contrast."""
    img = ImageOps.exif_transpose(img)        # fix phone-camera rotation
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img)
    # Upscale small images; OCR works better on larger text
    if img.width < 1500:
        scale = 1500 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)))
    return img


def read_text(img: Image.Image, ocr_lang: str) -> str:
    img = prepare_image(img)
    text = pytesseract.image_to_string(img, lang=ocr_lang)
    return text.strip()


# ---------------------------------------------------------------
# 2) Explain with a local LLM
# ---------------------------------------------------------------
def explain(text: str, language_name: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system",
             "content": SYSTEM_PROMPT.format(language_name=language_name)},
            {"role": "user",
             "content": f"Here is the text from the document:\n\n{text}"},
        ],
        options={"temperature": 0.2},   # low = more careful, less creative
    )
    return response["message"]["content"].strip()


# ---------------------------------------------------------------
# 3) Text to speech with Piper
# ---------------------------------------------------------------
VOICE_CACHE: dict[str, PiperVoice] = {}


def get_voice(voice_name: str) -> PiperVoice:
    if voice_name not in VOICE_CACHE:
        model_path = VOICES_DIR / f"{voice_name}.onnx"
        if not model_path.exists():
            raise FileNotFoundError(f"Voice not found: {model_path}")
        VOICE_CACHE[voice_name] = PiperVoice.load(str(model_path))
    return VOICE_CACHE[voice_name]


def speak(text: str, voice_name: str) -> str:
    voice = get_voice(voice_name)
    out_file = Path(tempfile.gettempdir()) / "basira_output.wav"
    with wave.open(str(out_file), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    return str(out_file)


READ_MODES = [
    "النص الأصلي كما هو (Original Text)",
    "شرح وتلخيص المستند (AI Explanation)",
]


# ---------------------------------------------------------------
# 4) Put it all together
# ---------------------------------------------------------------
def process(image, language_choice, read_mode):
    if image is None:
        return "Please add a photo first.", "", None

    settings = LANGUAGES[language_choice]
    language_name = "Arabic" if "Arabic" in language_choice or language_choice == "العربية" else "English"
    if language_choice == "Arabic + English":
        language_name = "Arabic"

    try:
        raw_text = read_text(image, settings["ocr"])
    except Exception as e:
        return f"OCR problem: {e}", "", None

    if len(raw_text) < 5:
        return ("I couldn't read much text. Try a clearer, brighter, "
                "straighter photo."), raw_text, None

    # Generate AI explanation (optional / non-blocking if user only wants raw text)
    explanation = ""
    try:
        explanation = explain(raw_text, language_name)
    except Exception as e:
        explanation = f"(AI explanation unavailable: {e})"

    # Choose what to read aloud based on user selection
    if "النص الأصلي" in read_mode:
        text_to_speak = raw_text
    else:
        text_to_speak = explanation if not explanation.startswith("(AI explanation unavailable") else raw_text

    try:
        audio_path = speak(text_to_speak, settings["voice"])
    except Exception as e:
        return explanation + f"\n\n(Voice problem: {e})", raw_text, None

    return explanation, raw_text, audio_path


# ---------------------------------------------------------------
# 5) Big, high-contrast interface
# ---------------------------------------------------------------
CSS = """
* { font-size: 22px !important; }
h1 { font-size: 48px !important; }
textarea, .prose { font-size: 26px !important; line-height: 1.6 !important; }
button { min-height: 70px; font-weight: bold; }
"""

with gr.Blocks(title="Basira") as demo:
    gr.Markdown("# 👁️ Basira | بصيرة")
    gr.Markdown("Take a photo of a paper. I will read it and explain it to you.")

    with gr.Row():
        with gr.Column():
            image_in = gr.Image(type="pil", sources=["upload", "webcam"],
                                label="Photo of the document")
            lang = gr.Dropdown(list(LANGUAGES.keys()), value="العربية",
                               label="Language / اللغة")
            mode = gr.Radio(
                READ_MODES,
                value=READ_MODES[0],
                label="What to read aloud / ماذا تريد أن تسمع؟",
            )
            go = gr.Button("🔊 Read it to me | قراءة المستند", variant="primary")
        with gr.Column():
            audio_out = gr.Audio(label="Listen / استمع", autoplay=True)
            explanation_out = gr.Textbox(label="Simple explanation / الشرح والتلخيص", lines=8)
            with gr.Accordion("Original text found in the photo / النص الأصلي", open=True):
                raw_out = gr.Textbox(lines=8, label="OCR text")

    go.click(process, inputs=[image_in, lang, mode],
             outputs=[explanation_out, raw_out, audio_out])

if __name__ == "__main__":
    # 0.0.0.0 lets other devices on your Wi-Fi (like a phone) open the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(primary_hue="yellow", neutral_hue="slate"),
        css=CSS,
    )