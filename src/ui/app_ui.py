import gradio as gr
from src.config import LANGUAGES, READ_MODES
from src.core.processor import process

CUSTOM_CSS = """
* { font-size: 22px !important; }
h1 { font-size: 48px !important; }
textarea, .prose { font-size: 26px !important; line-height: 1.6 !important; }
button { min-height: 70px; font-weight: bold; }
"""


def create_ui() -> gr.Blocks:
    with gr.Blocks(title="Basira") as demo:
        gr.Markdown("# 👁️ Basira | بصيرة")
        gr.Markdown("Take a photo of a paper. I will read it and explain it to you.")

        with gr.Row():
            with gr.Column():
                image_in = gr.Image(
                    type="pil",
                    sources=["upload", "webcam"],
                    label="Photo of the document",
                )
                lang = gr.Dropdown(
                    list(LANGUAGES.keys()),
                    value="العربية",
                    label="Language / اللغة",
                )
                mode = gr.Radio(
                    READ_MODES,
                    value=READ_MODES[0],
                    label="What to read aloud / ماذا تريد أن تسمع؟",
                )
                go = gr.Button("🔊 Read it to me | قراءة المستند", variant="primary")

            with gr.Column():
                audio_out = gr.Audio(label="Listen / استمع", autoplay=True)
                explanation_out = gr.Textbox(
                    label="Simple explanation / الشرح والتلخيص",
                    lines=8,
                )
                with gr.Accordion("Original text found in the photo / النص الأصلي", open=True):
                    raw_out = gr.Textbox(lines=8, label="OCR text")

        go.click(
            process,
            inputs=[image_in, lang, mode],
            outputs=[explanation_out, raw_out, audio_out],
        )

    return demo
