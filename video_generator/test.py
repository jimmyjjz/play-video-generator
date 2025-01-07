#from moviepy import VideoFileClip, CompositeVideoClip, ImageClip
#from moviepy.video.io.bindings import PIL_to_npimage
import moviepy
from moviepy import *
clip=VideoFileClip("orange_juice_video.mp4").subclipped(20,25)
thing=ImageClip("tti.gif",transparent=True,duration=5)
#thing=VideoFileClip("tti.gif",has_mask=True)
#thing=VideoClip(VideoFileClip("tti.gif",has_mask=True))
final_product = CompositeVideoClip([clip,thing])
final_product.write_videofile(
    "output.mov",
    codec="dnxhd",
    ffmpeg_params=[
        "-b:v", "36M",  #36 Mbps
        "-pix_fmt", "yuv422p",
    ]
)