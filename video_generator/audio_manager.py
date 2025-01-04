from TTS.api import TTS
import torch

def create_speech(text:str, preset:str="ultra_fast", model_path:str="tts_models/en/multi-dataset/tortoise-v2", )->None:
    print("IGNORE ALL WARNINGS AND ERRORS")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using:", device)
    tts = TTS(model_path).to(device)
    tts.tts_to_file(
        text=text,
        file_path="speech.wav",
        voice_dir="speaker",
        speaker="test",
        preset=preset
    )

"""
preset list:
single_sample
ultra_fast
ultra_fast_old
very_fast
fast
fast_old
standard
high_quality
"""
# ==================================================TESTING==================================================
create_speech("Hello John. Cool car Cole.",preset="high_quality")