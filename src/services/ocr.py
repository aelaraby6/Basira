from PIL import Image, ImageOps
import pytesseract


def prepare_image(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img)
    if img.width < 1500:
        scale = 1500 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)))
    return img


def read_text(img: Image.Image, ocr_lang: str) -> str:
    img = prepare_image(img)
    text = pytesseract.image_to_string(img, lang=ocr_lang)
    return text.strip()
