# Basira

**A private, offline document reader for people with low vision.**
Take a photo of a paper, bill, or medicine leaflet. Basira reads it aloud and explains it in simple words, all on your own computer, with no cloud and no subscription.

---

## Table of Contents

1. [What Basira Does](#1-what-basira-does)
2. [Why Open Source](#2-why-open-source)
3. [How It Works](#3-how-it-works)
4. [Tech Stack](#4-tech-stack)
5. [Requirements](#5-requirements)
6. [Step-by-Step Setup](#6-step-by-step-setup)
7. [Project Structure](#7-project-structure)
8. [Run It](#8-run-it)
9. [Use It From a Phone](#9-use-it-from-a-phone)
10. [Troubleshooting](#10-troubleshooting)
11. [Safety Notes](#11-safety-notes)
12. [Future Ideas](#12-future-ideas)
13. [License](#13-license)

---

## 1. What Basira Does

| Step | What happens |
|------|--------------|
| 1. Capture | The user uploads or photographs a document. |
| 2. Read | OCR (text recognition) turns the image into text. |
| 3. Explain | A small local AI model rewrites the text in simple, clear language and highlights key information: amounts, dates, deadlines, and required actions. |
| 4. Speak | A local text-to-speech voice reads the text or explanation aloud. |

**Main features**

- Works in **Arabic and English**
- Very **large text and high-contrast** interface
- Option to read the original verbatim text or the AI simplified explanation
- Runs **fully offline** after initial setup
- Free to run, with no accounts or API keys required

---

## 2. Why Open Source

- **Privacy:** Bills, medical papers, and ID documents are sensitive. With local models, nothing ever leaves your device.
- **Offline:** Works without internet connection.
- **Free forever:** No per-page fees, subscriptions, or API rate limits.
- **Modular components:** Easily change the AI model, voice, or OCR language.
- **Customizable behavior:** Fine-tune prompts to tailor explanation detail.

---

## 3. How It Works

```
+----------+    +-----------+    +----------------+    +-----------+    +----------+
|  Photo   | -> | Tesseract | -> | Local LLM      | -> |   Piper   | -> |  Audio   |
| (image)  |    |   (OCR)   |    | (Ollama)       |    |   (TTS)   |    |  + Text  |
+----------+    +-----------+    +----------------+    +-----------+    +----------+
                      +---------------  Gradio web interface  ---------------+
```

---

## 4. Tech Stack

| Job | Tool | Why |
|-----|------|-----|
| Language | **Python 3.10+** | Versatile and ecosystem-rich |
| Web interface | **Gradio** | Fast, high-contrast, accessible UI |
| OCR | **Tesseract** (`pytesseract`) | Open-source OCR with Arabic support |
| Image cleanup | **Pillow** | Preprocessing to improve OCR accuracy |
| Local AI model | **Ollama** (`qwen2.5:3b`) | Efficient local LLM inference |
| Text to speech | **Piper** (`piper-tts`) | Fast, local neural TTS with Arabic and English voices |

Model tip: 3B models run on most laptops. If your system has 16 GB+ RAM, 7B/8B models provide higher explanation accuracy.

---

## 5. Requirements

- PC or laptop with **8 GB RAM minimum** (16 GB recommended)
- About **10 GB free disk space**
- Internet connection for initial setup and model downloads only
- No dedicated GPU required

---

## 6. Step-by-Step Setup

### Step 1: Install Python

Install Python 3.10 or newer from https://www.python.org/downloads/
On Windows, ensure you check **"Add Python to PATH"**.

### Step 2: Set Up Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### Step 3: Install Tesseract (OCR)

- **Windows:** Download the installer from UB Mannheim. During setup, select the **Arabic language data**.
- **macOS:**
  ```bash
  brew install tesseract tesseract-lang
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng
  ```

### Step 4: Install Ollama and Download Model

1. Download Ollama from https://ollama.com/download
2. Pull the default model:
   ```bash
   ollama pull qwen2.5:3b
   ```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Download Piper Voices

Download English and Arabic voice models into the `voices/` folder:

```bash
python -m piper.download_voices --download-dir voices en_US-lessac-medium ar_JO-kareem-medium
```

---

## 7. Project Structure

```
Basira/
├── src/
│   ├── config.py             # Settings, paths, and language definitions
│   ├── services/
│   │   ├── ocr.py            # Image preprocessing & Tesseract OCR
│   │   ├── llm.py            # Ollama text explanation
│   │   └── tts.py            # Piper TTS voice synthesis & caching
│   ├── core/
│   │   └── processor.py      # Core document processing pipeline
│   └── ui/
│       └── app_ui.py         # Gradio user interface layout & styling
├── voices/                   # Downloaded Piper ONNX models (gitignored)
├── app.py                    # Application entry point
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 8. Run It

1. Ensure Ollama is running (`ollama serve` if not started as a service).
2. Start the application:
   ```bash
   python app.py
   ```
3. Open http://localhost:7860 in your browser.
4. Upload or capture a document, choose language and read mode, and click **Read it to me**.

---

## 9. Use It From a Phone

1. Connect your phone and computer to the **same Wi-Fi network**.
2. Find your computer's local IP address (`ipconfig` on Windows or `ifconfig`/`ip a` on Linux/macOS).
3. On your phone's browser, navigate to `http://<local-ip>:7860` (e.g., `http://192.168.1.50:7860`).
4. Tap the image box and take a photo directly from your phone camera.

---

## 10. Troubleshooting

| Problem | Fix |
|---------|-----|
| `TesseractNotFoundError` | Verify Tesseract is installed. `src/config.py` checks default Windows paths automatically. |
| Arabic OCR outputs incorrect characters | Run `tesseract --list-langs` to ensure `ara` is installed. |
| `Connection refused` from Ollama | Start Ollama service (`ollama serve`). |
| TTS audio errors | Ensure voice models are downloaded into `voices/`. |
| Phone cannot access the UI | Ensure both devices are on the same Wi-Fi and firewall allows port 7860. |

---

## 11. Safety Notes

Basira is an assistant tool, not a certified legal or medical authority:
- OCR and language models can make mistakes, especially with low-quality or blurry photos.
- For medical prescriptions or critical legal papers, always verify with a professional or trusted person.
- All processing occurs completely offline on your local machine.

---

## 12. Future Ideas

- Voice commands for hands-free scanning (Whisper integration)
- Expanded language support
- Local document reading history
- Local vision models (VLM) for complex layouts
- Progressive Web App (PWA) packaging

---

## 13. License

Released under the **MIT License**. Free to use, copy, modify, and distribute.
