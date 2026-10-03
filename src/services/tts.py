import tempfile
import wave
from pathlib import Path
from piper.voice import PiperVoice
from src.config import VOICES_DIR

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
