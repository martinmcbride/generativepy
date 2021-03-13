# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT

import math


class Tween():
    '''
    Tweening class for scalar values

    Initial value is set on construction.

    wait() maintains the current value for the requested number of frames

    pad() similar to wait, but pads until the total length of the tween is the required size.

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

    def pad(self, final_length):
        self.check_count(final_length)
        required = final_length - len(self.frames)
        if required > 0:
            self.frames.extend([self.previous for i in range(required)])
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
        for i in range(count):
            factor = (i + 1) / count
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def ease(self, value, count, ease_function):
        self.check_value(value, self.previous)
        self.check_count(count)
        for i in range(count):
            factor = ease_function((i + 1) / count)
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def get(self, frame):
        if frame >= len(self.frames):
            return self.previous
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
            factor = (i + 1) / count
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def ease(self, value, count, ease_function):
        self.check_value(value, self.previous)
        self.check_count(count)
        for i in range(count):
            nextvalue = []
            factor = ease_function((i + 1) / count)
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
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


def ease_linear():
    return lambda x: x


def ease_in_harm():
    return lambda x: 1 + math.sin(math.pi * (x / 2 - 0.5))


def ease_out_harm():
    return lambda x: math.sin(math.pi * x / 2)


def ease_in_out_harm():
    return lambda x: 0.5 + 0.5 * math.sin(math.pi * (x - 0.5))


def ease_in_elastic():
    return lambda x: math.sin(2.25 * 2 * math.pi * (x)) * pow(2, 10 * (x - 1))


def ease_out_elastic():
    return lambda x: 1 - math.sin(2.25 * 2 * math.pi * (1 - x)) * pow(2, -10 * x)


def ease_in_out_elastic():
    def fn(x):
        if x < 0.5:
            f = 2 * x
            return 0.5 * (math.sin(2.25 * 2 * math.pi * f) * pow(2, 10 * (f - 1)))
        else:
            f = (2 * x - 1)
            return 0.5 * (1 - math.sin(2.25 * 2 * math.pi * (1 - f)) * pow(2, -10 * f)) + 0.5

    return fn


def ease_in_back():
    return lambda x: x * x * x - x * math.sin(x * math.pi)


def ease_out_back():
    def fn(x):
        f = (1 - x)
        return 1 - (f * f * f - f * math.sin(f * math.pi))

    return fn


def ease_in_out_back():
    def fn(x):
        if x < 0.5:
            f = 2 * x
            return 0.5 * (f * f * f - f * math.sin(f * math.pi))
        else:
            f = (1 - (2 * x - 1))
            return 0.5 * (1 - (f * f * f - f * math.sin(f * math.pi))) + 0.5

    return fn


# Basic bounce function used by the bounce easing functions.
# Don't use this function directly, use the ease_*_bounce functions instead.
def _bounce(x):
    if x < 4 / 11.0:
        return (121 * x * x) / 16.0
    elif x < 8 / 11.0:
        return (363 / 40.0 * x * x) - (99 / 10.0 * x) + 17 / 5.0
    elif x < 9 / 10.0:
        return (4356 / 361.0 * x * x) - (35442 / 1805.0 * x) + 16061 / 1805.0
    else:
        return (54 / 5.0 * x * x) - (513 / 25.0 * x) + 268 / 25.0


def ease_in_bounce():
    return lambda x: 1 - _bounce(1 - x)


def ease_out_bounce():
    return lambda x: _bounce(x)


def ease_in_out_bounce():
    def fn(x):
        if x < 0.5:
            return 0.5 * (1 - _bounce(1 - x * 2))
        else:
            return 0.5 * _bounce(x * 2 - 1) + 0.5

    return fn

