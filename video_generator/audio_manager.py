from random import shuffle
from TTS.api import TTS
import torch, misc

voices={"test":"test"}
male=["apple","lemon","watermelon","grape","blueberry"]
female=["banana","orange","peach","strawberry","cherry"]

def create_speech(text:str, speaker:str, output_name:str, preset:str="ultra_fast", model_path:str="tts_models/en/multi-dataset/tortoise-v2")->None:
    """
    preset list:
    single_sample, ultra_fast, ultra_fast_old, very_fast, fast, fast_old, standard, high_quality
    """
    print("\nIGNORE ALL WARNINGS AND ERRORS")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using:", device)
    tts = TTS(model_path).to(device)
    print(text)
    tts.tts_to_file(
        text=text,
        file_path="speech\\"+output_name+".wav",
        voice_dir="speaker",
        speaker=speaker,
        preset=preset
    )

def dialogues_to_speech(dialogues:list)->None:
    for i in range(len(dialogues)):
        dialogue=dialogues[i].split(":")
        create_speech(dialogue[1],voices[dialogue[0]],"speech\\"+str(i)+"_speech")

def setup_voices(characters:list)->None:
    shuffle(male)
    shuffle(female)
    m,f=0,0
    for c in characters:
        character=c.split("-")
        if character[0]=="male":
            voices[character[1]] = male[m]
            m+=1
        else:#female. other genders are defaulted to female voice currently
            voices[character[1]] = female[f]
            f+=1

def setup_voices_with_script(script:str)->None:
    return setup_voices(misc.script_to_characters(script))

# ==================================================TESTING==================================================
#create_speech("Hello John. Cool car Cole.",preset="high_quality")