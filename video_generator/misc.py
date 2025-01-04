from moviepy import VideoClip, ImageClip, concatenate_videoclips

def generate_script_prompt(type_of_script:str, topic:str, rating:int)->str:
    return f"Make a 20 second {type_of_script} script on a review on {topic}. Make the the script includes a rating({rating} out of 10) at the end.\
           do not format them into blocks."

def generate_actions_prompt(obj:str, words_and_stamps:list)->str:
    return f"Give a list of timestamped emotions/actions of a {obj} given the following timestamped words:{words_and_stamps}. start time, end time\
           , and action/emotion are separated by |. The following emotions are available: neutral, angry, sad, thinking. The following actions are available:\
           move-right, move-down, move-left, remain. Do not format into blocks. Format into: start_time_1|duration_1|action_or_emotion_1,start_time_2|duration_2|action_or_emotion_2,...\
           .Make sure there is no overlap. Make sure no start time is 0. Make sure it is ordered."

def generate_selection_prompt(total_time:int, content:str, clips_from:str, clip_time:int, coordinating_subtitle:list="")->str:
    #make sure total_time%clip_time==0(at least if not using coordinating_subtitle
    #Note: It is going off of if gpt has already watched the video whose name/whatever is inputted(no video is inputted).
    if total_time%clip_time!=0:
        raise ValueError("total_time%clip_time must equal 0")
    if coordinating_subtitle=="":
        return f"Draw up a {total_time} second {content} using clips from {clips_from} that do not surpass {clip_time} seconds in the following format:\
               time_in_seconds_clip_one_start-time_in_seconds_clip_one_end_time, time_in_seconds_clip_two_start-time_in_seconds_clip_two_end_time...\
               Do not write words beyond the format stated above. Choose {total_time//clip_time} clips out of the clips you have chosen."
    else:
        return f"Draw up a {total_time} second {content} using clips from {clips_from} that do not surpass {clip_time} seconds in the following format:\
               time_in_seconds_clip_one_start-time_in_seconds_clip_one_end_time, time_in_seconds_clip_two_start-time_in_seconds_clip_two_end_time...\
               Do not write words beyond the format stated above. Coordinate the clips with the following timestamped subtitles:{coordinating_subtitle}"

def sequence_from_stamped(stamped:str, folder_path:str, default_png_name:str, vid_length:float)->VideoClip:
    sequence_guide=[]
    for s in stamped.split(","):
        splitted = s.split("|")
        sequence_guide.append((splitted[0],splitted[1],splitted[3]))
    if not sequence_guide:
        raise ValueError("stamped is empty.")
    sequence = [ImageClip(folder_path+"\\"+default_png_name+".png",duration=sequence_guide[0][0])]
    for i in range(0,len(sequence_guide)-1):
        sequence.append(ImageClip(folder_path+"\\"+sequence_guide[i][2]+".png", duration=float(sequence_guide[i][1])))
        sequence.append(ImageClip(folder_path+"\\"+default_png_name+".png", duration=float(sequence_guide[i+1][0])-float(sequence_guide[i][0])))
    sequence.append(ImageClip(folder_path+"\\"+sequence_guide[len(sequence_guide)-1][2]+".png", duration=float(sequence_guide[len(sequence_guide)-1][1])))
    sequence.append(ImageClip(folder_path+"\\"+default_png_name+".png", duration=vid_length-float(sequence_guide[len(sequence_guide)-1][0])))
    return concatenate_videoclips(sequence)



