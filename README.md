# Story Video Generator
A story video generator that is sizably powered by AI.

Uses a variety of different AI models to generate individual components of a play:
- The script(GPT4)
- Text to speech(Tortoise)
- Text to image(stable-diffusion)
- Speech to text(whisper)

which is compiled into a video using Moviepy.

Now utilizes PyTorch(use to utilize Tensorflow). 

Needed to run:
- tortoise_tts 3.0.0
- moviepy 2.1.0
- pytorch 2.5.1
- diffuser 0.32.1
- faster_whisper 1.1.0

and their dependencies
- adequately sized mp4(s) named bgvid# #=1,2,3...
- enough vram(~4-5gb for 15min video)

Customizability:
- animations and motion can be animated using Animateable
- settings for max vram usage
- switching ai models for different tasks
- visual images can be changed
- video settings

...



Videos made by this generator can be found on:
https://www.youtube.com/@Robloxuha
