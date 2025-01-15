from moviepy import ImageClip, concatenate_videoclips, TextClip, AudioFileClip, CompositeVideoClip
import audio_manager, subtitle_manager, misc, random
import tti_manager
from settings_manager import get_setting
from animateable import Animateable

fb,pw,ph,spv,tpaw,tpah=60,240,480,30,160,80#adjusment, from border, picture width, picture height, subtitle position value, throwable position adjustment width, throwable position adjustment height
sw=600

formations=(#True is left
    (((1920/2-pw/2,1080/2-ph/2),),(True,)),
    (((fb,1080/2-ph/2),(1920-fb-pw,1080/2-ph/2)),(True,False)),
    (((1920/2-pw/2,1080/2-ph/2-fb*5),(fb,1080-ph-fb),(1920-fb-pw,1080-ph-fb)),(True,True,False)),
    (((fb,fb),(1920-fb-pw,fb),(fb,1080-ph-fb),(1920-fb-pw,1080-ph-fb)),(True,False,True,False)),
    (((fb,fb),(1920-fb-pw,fb),(fb,1080-ph-fb),(1920-fb-pw,1080-ph-fb),(1920/2-pw/2,1080/2-ph/2)),(True,False,True,False,True)),#5 formation not in use currently
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
emotion_location={"microwave":(42,42),"mixer":(66,79),"pot":(67,67),"skillet":(67,67),"spatula":(67,67),
                  "dishwasher":(50,66),"stove":(74,89),"oven":(58,64),"whisk":(73,65),"toaster":(74,89),
                  "bowl":(66,106),"sink":(66,76),"faucet":(71,60),"vent":(66,63),"knife":(52,108),"pan":(66,99)
                  }
#add emotion location
male=["microwave","mixer","pot","skillet","spatula","knife","pan","vent"]
female=["dishwasher","stove","oven","whisk","toaster","bowl","faucet","sink"]

def create_scene(seq:list):
    if len(seq)<=1:
        raise ValueError("seq does not contain enough elements")
    scene_data=seq[0][1:].split("-")
    mapped_positions,queued_emotions,et,names,title={},[],0,scene_data[1].split(","),create_title(scene_data[2],get_setting("debug")==0,get_setting("create_speech_fast"))
    accumulant=[title]
    et+=accumulant[0].duration
    for i in range(len(names)):
        mapped_positions[names[i]]=i
    n=len(names)
    if 4<n or n<1:
        raise ValueError("invalid number of characters")
    for i in range(1, len(seq)):
        if seq[i][0] == 'd':
            di = seq[i].split("###<>")
            words_li = subtitle_manager.section_words(subtitle_manager.speech_to_text("speech\\" + di[0][1:] + "_speech.wav",'large' if get_setting("debug")==0 else 'medium'))
            splitted=di[1].split(":")
            emotion,idx=splitted[2],mapped_positions[splitted[0]]
            sp=(formations[n-1][0][idx][0] + (pw+spv if formations[n-1][1][idx] else -spv-sw), formations[n-1][0][idx][1])
            subtitle = subtitle_manager.sectioned_subtitles_to_subtitles(words_li,False,sp,formations[n-1][1][idx])#True
            subtitle.audio = AudioFileClip("speech\\" + di[0][1:] + "_speech.wav")
            if emotion != "has_emotion_but_no_emoji_popup":
                queued_emotions.append((splitted[0],emotion,et,et+subtitle.duration))
            et+=subtitle.duration
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
            if d[0]==0:
                start_x, end_x = formations[n - 1][0][mapped_positions[details[2]]][0] + pw / 2, formations[n - 1][0][mapped_positions[details[3]]][0] + pw / 2
            else:
                start_x,end_x=formations[n-1][0][mapped_positions[details[2]]][0] + (pw if d[0]==1 else -tpaw),formations[n-1][0][mapped_positions[details[3]]][0] + (-tpaw if d[0]==1 else pw)
            if d[1]==0:
                start_y, end_y=formations[n-1][0][mapped_positions[details[2]]][1] + ph / 2,formations[n-1][0][mapped_positions[details[3]]][1] + ph / 2
            else:
                start_y, end_y= formations[n - 1][0][mapped_positions[details[2]]][1] + (ph+tpah if d[1]==1 else tpah), formations[n-1][0][mapped_positions[details[3]]][1] + (tpah if d[1]==1 else ph+tpah)
            throwable = Animateable(ImageClip("assets\\" + details[0] + ".png", duration=spd), start_x, start_y)
            throwable.queue_smooth_move(0, spd, start_x, start_y, end_x, end_y)
            throwable.establish()
            et+=spd
            accumulant.append(CompositeVideoClip([misc.create_transparent_image(spd), throwable.clip]))
        else:
            raise ValueError("invalid sequence element")
        accumulant.append(misc.create_transparent_image(0.5))  # delay
        et+=0.5
    accumulated=concatenate_videoclips(accumulant)
    composition=[accumulated]
    for j in range(n):
        aic=ImageClip("assets\\" + characters[names[j]] + ".png", duration=accumulated.duration)
        for e in queued_emotions:
            if e[0]==names[j]:
                ic=ImageClip("assets\\"+e[1]+".png",duration=e[3]-title.duration).with_position((emotion_location[characters[names[j]]][0],emotion_location[characters[names[j]]][1])).resized((107,107))
                ic.start=e[2]-title.duration
                aic=CompositeVideoClip([aic,ic])
        aic=CompositeVideoClip([aic,TextClip(
            font='verdana',
            text=names[j],
            font_size=40,
            size=(pw, 50),
            color='cornflowerblue' if characters[names[j]] in male else 'orchid',
            stroke_width=5,
            stroke_color='black',
            duration=accumulated.duration
        ).with_position(('center','bottom'))])
        a=Animateable(aic, formations[n-1][0][j][0], formations[n-1][0][j][1])
        a.establish()
        a.clip.start=title.duration
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

def create_title(title:str, create_audio:bool=True,create_speech_fast:bool=False):
    if create_audio:
        if create_speech_fast:
            audio_manager.create_speech_fast(title, "test", title)
        else:
            audio_manager.create_speech(title,"test",title,'high_quality' if get_setting("debug")==2 else 'ultra_fast')
    try:
        tmp_a=AudioFileClip("speech\\"+title+".wav")
    except Exception:
        raise Exception("some problem occurred, check if the audio_file exists.")
    temp=TextClip(
        font='verdana',
        text=title,
        font_size=100,
        size=(1920,1080),
        color='aquamarine',
        stroke_width=5,
        stroke_color='black',
        duration=tmp_a.duration,
    ).with_position("center","center")
    temp.audio=tmp_a
    if get_setting("debug")==0:
        tti_manager.generate_images_ani_single(title)
    return CompositeVideoClip([temp,ImageClip("temp_images\\"+title+".png",duration=tmp_a.duration).resized((450,450)).with_position(("center",580))])

def throw_direction(x1:float,y1:float,x2:float,y2:float)->tuple:
    if x2>x1:
        x=1
    elif x2==x1:
        x=0
    else:
        x=-1
    if y2>y1:
        y=1
    elif y2==y1:
        y=0
    else:
        y=-1
    return x,y