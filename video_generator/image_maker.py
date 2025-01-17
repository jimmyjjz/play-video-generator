import misc
import tti_manager

print("RECOMMENDED TO RUN script_check.py before this")
with open("script.txt","r") as f:
    script=f.read()

sectioned_sequence=misc.section_sequence(misc.script_to_sequence(script,False))
img_prompts=tti_manager.grab_image_prompts(sectioned_sequence)+[misc.script_to_title(script)]
for p in img_prompts:
    tti_manager.generate_images_ani_single(p)#if i go mult my current pc will run out of memory
    print("generated",p)