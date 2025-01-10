from moviepy import ImageClip, concatenate_videoclips, TextClip, AudioFileClip, CompositeVideoClip
import audio_manager, subtitle_manager, misc, random
from animateable import Animateable

fb,pw,ph,spv,tpaw,tpah=100,240,480,120,160,80#from border, picture width, picture height, subtitle position value, throwable position adjustment width, throwable position adjustment height
formations=(
    (((1920/2-pw/2,1080/2-ph/2)),((1920/2-pw/2,1080/2-ph/2-spv))),#IGNORE YELLOW LINES(if they exist)
    (((fb,1080/2-ph/2),(1920-fb-pw,1080/2-ph/2)),((fb+pw+spv,1080/2),(1920-fb-pw-spv,1080/2))),
    (((1920/2-pw/2,1080/2-ph/2-fb),(fb,1080-ph-fb),(1920-fb-pw,1080-ph-fb)),((1920/2-pw/2,1080/2-ph/2-spv-fb),(fb+pw+spv,1080-fb-ph/2),(1920-fb-pw-spv,1080-fb-ph/2))),
    (((fb,fb),(1920-fb-pw,fb),(fb,1080-ph-fb),(1920-fb-pw,1080-ph-fb)),((fb+pw+spv,fb+ph/2),(1920-fb-pw-spv,fb+ph/2),(fb+pw+spv,1080-fb-ph/2),(1920-fb-pw-spv,1080-fb-ph/2))),
)
'''
o-----+
|     |
|     |
|     |
+-----+
o is where pos is
'''
fs,ss=0.5,2#fast speed, slow speed
characters={}
male=["microwave","mixer","pot","skillet","spatula"]
female=["dishwasher","stove","oven","whisk","toaster"]

def create_scene(seq:list):
    if len(seq)<=1:
        raise ValueError("seq does not contain enough elements")
    scene_data=seq[0][1:].split("-")
    names=scene_data[1].split(",")#idx coordinated with formation idx
    mapped_positions={}
    accumulant = [create_title(scene_data[2],False)]#False if already have speech file
    for i in range(len(names)):
        mapped_positions[names[i]]=i
    n=len(names)
    if 4<n or n<1:
        raise ValueError("invalid number of characters")
    for i in range(1, len(seq)):
        #accumulant.append(misc.create_transparent_image(0.1))#delay
        if seq[i][0] == 'd':
            words_li = subtitle_manager.section_words(subtitle_manager.speech_to_text("speech\\" + seq[i][1] + "_speech.wav"))
            idx = mapped_positions[seq[i][2:].split(":")[0]]
            subtitle = subtitle_manager.sectioned_subtitles_to_subtitles(words_li)
            subtitle = subtitle.with_position(misc.cpos_to_rpos((subtitle.w, subtitle.h), (formations[n-1][1][idx][0], formations[n-1][1][idx][1])))
            subtitle.audio = AudioFileClip("speech\\" + seq[i][1] + "_speech.wav")
            accumulant.append(CompositeVideoClip([misc.create_transparent_image(subtitle.duration), subtitle]))
        elif seq[i][0] == 't':
            details = seq[i][1:].split("-")
            if details[1] == 'slow':
                spd = ss
            elif details[1] == 'fast':
                spd = fs
            else:
                raise ValueError("not a valid throw speed")
            d=throw_direction(formations[n-1][0][mapped_positions[details[2]]][0],formations[n-1][0][mapped_positions[details[2]]][1],formations[n-1][0][mapped_positions[details[3]]][0],formations[n-1][0][mapped_positions[details[3]]][1])
            start_x,end_x=formations[n-1][0][mapped_positions[details[2]]][0] + (pw if d[0] else -tpaw),formations[n-1][0][mapped_positions[details[3]]][1] + (-tpaw if d[0] else pw)
            if d[1]==0:
                start_y, end_y=formations[n-1][0][mapped_positions[details[2]]][1] + ph / 2,formations[n-1][0][mapped_positions[details[3]]][1] + ph / 2
            else:
                start_y, end_y= formations[n - 1][0][mapped_positions[details[2]]][1] + (ph+tpah if d[1]==1 else tpah), formations[n-1][0][mapped_positions[details[3]]][1] + (tpah if d[1]==1 else ph+tpah)
            throwable = Animateable(ImageClip("assets\\" + details[0] + ".png", duration=spd), start_x, start_y)
            throwable.queue_smooth_move(0, spd, start_x, start_y, end_x, end_y)
            throwable.establish()
            accumulant.append(CompositeVideoClip([misc.create_transparent_image(spd), throwable.clip]))
        else:
            raise ValueError("invalid sequence element")
    accumulant.append(misc.create_transparent_image(0.1))  # delay
    accumulated=concatenate_videoclips(accumulant)
    composition=[accumulated]
    for j in range(n):
        a=Animateable(ImageClip("assets\\" + characters[names[j]] + ".png", duration=accumulated.duration), formations[n-1][0][j][0], formations[n-1][0][j][1])
        a.establish()
        composition.append(a.clip)
    return CompositeVideoClip(composition)

def setup_characters(ch:list)->None:
    random.shuffle(male)
    random.shuffle(female)
    m,f=0,0
    for c in ch:
        character=c.split("-")
        if character[0]=="male":
            characters[character[1]] = male[m]
            m+=1
        else:
            characters[character[1]] = female[f]
            f+=1

def create_title(title:str, create_audio:bool=True):
    if create_audio:
        audio_manager.create_speech(title,"test",title)
    try:
        tmp_a=AudioFileClip("speech\\"+title+".wav")
    except Exception:
        raise Exception("some problem occurred, check if the audio_file exists.")
    temp=TextClip(
        font='verdana',
        text=title,
        font_size=120,
        size=(1920,1080),
        color='aquamarine',
        stroke_width=5,
        stroke_color='black',
        duration=tmp_a.duration
    ).with_position("center","center")
    temp.audio=tmp_a
    return temp

def throw_direction(x1:float,y1:float,x2:float,y2:float)->tuple:
    if y2==y1:
        return 1 if x2 > x1 else 0, 0
    return 1 if x2>x1 else 0, 1 if y2>y1 else -1