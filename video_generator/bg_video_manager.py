from moviepy import concatenate_videoclips
from moviepy.video.io import VideoFileClip
from openai import OpenAI

def generate_prompt(total_time:int, content:str, clips_from:str, clip_time:int, coordinating_subtitle:list="")->str:
    #make sure total_time%clip_time==0(at least if not using coordinating_subtitle
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

def deliver_prompt(prompt:str, api_key:str, model:str="gpt-4o-mini"):
    client = OpenAI(api_key=api_key)
    return client.chat.completions.create(messages=[{"role": "user","content": prompt}],model=model)

def output_to_timestamps(output:str)->list:
    # example output: "0-5, 10-15, 20-25, 60-65, 130-135, 225-230"
    intervals=output.split(", ")
    timestamps=[]
    for v in intervals:
        timestamps.append(v.split("-"))
    return timestamps

def generate_bg_video(full_clips_source:VideoFileClip, timestamps:list)->VideoFileClip:
    clips=[]
    for ts in timestamps:
        clips.append(full_clips_source.subclipped(ts[0],ts[1]))
    return concatenate_videoclips(clips)

# ==================================================TESTING==================================================
print(generate_prompt(30,"review on World Trigger","episode one",5))