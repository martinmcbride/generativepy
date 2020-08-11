# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT

class Tween():
    '''
    Tweening class for scalar values

    Initial value is set on construction.

    wait() maintains the current value for the requested number of frames

    set() sets a new current values, and adds it for the requested number of frames (which can be zero)

    to() moves linearly from the current value to the supplied value. The first frame added will have the current value,
    the last frame added will have the new value, with values spaced evenly in between. The final value will be set as
    the new current value.

    You can use get(n) to get the nth frame, or alternatively you can use tween[n]. The built in len() function can be
    used to find the sequence length. Tween are iterable, so they can be used with for loops etc.
    '''
    
    def __init__(self, value=0):
        self.check_value(value, None)
        self.frames = []
        self.previous = value
        self.nextFrame = 0
        
    def wait(self, count):
        self.check_count(count)
        self.frames.extend([self.previous for i in range(count)])
        return self
        
    def set(self, value, count=0):
        self.check_value(value, self.previous)
        self.check_count(count)
        self.frames.extend([value for i in range(count)])
        self.previous = value
        return self
        
    def to(self, value, count):
        self.check_value(value, self.previous)
        self.check_count(count)
        self.frames.extend([self.previous + i*(value - self.previous)/(count-1) for i in range(count)])
        self.previous = value
        return self
        
    def get(self, frame):
        if frame >= len(self.frames):
            raise IndexError()
        return self.frames[frame]
    
    def __getitem__(self, key):
        return self.get(key)

    def __next__(self):
        if self.nextFrame >= len(self.frames):
            raise StopIteration()
        frame = self.get(self.nextFrame)
        self.nextFrame += 1
        return frame

    def __iter__(self):
        return self

    def check_value(self, value, previous):
        if (not isinstance(value, (int, float))) or isinstance(value, bool):
            raise ValueError('Numeric value required')

    def check_index(self, value):
        if not isinstance(value, int):
            raise ValueError('Integer value required')

    def check_count(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError('Non-negative integer value required')

    def __len__(self):
        return len(self.frames)
    
    
class TweenVector(Tween):
    '''
    Tweening class for vector quantities.

    Similar to Tween, but the values are vector quantities (ie tuples of lists), such as (x, y) positions or
    (r, g, b, a) colours.

    The vector quantities must have at least 1 element, but normally it will be 2 or more. Every value added must have
    the same length as the initial value, for example if you start with an (x, y) value, every new value must also
    have 2 dimansions.
    '''
    def __init__(self, value=(0, 0)):
        Tween.__init__(self, value)
        
    def to(self, value, count):
        self.check_value(value, self.previous)
        self.check_count(count)
        for i in range(count):
            nextvalue = []
            for a, b in zip(self.previous, value):
                nextvalue.append(a + i*(b - a)/(count-1))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def check_value(self, value, previous):
        try:
            if len(value) <= 0:
                raise ValueError('Vectors of rank 0 are not supported')
            if previous and len(value) != len(self.previous):
                raise ValueError('All values must be vectors of equal rank')
        except:
            ValueError('Sequence value required')
