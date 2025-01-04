import audio_manager, subtitle_manager, settings_manager, bg_video_manager, misc

if not settings_manager.get_setting("debug"):
    raise Exception("currently not set up")

if settings_manager.get_setting("debug"):
    print(misc.generate_script_prompt("SsethTzeentach", "World Trigger", 7))
    script = input("Input output from GPT:")
    #
    audio_manager.create_speech(script, preset="ultra-fast")
    text=subtitle_manager.speech_to_text("speech", "medium")
else:
    pass

sectioned_text=subtitle_manager.section_words(text)#ignore yellow underline

if settings_manager.get_setting("debug"):
    misc.generate_selection_prompt(30,"review on World Trigger","episode one",5)
else:
    pass

bg_video_manager.output_to_timestamps(input("Enter GPT output:"))

#when creating front end make it so the user can select the model_type
print("End")