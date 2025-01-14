from moviepy import VideoClip, ImageClip, concatenate_videoclips, TextClip, AudioFileClip
import re, audio_manager

from settings_manager import get_setting


def generate_script_prompt(content:str, min_word_count:int)->str:
    return f'Generate a {content} script. Format into sentences that are separated with "|".\
           Include only dialogue, "throwing" action, and change scene.\
           Dialogue is in this format:<name(must be a character)>:<dialogue>:<emotion>. List of emotions: thinking, ok, sad, angry, has_emotion_but_no_emoji_popup. Use has_emotion_but_no_emoji_popup 90% of the time.\
           Throwing action in this format: <thing>-<speed>-<thrower name(must be a character)>-<target name(must be a character)>. \
           List of things that can be thrown: mail, attack, tree. List of throwing speeds: slow, fast. \
           Change scene action is in the following format: <"change" the word>-<people entering(max 4) separated with commas\
           . Characters not in this list cannot talk or do anything in this scene>-<setting of the scene(keep it under 5 words)>. \
           Do not format into lines, make sure each line is right next to each other. Rarely use the throw action.\
           Do not include anything else. Do not include start and end. 10 minute script. At least {min_word_count} words.\
           Include list of all the characters in the second line in this format: gender-name1,gender-name2,gender-name3,...\
           First line is the movie title. After each change scene there must be at least one dialogue or throw action. Make sure no space before and after |.\
           Do not put | at the very end. Make sure all the people that are going to talk in a scene is in the change of that particular scene.'

def sequence_from_stamped(stamped:str, folder_path:str)->VideoClip:
    sequence_guide=[]
    for s in stamped.split(","):
        splitted = s.split("|")
        sequence_guide.append((splitted[0],splitted[1],splitted[3]))
    if not sequence_guide:
        raise ValueError("stamped is empty.")
    sequence=[]
    for i in range(len(sequence_guide)):
        sequence.append(ImageClip(folder_path+"\\"+sequence_guide[i][2]+".png", duration=float(sequence_guide[i][1])))
    return concatenate_videoclips(sequence)

def script_to_characters(script:str)->list:
    splitted=script.split("|")
    return splitted[1].split(",")

def script_to_title(script:str)->str:
    splitted=script.split("|")
    return splitted[0]

def script_to_sequence(script:str, create_speech:bool=True,create_speech_fast:bool=False)->list:
    splitted = script.split("|")
    sequence=splitted[2:]
    for i in range(len(sequence)):
        s=sequence[i].split("-")
        match len(s):
            case 1:#dialogue
                if create_speech:
                    dialogue = sequence[i].split(":")
                    if create_speech_fast:
                        audio_manager.create_speech_fast(dialogue[1], audio_manager.voices[dialogue[0]], str(i) + "_speech")
                    else:
                        audio_manager.create_speech(dialogue[1], audio_manager.voices[dialogue[0]], str(i) + "_speech",'high_quality' if get_setting("debug")==2 else 'ultra_fast')
                sequence[i] = "d"+str(i)+"###<>"+sequence[i]
            case 3:#change scene
                sequence[i] = "c"+sequence[i]
            case 4:#throw
                sequence[i] = "t"+sequence[i]
            case _:
                raise ValueError("invalid element of sequence")
    return sequence

def section_sequence(seq:list)->list:
    sectioned_sequence=[]
    accu=[]
    for s in seq:
        if s[0]=='c':
            if accu:
                sectioned_sequence.append(accu)
            accu=[]
        accu.append(s)
    sectioned_sequence.append(accu)
    return sectioned_sequence

def create_transparent_image(duration:float):#1920x1080
    img = ImageClip("assets\\compulsory\\white.png",transparent=False, duration=duration)
    img.mask=ImageClip("assets\\compulsory\\black.png",is_mask=True)
    return img

def cpos_to_rpos(size:tuple, cpos:tuple):#center pos to real pos
    #size w,h. cpos x,y
    return cpos[0]-size[0]/2,cpos[1]-size[1]/2

#========================= old prompt generators =========================
def generate_script_prompt_old(type_of_script:str, script_approx_length:int, topic:str, extra:str="")->str:
    return f"Make a {script_approx_length} second {type_of_script} script on a review on {topic}. Do not format them into blocks. Do not use apostrophes."+extra#Make the the script includes a rating({rating} out of 10) at the end.

def generate_status_prompt(obj:str, words_and_stamps:list)->str:
    return f"Give a list of timestamped actions and states of a {obj} given the following timestamped words:{words_and_stamps}. start time, duration\
           , action, and state are separated by |. The following states are available: neutral, angry, sad, thinking. The following actions are available:\
           move-right, move-down, move-left, remain. Do not format into blocks. Format into: start_time_1|duration_1|action_1|state_1,start_time_2|duration_2|action_2|state_2,...\
           .Make sure there is no overlap. Make sure it is action before state(action|state). Make sure it is ordered. Make sure all the same line.\
           Do not end with a period(.). Make sure all seconds are covered."

def generate_selection_prompt(content:str, clips_from:str, clip_time:int, total_time:int=-1, coordinating_subtitle:list=None)->str:
    #make sure total_time%clip_time==0(at least if not using coordinating_subtitle)
    #Note: It is going off of if gpt has already watched the video whose name/whatever is inputted(no video is inputted).
    if total_time%clip_time!=0:
        raise ValueError("total_time%clip_time must equal 0")
    if coordinating_subtitle is None:
        return f"Draw up a {total_time} second {content} using clips from {clips_from} that do not surpass {clip_time} seconds in the following format:\
               time_in_seconds_clip_one_start-time_in_seconds_clip_one_end_time, time_in_seconds_clip_two_start-time_in_seconds_clip_two_end_time...\
               Do not write words beyond the format stated above. Choose {total_time//clip_time} clips out of the clips you have chosen."
    else:#does not work(at least not consistently)(never seen this work)
        return f"Draw up {content} using clips from {clips_from} that do not surpass {clip_time} seconds in the following format:\
               time_in_seconds_clip_one_start-time_in_seconds_clip_one_end_time, time_in_seconds_clip_two_start-time_in_seconds_clip_two_end_time...\
               Do not write words beyond the format stated above. Given the timestamped script(extra content to work with):{coordinating_subtitle}."
