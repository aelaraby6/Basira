from PIL import Image
from src.config import LANGUAGES
from src.services.ocr import read_text
from src.services.llm import explain
from src.services.tts import speak


def process(image: Image.Image, language_choice: str, read_mode: str):
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
        return ("I couldn't read much text. Try a clearer, brighter, straighter photo."), raw_text, None

    explanation = ""
    try:
        explanation = explain(raw_text, language_name)
    except Exception as e:
        explanation = f"(AI explanation unavailable: {e})"

    if "النص الأصلي" in read_mode:
        text_to_speak = raw_text
    else:
        text_to_speak = explanation if not explanation.startswith("(AI explanation unavailable") else raw_text

    try:
        audio_path = speak(text_to_speak, settings["voice"])
    except Exception as e:
        return explanation + f"\n\n(Voice problem: {e})", raw_text, None

    return explanation, raw_text, audio_path
