from faster_whisper import WhisperModel
from moviepy import TextClip, concatenate_videoclips, VideoClip
import re


def speech_to_text(audio_file_name: str, model_type: str="medium") -> list:
    """
    Compute the timestamp of each word that is captured within a given audio file.

    :param audio_file_name: audio file of choice(mp3, wav, etc)
    :param model_type: whisper model type(tiny, small, medium, large)
    :return: timestamp of each word
    """
    model = WhisperModel(model_type)  # use medium for testing, large for product
    slots, info = model.transcribe(audio_file_name, word_timestamps=True)
    slots = list(slots)
    words_and_stamps = []
    for line in slots:
        for word in line.words:
            words_and_stamps.append((word.start, word.end, word.word))
    return words_and_stamps

def section_words(words_and_stamps: list, split_threshold: float = 1.25) -> list:
    """
    Section word and timestamps that are given are treated in a sentence-by-sentence fashion
    with each sentence sectioned into the biggest sections of text that are read under a given time.
    All occurrences of commas and periods are removed.

    :param words_and_stamps: words with each possessing their corresponding timestamp
    :param split_threshold: length(positive) in which each section of words are capped within
    :return: sectioned words
    """
    sectioned_subtitles = []
    s, e, words = 0, -1, []
    for v in words_and_stamps:
        if v[1] - s >= split_threshold or re.search("[.,?!;]", v[2]):
            sectioned_subtitles.append((s, e, "".join(words).lstrip()))
            words = []
            s = e
        words.append(re.sub("[.,?!;]", "", v[2]))
        e = v[1]
    if words:
        sectioned_subtitles.append((s, e, "".join(words).lstrip()))
    return sectioned_subtitles

def sectioned_subtitles_to_subtitles(sectioned_subtitles:list,start:float=0)->VideoClip:
    #I have observed so far that it is one after another
    subtitle_list=[]
    for ss in sectioned_subtitles:
        subtitle_list.append(TextClip(
            font='verdana',
            text=ss[2],
            font_size=40,
            color='yellow',
            duration=ss[1]-ss[0]
        ))
    temp = concatenate_videoclips(subtitle_list)
    temp.start=start
    return temp

# ==================================================TESTING==================================================
'''
li = speech_to_text("speech.wav", "medium")
li = section_words(li, 1.25)
# test with 1sec
print(li)
'''