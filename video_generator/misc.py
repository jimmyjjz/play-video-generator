from moviepy import VideoClip, ImageClip, concatenate_videoclips

def generate_script_prompt(type_of_script:str, script_approx_length:int, topic:str, extra:str="")->str:
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



