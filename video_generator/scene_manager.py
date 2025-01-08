from random import shuffle

from moviepy import VideoClip, ImageClip, concatenate_videoclips, TextClip, AudioFileClip, CompositeVideoClip
import re, audio_manager

import subtitle_manager, misc
from animateable import Animateable

fb,pw,ph,spv=100, 160, 320, 150#from border, picture width, picture height, subtitle position value
four_formation=((fb,fb),(1920-fb-pw,1080-fb-ph),(fb,1080-fb-ph),(1920-fb-pw,fb)),((fb+spv,fb),(1920-fb-pw-spv,1080-fb-ph),(fb+spv,1080-fb-ph),(1920-fb-pw-spv,fb))
three_formation=(1920-fb-pw,1080-fb-ph),(fb,1080-fb-ph),(1920/2-pw/2,fb/4),((1920-fb-pw-spv,1080-fb-ph),(fb+spv,1080-fb-ph),(1920/2-pw/2,fb/4+spv/2))
two_formation=((1920/2+ph/2-fb/2,1080/2+ph/2),(1920/2+ph/2+fb/2,1080/2+ph/2)),((1920/2+ph/2-fb/2-spv,1080/2+ph/2),(1920/2+ph/2+fb/2+spv,1080/2+ph/2))
one_formation=(1920/2+ph/2,1080/2+ph/2),(1920/2+ph/2,1080/2+ph/2+spv/2)

fs,ss=0.5,2#fast speed, slow speed
characters={}
male=["yellow","blue"]
female=["green","magenta"]

def create_scene(seq:list):
    if len(seq)<=1:
        raise ValueError("seq does not contain enough elements")
    scene_data=seq[0][1:]
    temp=scene_data.split("-")
    names=temp[1].split(",")#idx coordinated with formation idx
    mapped_positions={}
    accumulant = []
    for i in range(len(names)):
        mapped_positions[names[i]]=i
    match len(names):
        case 1:
            a1=Animateable(ImageClip(characters[names[0]]+".png"),one_formation[0][0],one_formation[0][1])
            for i in range(1,len(seq)):
                if seq[i][0]=='d':
                    words_li=subtitle_manager.section_words(subtitle_manager.speech_to_text("speech\\"+seq[i][1]+"_speech.wav"))
                    subtitle=subtitle_manager.sectioned_subtitles_to_subtitles(words_li).with_position(one_formation[1][0],one_formation[1][1])
                    accumulant.append(subtitle)
                elif seq[i][0]=='t':
                    details=seq[1:].split("-")
                    throwable=Animateable(ImageClip(details[0]+".png"),one_formation[0][0],one_formation[0][1])
                    if details[1]=='slow':
                        throwable.queue_smooth_move(0, ss/2, one_formation[0][0],one_formation[0][1],one_formation[0][0],fb)
                        throwable.queue_smooth_move(0, ss/2, one_formation[0][0], one_formation[0][1], one_formation[0][0], one_formation[0][1])
                    elif details[1]=='fast':
                        throwable.queue_smooth_move(0, fs / 2, one_formation[0][0], one_formation[0][1],one_formation[0][0], fb)
                        throwable.queue_smooth_move(0, fs / 2, one_formation[0][0], one_formation[0][1],one_formation[0][0], one_formation[0][1])
                    else:
                        raise ValueError("not a valid throw speed")
                    throwable.establish()
                    accumulant.append(throwable.clip)
            return CompositeVideoClip([a1,concatenate_videoclips(accumulant)])
        case 2:
            a1 = Animateable(ImageClip(characters[names[0]]+".png"), two_formation[0][0][0], two_formation[0][0][1])
            a2 = Animateable(ImageClip(characters[names[1]]+".png"), two_formation[0][1][0], two_formation[0][1][1])
            for i in range(1, len(seq)):
                if seq[i][0] == 'd':
                    words = seq[i][2:].split(":")
                    words_li = subtitle_manager.section_words(subtitle_manager.speech_to_text("speech\\" + seq[i][1] + "_speech.wav"))
                    idx=mapped_positions[words[0]]
                    subtitle = subtitle_manager.sectioned_subtitles_to_subtitles(words_li).with_position(two_formation[1][idx][0], two_formation[1][idx][1])
                    accumulant.append(subtitle)
                elif seq[i][0] == 't':
                    details = seq[1:].split("-")
                    throwable = Animateable(ImageClip(details[0] + ".png"), two_formation[0][mapped_positions[details[2]]][0], two_formation[0][mapped_positions[details[2]]][1])
                    if details[1] == 'slow':
                        throwable.queue_smooth_move(0, ss, two_formation[0][mapped_positions[details[2]]][0], two_formation[0][mapped_positions[details[2]]][1],
                                                    two_formation[0][mapped_positions[details[3]]][0], two_formation[0][mapped_positions[details[3]]][1])
                    elif details[1] == 'fast':
                        throwable.queue_smooth_move(0, fs, two_formation[0][mapped_positions[details[2]]][0], two_formation[0][mapped_positions[details[2]]][1],
                                                    two_formation[0][mapped_positions[details[3]]][0], two_formation[0][mapped_positions[details[3]]][1])
                    else:
                        raise ValueError("not a valid throw speed")
                    throwable.establish()
                    accumulant.append(throwable.clip)
            return CompositeVideoClip([a1, a2, concatenate_videoclips(accumulant)])#might need to attach white and black
        case 3:
            pass
        case 4:
            pass
        case _:
            raise ValueError("invalid number of characters")

def setup_characters(ch:list)->None:
    shuffle(male)
    shuffle(female)
    m,f=0,0
    for c in ch:
        character=c.split("-")
        if character[0]=="male":
            characters[character[1]] = male[m]
            m+=1
        else:#female. other genders are defaulted to female characters currently
            characters[character[1]] = female[f]
            f+=1