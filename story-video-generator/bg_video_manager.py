from moviepy import concatenate_videoclips
from moviepy.video.io import VideoFileClip
from openai import OpenAI

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
#print(generate_prompt(30,"review on World Trigger","episode one",5))