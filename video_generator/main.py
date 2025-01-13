from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import audio_manager,misc,scene_manager
import script_check,time
from settings_manager import get_setting

#IGNORE YELLOW UNDERLINES
print("IF YOU HAVE NOT ALREADY. PROVIDE A BACKGROUND VIDEO AND NAME IT \"bgvid\"(must be mp4. mkv maybe supported soon).")
if get_setting("debug")==1:
    print("DEBUG 1\nNo speech files will be made.")
    with open("script.txt","r") as f:
        script=f.read()
elif get_setting("debug")==2:
    print("DEBUG 2\n"+misc.generate_script_prompt("roblox story video", 1000))
    script = input("Input script output from GPT:")
else:
    print("THE FOLLOWING MAY POPUP TWICE WHEN THE SETTING create_speech_fast IS TRUE. IGNORE THE SECOND POPUP.")
    inp=input("1.Read (I)nput\n2.Read (F)ile\n3.(G)enerate prompt\nFile assumes that you have already added the GPT output into script.txt.\nEnter capital letter:")
    if inp=="I":
        print("NOTE: DOES NOT HAVE CHECK. PROCEED WITH THE")
        print(misc.generate_script_prompt(input("Enter content:"), int(input("Enter min word count:"))))
        script = input("Input script output from GPT:")
    elif inp=="F":
        with open("script.txt", "r") as f:
            script = f.read()
            script_check.check_script(script)
    elif inp=="G":
        print(misc.generate_script_prompt(input("Enter content:"), int(input("Enter min word count:"))))
        exit("Prompt given. Program terminated.")
    else:
        raise ValueError("INVALID INPUT")

st=time.time()

audio_manager.setup_voices_with_script(script)
sectioned_sequence=misc.section_sequence(misc.script_to_sequence(script,get_setting("debug")==0,get_setting("create_speech_fast")))
scene_manager.setup_characters(misc.script_to_characters(script))
scenes=[scene_manager.create_title(misc.script_to_title(script),get_setting("debug")==0,get_setting("create_speech_fast"))]

for e in sectioned_sequence:
    scenes.append(scene_manager.create_scene(e))

fg=concatenate_videoclips(scenes).with_position("center")
bg_video=VideoFileClip("bgvid.mp4").without_audio()
final_product=CompositeVideoClip([bg_video.subclipped(0,fg.duration),fg])
final_product.write_videofile("outputted_test_video.mp4", preset='ultrafast', fps=50)

print("Process took:",time.time()-st,"seconds")