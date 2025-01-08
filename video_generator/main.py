import math

from moviepy import VideoFileClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import audio_manager, subtitle_manager, settings_manager, bg_video_manager, misc
import debug#possible thing that happens is that when importing the py file runs
from animateable import Animateable

#IGNORE YELLOW UNDERLINES
if settings_manager.get_setting("debug")==0:
    raise Exception("currently not set up")

if settings_manager.get_setting("debug")==1:
    print("DEBUG 1")
    with open("script.txt","r") as f:
        script=f.read()
    #
    audio_manager.setup_voices_with_script(script)
    audio_manager.dialogues_to_speech(misc.script_to_dialogues(script))
    #
    #audio_manager.create_speech(script)
    #text=subtitle_manager.speech_to_text("speech.wav", "medium")
elif settings_manager.get_setting("debug")==2:
    print("DEBUG 2")
    print(misc.generate_script_prompt("roblox story video", 1000))
    script = input("Input script output from GPT:")
    audio_manager.setup_voices_with_script(script)
    audio_manager.dialogues_to_speech(misc.script_to_dialogues(script))
else:
    pass

#+==================================================================================================================
#speech to text
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

#scene by scene
#attach intro after video done
#need title
print("End")
#when creating front end make it so the user can select the model_type