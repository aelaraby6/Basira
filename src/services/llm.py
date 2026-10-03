import ollama
from src.config import MODEL, SYSTEM_PROMPT


def explain(text: str, language_name: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(language_name=language_name),
            },
            {
                "role": "user",
                "content": f"Here is the text from the document:\n\n{text}",
            },
        ],
        options={"temperature": 0.2},
    )
    return response["message"]["content"].strip()
