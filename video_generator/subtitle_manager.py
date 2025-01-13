from faster_whisper import WhisperModel
from moviepy import TextClip, concatenate_videoclips, VideoClip
import re

from sympy.physics.optics import lens_makers_formula

from animateable import Animateable


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

def section_words(words_and_stamps: list, split_threshold: float = 0.75) -> list:
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
        if words and (v[1] - s >= split_threshold or re.search("[.,?!;]", v[2])):
            sectioned_subtitles.append((s, e, "".join(words).lstrip()))
            words = []
            s = e
        words.append(re.sub("[.,?!;]", "", v[2]))
        e = v[1]
    if words:
        sectioned_subtitles.append((s, e, "".join(words).lstrip()))
    return sectioned_subtitles

def sectioned_subtitles_to_subtitles(sectioned_subtitles:list,pulse:bool=False,pos:tuple=(0,0),left:bool=True)->tuple:
    #I have observed so far that it is one after another
    m,mh=0,0
    subtitle_list=[]
    s,p=[],[]
    t=0
    for ss in sectioned_subtitles:
        temp=TextClip(
            font='verdana',
            stroke_width=5,
            stroke_color='black',
            text=ss[2],
            font_size=50,
            color='yellow',
            horizontal_align='left'if left else'right',
            duration=ss[1]-ss[0]
        )
        temp.size=(temp.size[0],temp.size[1]+20)
        if pulse:
            b=bounce(temp.w, temp.h ,pos[0],pos[1],t)
            s.extend(b[0])
            p.extend(b[1])
        mh=max(mh,temp.h)
        m=max(m,temp.w)
        t+=temp.duration
        subtitle_list.append(temp)
    temp2 = Animateable(concatenate_videoclips(subtitle_list),pos[0],pos[1])
    for tu in s:
        temp2.queue_scale(tu[0],tu[1],tu[2],tu[3],tu[4])
    for tu in p:
        temp2.queue_move(tu[0],tu[1],tu[2],tu[3],tu[4])
    temp2.establish()
    return temp2.clip,m,mh

def bounce(w:int, h:int, x:int, y:int, t:int)->tuple:#bounce effect
    a,b=0.02,8
    s,p=[],[]
    s.append((t, a, w, h, False))
    p.append((t, a, x, y, False))
    tot=a
    while tot<=a*3:
        w+=2*b
        h+=h/w*2*b
        x+=-1*b
        y+=-h/w*b
        s.append((t+tot,a,w,h,False))
        p.append((t+tot, a, x, y, False))
        tot+=a
    while tot<=a*6:
        w-=2*b
        h-=h/w*2*b
        x-=-1*b
        y-=-h/w*b
        s.append((t+tot,a,w,h,False))
        p.append((t+tot, a, x, y, False))
        tot += a
    return s,p

# ==================================================TESTING==================================================
'''
li = speech_to_text("speech.wav", "medium")
li = section_words(li, 1.25)
# test with 1sec
print(li)
'''