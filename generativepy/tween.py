# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT

class Tween():
    
    def __init__(self, value=0):
        self.frames = []
        self.previous = value
        self.nextFrame = 0
        
    def wait(self, frames):
        self.frames.extend([self.previous for i in range(frames)])
        return self
        
    def set(self, value, frames):
        self.frames.extend([value for i in range(frames)])
        self.previous = value
        return self
        
    def to(self, value, frames):
        self.frames.extend([self.previous + i*(value - self.previous)/frames for i in range(frames)])
        self.previous = value
        return self
        
    def get(self, frame):
        return self.frames[frame] if frame < len(self.frames) else self.previous
    
    def __getitem__(self, key):
        return self.get(key)

    def __next__(self):
        frame = self.get(self.nextFrame)
        self.nextFrame += 1
        return frame
    
    
class TweenVector(Tween):
    def __init__(self, value=(0, 0)):
        Tween.__init__(self, value)
        
    def to(self, value, frames):
        nextvalue=value
        for i in range(frames):
            nextvalue = []
            for a, b in zip(self.previous, value):
                nextvalue.append(a + i*(b - a)/frames)
            self.frames.append(nextvalue)
        self.previous = value
        return self
