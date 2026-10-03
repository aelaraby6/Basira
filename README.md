# 👁️ Basira (بصيرة)

**A private, offline document reader for people with low vision.**
Take a photo of a paper, bill, or medicine leaflet. Basira reads it aloud and explains it in simple words, all on your own computer, with no cloud and no subscription.

> Built for the **Hacktoberfest 2026 Weekend Challenge: Build for a Friend**.
> Built for: *[write the name of your real person here, e.g. "my grandfather"]*.

---

## Table of Contents

1. [What Basira Does](#1-what-basira-does)
2. [Why Open Source Matters Here](#2-why-open-source-matters-here)
3. [How It Works](#3-how-it-works)
4. [Tech Stack](#4-tech-stack)
5. [Before You Start (Requirements)](#5-before-you-start-requirements)
6. [Step-by-Step Setup](#6-step-by-step-setup)
7. [The Code](#7-the-code)
8. [Run It](#8-run-it)
9. [Test It](#9-test-it)
10. [Use It From a Phone](#10-use-it-from-a-phone)
11. [Hand It Over to Your Person](#11-hand-it-over-to-your-person)
12. [24-Hour Build Plan](#12-24-hour-build-plan)
13. [Troubleshooting](#13-troubleshooting)
14. [Safety Notes](#14-safety-notes)
15. [Future Ideas](#15-future-ideas)
16. [DEV Post Template](#16-dev-post-template)
17. [License](#17-license)

---

## 1. What Basira Does

| Step | What happens |
|------|--------------|
| 📷 **1. Capture** | The user uploads or photographs a document. |
| 🔍 **2. Read** | OCR (text recognition) turns the image into text. |
| 🧠 **3. Explain** | A small local AI model rewrites the text in simple, clear language and highlights the important parts: amounts, dates, deadlines, and what to do next. |
| 🔊 **4. Speak** | A local text-to-speech voice reads the explanation aloud. |

**Main features**

- Works in **Arabic and English**
- Very **large text and high-contrast** interface
- Reads the original text *and* a simple explanation
- Runs **fully offline** after the first setup
- Free to run, with no accounts or API keys

---

## 2. Why Open Source Matters Here

This is the part judges care about, so be specific in your post.

- **Privacy:** Bills, medical papers, and ID documents are very personal. With local models, nothing ever leaves the laptop.
- **Offline:** It works without internet, which matters in places with weak or expensive connections.
- **Free forever:** There are no per-page fees and no subscription for a family member to pay.
- **Swappable parts:** You can change the AI model, the voice, or the OCR language without rewriting anything.
- **Customizable behavior:** You control the prompt, so you can make the explanations as simple or as detailed as your person needs.

---

## 3. How It Works

```
┌──────────┐    ┌───────────┐    ┌────────────────┐    ┌───────────┐    ┌──────────┐
│  Photo   │ -> │ Tesseract │ -> │ Local LLM      │ -> │   Piper   │ -> │  Audio   │
│ (image)  │    │   (OCR)   │    │ (Ollama)       │    │   (TTS)   │    │  + Text  │
└──────────┘    └───────────┘    └────────────────┘    └───────────┘    └──────────┘
                      └───────────────  Gradio web interface  ───────────────┘
```

---

## 4. Tech Stack

All of these are open source.

| Job | Tool | Why |
|-----|------|-----|
| Language | **Python 3.10+** | Beginner friendly |
| Web interface | **Gradio** | Builds a web UI in a few lines |
| OCR | **Tesseract** (+ `pytesseract`) | Mature, supports Arabic |
| Image cleanup | **Pillow** | Improves OCR accuracy |
| Local AI model | **Ollama** + a small model such as `qwen2.5:3b` or `gemma3` | Easy to install and run locally |
| Text to speech | **Piper** | Fast, offline, many voices including Arabic |

> 💡 Model tip: Smaller models (3B) run on most laptops but make more mistakes. If your laptop has 16 GB RAM, try a 7B or 8B model. Test two or three models on **real Arabic documents** and keep the best one.

---

## 5. Before You Start (Requirements)

- A laptop or PC with **8 GB RAM minimum** (16 GB recommended)
- About **10 GB free disk space**
- Internet for the **first setup only**
- Some sample documents (a bill, a receipt, a medicine leaflet) to test with

You do **not** need a GPU.

---

## 6. Step-by-Step Setup

### Step 1: Install Python

Download Python 3.10 or newer from <https://www.python.org/downloads/>.
On Windows, **tick "Add Python to PATH"** during installation.

Check it worked by opening a terminal (Command Prompt, PowerShell, or Terminal) and typing:

```bash
python --version
```

(On Mac/Linux you may need `python3 --version`.)

### Step 2: Create the project folder

```bash
mkdir basira
cd basira
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal line.

### Step 3: Install Tesseract (OCR engine)

- **Windows:** Download the installer from the Tesseract project ("UB Mannheim" builds are the common choice). During installation, **select the Arabic language data**. Note the install path, usually `C:\Program Files\Tesseract-OCR\tesseract.exe`.
- **macOS:**
  ```bash
  brew install tesseract tesseract-lang
  ```
- **Ubuntu/Debian:**
  ```bash
  sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng
  ```

Check it:

```bash
tesseract --list-langs
```

You should see `ara` and `eng` in the list.

### Step 4: Install Ollama and download a model

1. Install Ollama from <https://ollama.com/download>.
2. Download a small model:

```bash
ollama pull qwen2.5:3b
```

3. Quick test:

```bash
ollama run qwen2.5:3b "Say hello in Arabic"
```

If you get an answer, the AI part works. Type `/bye` to exit.

### Step 5: Install the Python packages

Inside your activated venv:

```bash
pip install gradio pytesseract pillow ollama piper-tts
```

### Step 6: Download a Piper voice

Voices are `.onnx` model files. Create a folder and download one English and one Arabic voice:

```bash
mkdir voices
python -m piper.download_voices en_US-lessac-medium --data-dir voices
python -m piper.download_voices ar_JO-kareem-medium --data-dir voices
```

After this, `voices/` should contain files like `en_US-lessac-medium.onnx` and `ar_JO-kareem-medium.onnx` (each with a matching `.json`).

> ⚠️ Piper's command line has changed between versions. If a command fails, check the Piper documentation at <https://github.com/OHF-Voice/piper1-gpl> for the current syntax, or run `python -m piper --help`.

### Step 7: Folder structure

When you're done it should look like this:

```
basira/
├── venv/
├── voices/
│   ├── en_US-lessac-medium.onnx
│   ├── en_US-lessac-medium.onnx.json
│   ├── ar_JO-kareem-medium.onnx
│   └── ar_JO-kareem-medium.onnx.json
├── app.py
├── requirements.txt
└── README.md
```

---

## 7. The Code

Create a file called `app.py` and paste this in.

```python
"""
Basira - a private, offline document reader for people with low vision.
OCR (Tesseract) -> explanation (Ollama) -> speech (Piper) -> Gradio UI
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import gradio as gr
import ollama
import pytesseract
from PIL import Image, ImageOps

# ---------------------------------------------------------------
# SETTINGS - change these to fit your setup
# ---------------------------------------------------------------

# Windows only: uncomment and fix the path if Tesseract isn't found
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
def speak(text: str, voice_name: str) -> str:
    model_path = VOICES_DIR / f"{voice_name}.onnx"
    if not model_path.exists():
        raise FileNotFoundError(f"Voice not found: {model_path}")

    out_file = Path(tempfile.gettempdir()) / "basira_output.wav"
    subprocess.run(
        [sys.executable, "-m", "piper", "-m", str(model_path), "-f", str(out_file)],
        input=text.encode("utf-8"),
        check=True,
    )
    return str(out_file)


# ---------------------------------------------------------------
# 4) Put it all together
# ---------------------------------------------------------------
def process(image, language_choice):
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

    if len(raw_text) < 10:
        return ("I couldn't read much text. Try a clearer, brighter, "
                "straighter photo."), raw_text, None

    try:
        explanation = explain(raw_text, language_name)
    except Exception as e:
        return f"AI problem (is Ollama running?): {e}", raw_text, None

    try:
        audio_path = speak(explanation, settings["voice"])
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

with gr.Blocks(theme=gr.themes.Base(primary_hue="yellow", neutral_hue="slate"),
               css=CSS, title="Basira") as demo:
    gr.Markdown("# 👁️ Basira | بصيرة")
    gr.Markdown("Take a photo of a paper. I will read it and explain it to you.")

    with gr.Row():
        with gr.Column():
            image_in = gr.Image(type="pil", sources=["upload", "webcam"],
                                label="Photo of the document")
            lang = gr.Dropdown(list(LANGUAGES.keys()), value="English",
                               label="Language")
            go = gr.Button("🔊 Read it to me", variant="primary")
        with gr.Column():
            explanation_out = gr.Textbox(label="Simple explanation", lines=10)
            audio_out = gr.Audio(label="Listen", autoplay=True)
            with gr.Accordion("Original text found in the photo", open=False):
                raw_out = gr.Textbox(lines=8, label="OCR text")

    go.click(process, inputs=[image_in, lang],
             outputs=[explanation_out, raw_out, audio_out])

if __name__ == "__main__":
    # 0.0.0.0 lets other devices on your Wi-Fi (like a phone) open the app
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

Create `requirements.txt`:

```
gradio
pytesseract
pillow
ollama
piper-tts
```

---

## 8. Run It

1. Make sure Ollama is running (it usually starts automatically; if not, run `ollama serve` in another terminal).
2. In your project folder, with the venv activated:

```bash
python app.py
```

3. Open <http://localhost:7860> in your browser.
4. Upload a photo, choose a language, and press **Read it to me**.

---

## 9. Test It

Test with at least **5 real documents** and write down the results, because they make your post stronger.

| Document | Language | OCR quality | Explanation quality | Notes |
|----------|----------|-------------|---------------------|-------|
| Electricity bill | Arabic | | | |
| Pharmacy receipt | Arabic | | | |
| Medicine leaflet | English | | | |
| Official letter | Arabic | | | |
| Restaurant menu | English | | | |

**Tips for better photos**

- Good lighting, with no shadows or glare
- Hold the phone parallel to the paper
- Fill the frame with the document
- Place the paper on a dark, plain surface

**Compare models:** Try `qwen2.5:3b`, `gemma3`, and `llama3.2:3b` on the same document and note which handles Arabic best. This comparison is great content for your DEV post.

---

## 10. Use It From a Phone

Your person will probably find a phone easier than a laptop.

1. Connect the phone and laptop to the **same Wi-Fi**.
2. Find the laptop's local IP address:
   - Windows: `ipconfig` and look for "IPv4 Address"
   - Mac/Linux: `ifconfig` or `ip a`
3. On the phone's browser, open `http://<laptop-ip>:7860` (for example `http://192.168.1.20:7860`).
4. Tap the image box and choose **Camera** (or pick a photo from the gallery).

> Note: Live webcam access in a phone browser usually requires HTTPS, but **uploading a photo taken with the phone camera works fine** over plain HTTP.

**Bonus:** Add a shortcut to the phone's home screen so your person can open it with one tap.

---

## 11. Hand It Over to Your Person

The challenge gives bonus points for actually delivering it. Do this:

1. **Sit with them** and watch how they use it. Don't explain too much.
2. **Note the struggles:** Is the voice too fast? Is the text still too small? Is the photo step hard?
3. **Ask them:**
   - "Was the explanation easy to understand?"
   - "Which documents would you use this for?"
   - "What would make it better?"
4. **Adjust** (voice speed, font size, prompt wording) based on what you see.
5. **Take a photo or short video** (with their permission) and **write down their reaction in your post**.

---

## 12. 24-Hour Build Plan

| Time | Task |
|------|------|
| Hour 0-2 | Install Python, Tesseract, Ollama, and download the models and voices |
| Hour 2-4 | Run each part separately: OCR on a photo, Ollama in the terminal, Piper to make a wav file |
| Hour 4-7 | Paste `app.py`, fix errors, get the full flow working |
| Hour 7-10 | Test with real documents and improve the prompt |
| Hour 10-13 | Improve the interface and photo quality tips |
| Hour 13-16 | Hand it to your person and collect feedback |
| Hour 16-19 | Apply their feedback, record screenshots or a short demo video |
| Hour 19-23 | Write and publish the DEV post |
| Hour 23-24 | Check the submission before the deadline |

⏰ **Deadline:** Monday, October 5, 2026 at 06:59 UTC. Always confirm the exact time on the challenge page.

---

## 13. Troubleshooting

| Problem | Fix |
|---------|-----|
| `TesseractNotFoundError` | Set the `tesseract_cmd` path in `app.py` (Windows) or reinstall Tesseract |
| Arabic text comes out as garbage | Run `tesseract --list-langs`; if `ara` is missing, install the Arabic data |
| `Connection refused` from Ollama | Run `ollama serve` in another terminal |
| Model is very slow | Use a smaller model (`qwen2.5:3b` or `llama3.2:1b`) and close other apps |
| Piper command fails | Run `python -m piper --help` and adjust the command in `speak()` |
| Voice file not found | Check the `voices/` folder and the file names |
| Phone can't open the page | Same Wi-Fi? Check your firewall allows port 7860 |
| OCR misses a lot of text | Retake the photo with better light, or crop the document tighter |

---

## 14. Safety Notes

Basira is an **assistant, not an authority**.

- OCR and AI can make mistakes, especially with handwriting, blurry photos, and numbers.
- For **medicine, legal, or financial** documents, always confirm with a professional or a trusted person.
- Basira's prompt is written to admit uncertainty rather than guess. Keep that behavior.
- Everything stays on the local machine. Do not add cloud services if privacy is your selling point.

---

## 15. Future Ideas

- 📥 A "Scan again" voice command (speech-to-text with Whisper)
- 🌍 More languages and voices
- 🗂️ History of previously read documents (stored locally)
- 💵 Special mode for **money amounts and due dates** only
- 🖼️ Try a local vision model (such as a small Qwen-VL or Gemma vision model) instead of Tesseract for messy layouts
- 📱 Package as a phone-friendly app (PWA)

---

## 16. DEV Post Template

Use this outline for your submission.

```markdown
# Basira: A Private Document Reader for My [Grandfather / Aunt / Friend]

## What I Built
(2-3 sentences + a screenshot or short video)

## Who It's For
(Introduce your real person and the real problem they face.)

## Why Open Source?
- Privacy: ...
- Offline: ...
- Cost: ...
- Swappable models/voices: ...

## How It Works
(Paste the architecture diagram and briefly explain each step.)

## What I Used
Tesseract, Ollama + [model], Piper, Gradio, Python

## What Went Wrong (and How I Fixed It)
(Be honest. Judges love this.)

## Model Comparison
(Your table of models tested on Arabic documents.)

## I Handed It Over - Here's What They Said
(Their reaction, direct quotes if possible.)

## What's Next
(Future ideas.)

## Code
GitHub link
```

---

## 17. License

Released under the **MIT License**. Free to use, copy, modify, and share.

---

*Built with ❤️ for someone who deserves to read their own mail.*
