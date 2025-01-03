from moviepy import *
from functools import partial

class Animateable(object):
    # Only VideoClip and its children are supported
    # rotation is currently is "boxed" and transparent pixels are turned black

    def animate(self, t, op:int):
        try:
            while self.timed_modifications[op][self.current_index[op]+1][0]<t:
                self.current_index[op]+=1
        except IndexError:pass
        if op=="rotation":
            return self.timed_modifications[op][self.current_index[op]][2]
        if op=="position" or op=="scale":
            #print(t,self.timed_modifications[op][self.current_index[op]][2],self.timed_modifications[op][self.current_index[op]][3])
            return self.timed_modifications[op][self.current_index[op]][2],self.timed_modifications[op][self.current_index[op]][3]

    def __init__(self, clip):
        self.clip=clip
        self.timed_modifications = {"position":[],"scale":[],"rotation":[]}
        self.current_index={"position":-1,"scale":-1,"rotation":-1}

    def queue_move(self, start_time: float, duration: float, x: float, y: float) -> None:
        self.timed_modifications["position"].append((start_time, duration, x, y))

    def queue_scale(self, start_time: float, duration: float, width: float, height: float) -> None:
        self.timed_modifications["scale"].append((start_time, duration, width, height))

    def queue_rotation(self, start_time: float, duration: float, degrees: float) -> None:
        self.timed_modifications["rotation"].append((start_time, duration, degrees))

    def smooth_move(self, start_time: float, duration: float, x1: float, y1: float, x2: float, y2: float, fps: int = 300) -> None:
        current_time, x, y = start_time, x1, y1
        while current_time + duration / fps <= start_time + duration:
            x += (x2 - x1) / (fps * duration)
            y += (y2 - y1) / (fps * duration)
            current_time += duration / fps
            self.queue_move(current_time, duration / fps, x, y)

    def establish(self) -> None:
        for k in self.timed_modifications.keys():
            self.timed_modifications[k].sort()
        for i in range(len(self.timed_modifications["rotation"])-1,-1,-1):
            self.timed_modifications["rotation"].insert(i + 1, (self.timed_modifications["rotation"][i][0] + self.timed_modifications["rotation"][i][1], -1, 0))
        for i in range(len(self.timed_modifications["scale"]) - 1, -1, -1):
            self.timed_modifications["scale"].insert(i+1, (self.timed_modifications["scale"][i][0]+self.timed_modifications["scale"][i][1], -1, self.clip.size[0], self.clip.size[1]))
            #
        for i in range(len(self.timed_modifications["position"]) - 1, -1, -1):
            self.timed_modifications["position"].insert(i+1, (self.timed_modifications["position"][i][0]+self.timed_modifications["position"][i][1], -1, 0, 0))
        self.timed_modifications["rotation"].insert(0,(0, -1, 0))
        self.timed_modifications["scale"].insert(0,(0, -1, self.clip.size[0], self.clip.size[1]))
        #
        self.timed_modifications["position"].insert(0,(0, -1, 0, 0))
        self.clip = self.clip.with_position(partial(self.animate, op="position"))
        self.clip = self.clip.resized(partial(self.animate, op="scale"))
        self.clip = self.clip.rotated(partial(self.animate, op="rotation"))

# ==================================================TESTING==================================================
full_video = VideoFileClip("test_video.mkv")
vid=full_video.subclipped(10,15)
ic=[ImageClip("krimdus_emotion_package\krimdus_neutral.png", duration=vid.duration)]
video_clip = concatenate_videoclips(ic)
print(type(video_clip))
krimdus=Animateable(video_clip)
krimdus.smooth_move(1,3,0,0,300,300)
#krimdus.queue_move(1,1,2,2)
#krimdus.queue_move(2,1,50,50)
#krimdus.queue_scale(3,1,10,10)
#krimdus.queue_rotation(4,1,45)
krimdus.establish()
background = ColorClip(size=(krimdus.clip.w, krimdus.clip.h), color=(255, 255, 255),duration=vid.duration)
final_product = CompositeVideoClip([vid,background, krimdus.clip])
#final_product=CompositeVideoClip([vid, krimdus.clip])
final_product.write_videofile("outputted_test_video.mp4", preset='ultrafast', fps = 60)