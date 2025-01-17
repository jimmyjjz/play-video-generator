from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import audio_manager,misc,scene_manager
import script_check,time
import tti_manager
from settings_manager import get_setting

#IGNORE YELLOW UNDERLINES
print("IF YOU HAVE NOT ALREADY, PROVIDE A BACKGROUND VIDEO AND NAME IT \"bgvid\"(must be mp4. mkv maybe supported soon).")
print("IF PC DOES NOT HAVE ENOUGH MEMORY RUN image_maker.py first to generate the images(if you are using script.txt)."
      "\nOtherwise, uncomment line 41 and 42 in main.py or line 145 or 146 in scene_manager.py(not both unless you want to generate each image twice)")
if get_setting("debug")==1:
    print("DEBUG 1\nNo speech or image files will be made.")
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
        print("Recommended to run script_check.py a few times before going further. Terminate the program if you want to do so.")
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

title=misc.script_to_title(script)
#if get_setting("debug")==0:
    #tti_manager.generate_images_ani_multi(tti_manager.grab_image_prompts(sectioned_sequence)+[title])#out of memory

scene_manager.setup_characters(misc.script_to_characters(script))
scenes=[scene_manager.create_title(title,get_setting("debug")==0,get_setting("create_speech_fast"))]

for e in sectioned_sequence:
    print("Creating scene ", e)
    scenes.append(scene_manager.create_scene(e))
    print("Created a scene", e)

fg=concatenate_videoclips(scenes).with_position("center")
bg_video=VideoFileClip("bgvid.mp4").without_audio()
mark=VideoFileClip("mark.mov",has_mask=True).with_position(("right",620))
final_product=CompositeVideoClip([bg_video.subclipped(0,fg.duration),fg,mark])
print("Making output video")
final_product.write_videofile("outputted_video.mp4", preset='ultrafast', fps=50, threads=14)

print("Process took:",time.time()-st,"seconds")
#12753.87342453003 seconds for 10 min 54 sec vid
#15577.287912368774 seconds
#Process finished with exit code -1073740791 (0xC0000409)
#process debug 1 took 7475.502396345139 seconds
#no pic generation 13min video took 10682.603286504745 seconds