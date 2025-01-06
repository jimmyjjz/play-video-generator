import math

from moviepy import VideoFileClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import audio_manager, subtitle_manager, settings_manager, bg_video_manager, misc
import debug#possible thing that happens is that when importing the py file runs
from animateable import Animateable

#IGNORE YELLOW UNDERLINES
if not settings_manager.get_setting("debug"):
    raise Exception("currently not set up")

if settings_manager.get_setting("debug")==1:
    print("DEBUG 1")
    print(misc.generate_script_prompt("The Infographics Show", 20,"how orange juice is made"))
    script = input("Input script output from GPT:")
    audio_manager.create_speech(script)
    text=subtitle_manager.speech_to_text("speech.wav", "medium")
    print(misc.generate_selection_prompt("presentation on how orange juice is made", "the given video", 1, math.ceil(AudioFileClip("speech.wav").duration)))#make round up to a certain multiple func. Later cut down video.
    selection=input("Input selection output from GPT:")
    print(misc.generate_status_prompt("presenter", text))
    statuses=input("Input statuses output from GPT:")

elif settings_manager.get_setting("debug")==2:
    print("DEBUG 2")
    with open("script.txt","r") as f:
        script=f.read()
    with open("statuses.txt","r") as f:
        statuses=f.read()
    with open("selection.txt","r") as f:
        selection=f.read()
    text = debug.test_text
else:
    pass

sectioned_text=subtitle_manager.section_words(text)
bg_video_manager.output_to_timestamps(selection)

if settings_manager.get_setting("debug"):
    krimdus = Animateable(misc.sequence_from_stamped(statuses,"state_package"),
                          settings_manager.get_setting("horizontal")/2-80,settings_manager.get_setting("vertical")/2+200)#ignore yellow underline
    krimdus.add_with_stamped_actions(statuses)
    krimdus.establish()
    full_video = VideoFileClip("orange_juice_video.mp4")
else:
    pass

subtitle=subtitle_manager.sectioned_subtitles_to_subtitles(subtitle_manager.section_words(text))
bg_video=bg_video_manager.generate_bg_video(full_video,bg_video_manager.output_to_timestamps(selection)).without_audio()
bg_video.audio = CompositeAudioClip([AudioFileClip("speech.wav")])
final_product = CompositeVideoClip([bg_video, krimdus.clip, subtitle])
final_product.write_videofile("outputted_test_video.mp4", preset='ultrafast', fps=60)

print("End")
#when creating front end make it so the user can select the model_type