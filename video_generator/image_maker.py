import misc,settings_manager,tti_manager

if __name__ == "__main__":
    print("RECOMMENDED TO RUN script_check.py before this")
    for i in range(1,settings_manager.get_setting("production_count")+1):
        if i==1:
            with open("script.txt","r") as f:
                script=f.read()
        elif i>1:
            with open(f"script{i}.txt","r") as f:
                script=f.read()
        else:
            raise ValueError

        sectioned_sequence=misc.section_sequence(misc.script_to_sequence(script,False))
        img_prompts=tti_manager.grab_image_prompts(sectioned_sequence)+[misc.script_to_title(script)]
        for p in img_prompts:
            tti_manager.generate_images_ani_single(p)#if i go mult my current pc will run out of memory
            print("generated",p)