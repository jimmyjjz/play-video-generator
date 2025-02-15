from moviepy import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import audio_manager,misc,scene_manager,script_check,time,gc,torch
from settings_manager import get_setting
if __name__ == "__main__":
    #IGNORE YELLOW UNDERLINES
    print("IF YOU HAVE NOT ALREADY, PROVIDE A BACKGROUND VIDEO AND NAME IT \"bgvid#\"(must be mp4).")
    print("RUN image_maker.py first. Set up script(#).txt(s) before running, can check with script_check.py.")
    if get_setting("debug")==1:
        print("DEBUG 1\nNo speech or image files will be made.")
        with open("script.txt","r") as f:
            script=f.read()
    else:
        inp=input("(1)Generate Video\n(2)Generate prompt\n\nEnter number:")
        if inp=="1":
            print("Recommended to run script_check.py a few times before going further. Terminate the program if you want to do so.")
        elif inp=="2":
            print(misc.generate_script_prompt(input("Enter content:"), int(input("Enter min word count:"))))
            exit("Prompt given. Program terminated.")
        else:
            raise ValueError("INVALID INPUT")

    for k in range(1,get_setting("production_count")+1):# 1. "script" 2+ "script#"
        print(f"script {k}")
        if k==1:
            with open("script.txt", "r") as f:
                script = f.read()
                script_check.check_script(script)
        elif k>1:
            with open("script"+str(k)+".txt", "r") as f:
                script = f.read()
                script_check.check_script(script)
        else:
            raise ValueError("INVALID product_count setting. Might because it is 0 or a negative number.")

        st=time.time()

        audio_manager.setup_voices_with_script(script)
        sectioned_sequence=misc.section_sequence(misc.script_to_sequence(script,get_setting("produce_dialogue"),get_setting("create_speech_fast")))#get_setting("debug")==0

        title=misc.script_to_title(script)

        scene_manager.setup_characters(misc.script_to_characters(script))
        if get_setting("title_portion"):
            scenes=[scene_manager.create_title(title,get_setting("debug")==0,get_setting("create_speech_fast"))]
        else:
            scenes = []

        misc.clear_processes()

        if get_setting("split_and_merge") == 2:#2 produce each video individually and merge them at the end. Takes the longest.
            bg_video = VideoFileClip(f"bgvid{k}.mp4").without_audio()
            mark = VideoFileClip("mark.mov", has_mask=True).with_position(("right", 620))
            j,accu=0,0
            for e in sectioned_sequence:
                print("Creating scene ", e)
                tmp=scene_manager.create_scene(e)
                gc.collect()
                tmp=CompositeVideoClip([bg_video.subclipped(accu,accu+tmp.duration),tmp])
                accu+=tmp.duration
                tmp.write_videofile("temp_vids\\output_"+str(j)+".mp4", preset='ultrafast', fps=50, threads=18)
                print("Created a scene", e)

                tmp.close()
                print("Deleting unneeded elements")
                del tmp
                print("Executing garbage collection")
                gc.collect()
                with torch.no_grad():
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
                j+=1
            scenes=[]
            for i in range(j):
                scenes.append(VideoFileClip("temp_vids\\output_"+str(i)+".mp4"))
            final_product = CompositeVideoClip([concatenate_videoclips(scenes),mark])

        elif get_setting("split_and_merge")==1:#1 produce 3 thirds and merge them at the end. Takes the second longest.
            if len(sectioned_sequence)<3:
                raise ValueError("Too less scenes to split and merge")

            bg_video = VideoFileClip(f"bgvid{k}.mp4").without_audio()
            mark = VideoFileClip("mark.mov", has_mask=True).with_position(("right", 620))
            print("First half")
            j=0#(2*len(sectioned_sequence)//3)-len(sectioned_sequence)//3
            for i in range(len(sectioned_sequence)//3):
                print("Creating scene ", sectioned_sequence[j])
                scenes.append(scene_manager.create_scene(sectioned_sequence[j]))
                gc.collect()
                print("Created a scene", sectioned_sequence[j])
                j+=1
            fg = concatenate_videoclips(scenes).with_position("center")
            first_half=CompositeVideoClip([bg_video.subclipped(0,fg.duration),fg,mark])
            first_half.write_videofile("temp_vids\\first_half.mp4", preset='ultrafast', fps=50, threads=18)
            fg_duration=fg.duration

            first_half.close()
            print("Deleting unneeded elements")

            for z in range(len(scenes)):
                scenes[z]=None
            fg,first_half=None,None

            del fg,scenes,first_half
            misc.clear_processes()

            print("Second half")
            scenes=[]
            for i in range((2*len(sectioned_sequence)//3)-len(sectioned_sequence)//3):
                print("Creating scene ", sectioned_sequence[j])
                scenes.append(scene_manager.create_scene(sectioned_sequence[j]))
                gc.collect()
                print("Created a scene", sectioned_sequence[j])
                j+=1
            fg2 = concatenate_videoclips(scenes).with_position("center")
            second_half = CompositeVideoClip([bg_video.subclipped(fg_duration, fg_duration+fg2.duration), fg2])
            second_half.write_videofile("temp_vids\\second_half.mp4", preset='ultrafast', fps=50, threads=18)
            fg2_duration=fg2.duration

            second_half.close()
            print("Deleting unneeded elements")

            for z in range(len(scenes)):
                scenes[z]=None
            fg2, second_half = None, None

            del fg2,scenes,second_half
            misc.clear_processes()

            #fg_duration,fg2_duration=VideoFileClip("temp_vids\\first_half.mp4").duration,VideoFileClip("temp_vids\\second_half.mp4").duration
            #gc.collect()

            print("Third half")
            scenes = []
            for i in range(len(sectioned_sequence)-(2 * len(sectioned_sequence) // 3)):
                print("Creating scene ", sectioned_sequence[j])
                scenes.append(scene_manager.create_scene(sectioned_sequence[j]))
                gc.collect()
                print("Created a scene", sectioned_sequence[j])
                j += 1
            fg3 = concatenate_videoclips(scenes).with_position("center")
            third_half = CompositeVideoClip([bg_video.subclipped(fg_duration+fg2_duration, fg_duration+fg2_duration+fg3.duration), fg3])
            third_half.write_videofile("temp_vids\\third_half.mp4", preset='ultrafast', fps=50, threads=18)

            third_half.close()
            print("Deleting unneeded elements")

            for z in range(len(scenes)):
                scenes[z]=None
            fg3, third_half = None, None

            del fg3,scenes,third_half
            misc.clear_processes()

            print("Making output video")
            final_product=concatenate_videoclips([VideoFileClip("temp_vids\\first_half.mp4"),VideoFileClip("temp_vids\\second_half.mp4"),VideoFileClip("temp_vids\\third_half.mp4")])
        else:#Produces all in one go. The fastest.
            for e in sectioned_sequence:
                print("Creating scene ", e)
                scenes.append(scene_manager.create_scene(e))
                gc.collect()
                print("Created a scene", e)

            fg = concatenate_videoclips(scenes).with_position("center")
            bg_video = VideoFileClip(f"bgvid{k}.mp4").without_audio()
            mark = VideoFileClip("mark.mov", has_mask=True).with_position(("right", 620))
            final_product = CompositeVideoClip([bg_video.subclipped(0, fg.duration), fg, mark])

        print("Making output video")
        final_product.write_videofile("outputted_video"+str(k)+".mp4", preset='ultrafast', fps=50, threads=18)
        print("Process took:",time.time()-st,"seconds")
        final_product.close()
        final_product=None
        del final_product
        misc.clear_processes()