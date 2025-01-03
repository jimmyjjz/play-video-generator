#from moviepy import VideoFileClip,TextClip
from moviepy import *
#import mutagen
from mutagen.wave import WAVE
import pyttsx3
import random
import math
#1080x1920
#using 360x640 for testing
#340x570 clips size(centered
"""
Prompt to give chatgpt 

Note: Can use gpt api.

Generate an review of the anime "<insert name>" 
completed with a rating and a final note 
that takes 20secs to read.

"""
#theme theater with popsicle sticks characters(lit up by spotlight and lifted up while talking)
#while talking they should also be moving left to right(like an idle animation)
#would be cool if the stick spun around and swapped to another picture on stick as to show different emotion

print("Creating the audio and synced subtitles...")
audio_clips=[]
subtitle_clips=[]
total_length=0
with open("words_test.txt","r") as text:
    sentences=text.read().strip().split("\n")
    sentences=[l + "." for l in sentences]
    engine = pyttsx3.init()
    for i in range(len(sentences)):
        print("Working on:", sentences[i])
        sections=sentences[i].split(" ")
        for j in range(len(sections)):
            #engine.save_to_file(sections[j], str(i)+"_"+str(j)+'.wav')
            #engine.runAndWait()
            d=WAVE(str(i)+"_"+str(j)+'.wav').info.length
            subtitle_clips.append(TextClip(
                                font='verdana',
                                text=sections[j].replace(".",""),#sentences[i][:len(sentences[i])-1],
                                font_size=40,
                                color='yellow',
                                duration=d#,
                                #bg_color='yellow'
                                ))#maybe make it so it is every 1,2,3 words and not whole sentence
            #
            total_length+=d
            audio_clips.append(AudioFileClip(str(i)+"_"+str(j)+'.wav'))
    #^will error if empty line exists

    print("Completed\nTaking full video apart...")
    full_video = VideoFileClip("test_video.mkv")
    clips = []
    for i in range(0, math.ceil(total_length) if math.ceil(total_length)%2 else math.ceil(total_length)+1, 2):#temp
        clips.append(full_video.subclipped(i, i + 2))

    print("Completed\nShuffling and concatenating these clips...")
    random.shuffle(clips)
    video = concatenate_videoclips(clips)

    print("Completed\nResizing video...")
    #video=video.resized((1080,1920))#crop yeah pls
    print("Completed\nCombining video and audio components...")
    audio = concatenate_audioclips(audio_clips)
    video.audio = CompositeAudioClip([audio])
    subtitle = concatenate_videoclips(subtitle_clips).with_position('center','center')#will error if goes out of bounds
    video=video.with_position('center','center')
    bg=ImageClip("black_background.png", duration=video.duration)
    krimdus=ImageClip("krimdus_emotion_package\krimdus_neutral.png", duration=video.duration)#/
    krimdus = krimdus.with_position((460,1020))
    final_product = CompositeVideoClip([bg, video, subtitle, krimdus]).with_mask()

    print("Completed\nOutputting...")
    final_product.write_videofile("outputted_final_product.mp4", preset='ultrafast')
    #video.write_videofile("outputted_video_portion.mp4", preset='ultrafast', codec="libx264")
    #audio.write_audiofile("outputted_product_audio.mp3")
    final_product.save_frame("preview.png")

    print("Program finished")

#the "maybe to-do":
#"puppets" raising signs with pictures
#() enclosed text not spoken but shown in subtitles




'''
Yo. World Trigger.
A world where authorities deploy racist child soldiers to fend off non-sentient border hoppers.
To train such troops, the organization, Border, makes them undergo team cock fights, formally known as rank wars.
The story follows the liberal trio consisting of a global-elite smerf, Ms.good-organ-rng, and an average plus guy.
7 out of 10.
Watched the filler episodes, actually not that bad.
'''