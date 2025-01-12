from functools import partial
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
import settings_manager

class Animateable(object):
    # Only VideoClip and its children are supported
    # rotation is currently is "boxed" and transparent pixels are turned black

    def animate(self, t, op:int):#maybe raise exception if not established
        try:
            while self.timed_modifications[op][self.current_index[op]+1][0]<t:
                self.current_index[op]+=1
        except IndexError:pass
        if op=="position":
            if self.timed_modifications[op][self.current_index[op]][4]:
                tmp=self.most_recent_pos[0]+self.timed_modifications[op][self.current_index[op]][2],self.most_recent_pos[1]+self.timed_modifications[op][self.current_index[op]][3]
                self.most_recent_pos = tmp
                return tmp
            a, b=self.timed_modifications[op][self.current_index[op]][2],self.timed_modifications[op][self.current_index[op]][3]
            if a == -99:
                a = self.most_recent_pos[0]
            if b == -99:
                b = self.most_recent_pos[1]
            self.most_recent_pos = a, b
            return a, b
        if op=="scale":
            if self.timed_modifications[op][self.current_index[op]][4]:
                tmp=self.most_recent_size[0]+self.timed_modifications[op][self.current_index[op]][2],self.most_recent_size[1]+self.timed_modifications[op][self.current_index[op]][3]
                self.most_recent_size = tmp
                return tmp
            a, b = self.timed_modifications[op][self.current_index[op]][2],self.timed_modifications[op][self.current_index[op]][3]
            if a == -99:
                a = self.most_recent_size[0]
            if b == -99:
                b = self.most_recent_size[1]
            self.most_recent_size = a, b
            return a, b
        if op=="rotation":
            if self.timed_modifications[op][self.current_index[op]][3]:
                self.most_recent_rotation+=self.timed_modifications[op][self.current_index[op]][2]
                return self.most_recent_rotation+self.timed_modifications[op][self.current_index[op]][2]
            if self.timed_modifications[op][self.current_index[op]][2]==-99:
                return self.most_recent_rotation
            self.most_recent_rotation = self.timed_modifications[op][self.current_index[op]][2]
            return self.timed_modifications[op][self.current_index[op]][2]

    def __init__(self, clip, starting_h:float, starting_v:float, starting_rotation:float=0, stamped_move_distance:float=300):
        self.clip=clip
        self.timed_modifications = {"position":[],"scale":[],"rotation":[]}
        self.current_index={"position":-1,"scale":-1,"rotation":-1}
        self.starting_h=starting_h
        self.starting_v=starting_v
        self.most_recent_pos=(starting_h,starting_v)
        self.most_recent_size=(clip.w,clip.h)
        self.most_recent_rotation=starting_rotation
        self.stamped_move_distance=stamped_move_distance

    def queue_move(self, start_time: float, duration: float, x: float, y: float, relative:bool) -> None:
        self.timed_modifications["position"].append((start_time, duration, x, y, relative))

    def queue_scale(self, start_time: float, duration: float, width: float, height: float, relative:bool) -> None:
        self.timed_modifications["scale"].append((start_time, duration, width, height, relative))

    def queue_rotation(self, start_time: float, duration: float, degrees: float, relative:bool) -> None:
        self.timed_modifications["rotation"].append((start_time, duration, degrees, relative))

    def queue_smooth_move(self, start_time: float, duration: float, x1: float, y1: float, x2: float, y2: float, fps: int = 300) -> None:
        #Note: when fps gets too high some queued_moves will get skipped
        current_time, x, y = start_time, x1, y1
        while current_time + 1 / fps <= start_time + duration:
            x += (x2 - x1) / (fps * duration)
            y += (y2 - y1) / (fps * duration)
            current_time += 1 / fps
            self.queue_move(current_time, 1 / fps, x, y, False)

    def queue_smooth_move_relative(self, start_time: float, duration: float, x: float, y: float, fps: int = 300) -> None:
        #Note: when fps gets too high some queued_moves will get skipped
        current_time = start_time
        while current_time + 1 / fps <= start_time + duration:
            current_time += 1 / fps
            self.queue_move(current_time, 1 / fps, x / (fps * duration), y / (fps * duration), True)

    def add_with_stamped_actions(self, stamped:str)->None:
        #if stamped too close together then stuff can get skipped
        for s in stamped.split(","):
            splitted=s.split("|")
            match splitted[2]:
                case "move-right":
                    self.queue_smooth_move_relative(float(splitted[0]),float(splitted[1]), self.stamped_move_distance, 0)
                case "move-down":
                    self.queue_smooth_move_relative(float(splitted[0]),float(splitted[1]), 0, -self.stamped_move_distance)
                case "move-left":
                    self.queue_smooth_move_relative(float(splitted[0]),float(splitted[1]), -self.stamped_move_distance, 0)
                #case "move-remain":
                #    self.queue_smooth_move_relative(float(splitted[0]),1, 0, 0)

    def establish(self) -> None:
        for k in self.timed_modifications.keys():
            self.timed_modifications[k].sort()
        for i in range(len(self.timed_modifications["rotation"])-1,-1,-1):
            self.timed_modifications["rotation"].insert(i + 1, (self.timed_modifications["rotation"][i][0] + self.timed_modifications["rotation"][i][1], -1, -99, False))
        for i in range(len(self.timed_modifications["scale"]) - 1, -1, -1):
            self.timed_modifications["scale"].insert(i+1, (self.timed_modifications["scale"][i][0]+self.timed_modifications["scale"][i][1], -1, -99, -99, False))
        for i in range(len(self.timed_modifications["position"]) - 1, -1, -1):
            self.timed_modifications["position"].insert(i+1, (self.timed_modifications["position"][i][0]+self.timed_modifications["position"][i][1], -1, -99, -99, False))
        self.timed_modifications["rotation"].insert(0,(0, -1, -99, False))
        self.timed_modifications["scale"].insert(0,(0, -1, -99, -99, False))
        self.timed_modifications["position"].insert(0,(0, -1, -99, -99, False))
        self.clip = self.clip.with_position(partial(self.animate, op="position"))
        self.clip = self.clip.resized(partial(self.animate, op="scale"))
        self.clip = self.clip.rotated(partial(self.animate, op="rotation"))

# ==================================================TESTING==================================================
'''
full_video = VideoFileClip("test_video.mkv")
vid=full_video.subclipped(10,15)
#ic=[ImageClip("krimdus_emotion_package\krimdus_neutral.png", duration=vid.duration)]
#video_clip = concatenate_videoclips(ic)
#print(type(video_clip))
krimdus=Animateable(ImageClip("krimdus_emotion_package\krimdus_neutral.png", duration=vid.duration),100,100)
krimdus.queue_smooth_move(1,4,200,200,360,360, False)
#krimdus.queue_move(1,1,2,2)
#krimdus.queue_move(2,1,50,50)
#krimdus.queue_scale(3,1,10,10)
#krimdus.queue_rotation(4,1,45)
krimdus.establish()
#background = ColorClip(size=(krimdus.clip.w, krimdus.clip.h), color=(255, 255, 255),duration=vid.duration)
#final_product = CompositeVideoClip([vid,background, krimdus.clip])
final_product=CompositeVideoClip([vid, krimdus.clip])
final_product.write_videofile("outputted_test_video.mp4", preset='ultrafast', fps = 60)

#changing opacity
'''