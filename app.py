import gradio as gr
from src.ui.app_ui import create_ui, CUSTOM_CSS

demo = create_ui()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(primary_hue="yellow", neutral_hue="slate"),
        css=CUSTOM_CSS,
    )