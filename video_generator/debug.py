from moviepy import AudioFileClip
import misc, subtitle_manager, audio_manager, math
import settings_manager

script_prompt, generate_speech_wav, generate_text, selection_prompt, status_prompt=False, False, False, False, False
#make sure all false when running debug 2 in main
test_text=[(0.0, 0.32, ' Ever'), (0.32, 0.66, ' wondered'), (0.66, 0.88, ' how'), (0.88, 1.14, ' your'), (1.14, 1.52, ' favorite'), (1.52, 1.98, ' orange'), (1.98, 2.18, ' juice'), (2.18, 2.44, ' is'), (2.44, 2.7, ' made?'), (3.74, 3.9, ' Let'), (3.9, 4.1, ' us'), (4.1, 4.28, ' break'), (4.28, 4.54, ' it'), (4.54, 4.88, ' down.')]

print("WHEN GETTING OUTPUT FROM GPT DO NOT CLICK THE COPY BUTTON. JUST SELECT AND COPY.")
if script_prompt:
    with open("script.txt","w") as f:
        print(misc.generate_script_prompt("The Infographics Show", 20, "how orange juice is made"))
        f.write(input("Input script output from GPT:"))

if generate_speech_wav:
    with open("script.txt", "r") as f:
        audio_manager.create_speech(f.read())

if generate_text:
    text = subtitle_manager.speech_to_text("speech.wav", "medium")
    print(text)#test_text=<insert the output>

if selection_prompt:
    with open("selection.txt","w") as f:
        print(misc.generate_selection_prompt("presentation on how orange juice is made", "the given video", 1, math.ceil(AudioFileClip("speech.wav").duration)))#make round up to a certain multiple func. Later cut down video.
        f.write(input("Input selection output from GPT:"))

if status_prompt:
    with open("statuses.txt","w") as f:
        print(misc.generate_status_prompt("presenter", test_text))
        f.write(input("Input statuses output from GPT:"))