# Author:  Martin McBride
# Created: 2019-01-25
# Copyright (C) 2018, Martin McBride
# License: MIT
import collections
import math

"""
The tween module provides tweening functionality to help with animation,
"""

_FRAME_RATE = 1

def set_frame_rate(rate):
    """
    Sets the tween frame rate

    Args:
        rate: number - Number of frames per second
    """
    global _FRAME_RATE
    if not isinstance(rate, (int, float)):
        raise ValueError('Frame rate must be a numeric value')
    if rate < 1:
        raise ValueError('Frame rate must be one or greater')
    _FRAME_RATE = rate

class Tween():
    '''
    Tweening class for scalar values.

    Tween durations are measured in seconds, but the tween array created measures time in frame. This means that event times
    can be scheduled in seconds, but the array values can be indexed using the frame count.

    Initial value is set on construction.

    wait() maintains the current value up to requested time.

    set() sets a new current value.

    to() moves linearly from the current value to the supplied value. The first frame added will have the current value,
    the last frame added will have the new value, with values spaced evenly in between. The final value will be set as
    the new current value.

    You can use get(n) to get the nth frame, or alternatively you can use tween[n]. The built in len() function can be
    used to find the sequence length. Tween are iterable, so they can be used with for loops etc.
    '''

    def __init__(self, value=0):
        """
        Args:
            value: number - The initial value, defaults to 0.

        Returns:
            self
        """
        self.check_value(value, None)
        self.frames = []
        self.previous = value
        self.nextFrame = 0

    def wait(self, time):
        """
        Wait, maintaining the current value, until the specified absolute time.

        Args:
            time: number - Absolute time to wait

        Returns:
            self
        """
        count = self.check_and_convert_time(time, len(self.frames))
        self.frames.extend([self.previous for i in range(count)])
        return self

    def wait_d(self, time):
        """
        Wait, maintaining the current value, for the specified time period

        Args:
            time: number - Relative time to wait

        Returns:
            self
        """
        count = self.check_and_convert_time_d(time)
        self.frames.extend([self.previous for i in range(count)])
        return self

    def set(self, value):
        """
        Set the value

        Args:
            value: number - New tween value

        Returns:
            self
        """
        self.check_value(value, self.previous)
        self.previous = value
        return self

    def to(self, value, time):
        """
        Make the tween value move from its current value to a new value, finishing at the specified time.
        The transition is linear.

        Args:
            value: number - New tween value.
            time: number - Absolute time to reach final value.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time(time, len(self.frames))
        for i in range(count):
            factor = (i + 1) / count
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def to_d(self, value, time):
        """
        Make the tween value move from its current value to a new value, finishing after the specified time period.
        The transition is linear.

        Args:
            value: number - New tween value.
            time: number - Relative time period to reach final value.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time_d(time)
        for i in range(count):
            factor = (i + 1) / count
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def ease(self, value, time, ease_function):
        """
        Make the tween value move from its current value to a new value, finishing at the specified time.
        The transition is controlled by the easing function.

        Args:
            value: number - New tween value.
            time: number - Absolute time to reach final value.
            ease_function: function - Easing function. Thus accepts a value that varies between 0 and 1.0.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time(time, len(self.frames))
        for i in range(count):
            factor = ease_function((i + 1) / count)
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def ease_d(self, value, time, ease_function):
        """
        Make the tween value move from its current value to a new value, finishing after the specified time period.
        The transition is controlled by the easing function.

        Args:
            value: number - New tween value.
            time: number - Absolute time to reach final value.
            ease_function: function - Easing function. Thus accepts a value that varies between 0 and 1.0.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time_d(time)
        for i in range(count):
            factor = ease_function((i + 1) / count)
            self.frames.append(self.previous + factor * (value - self.previous))
        self.previous = value
        return self

    def get(self, frame):
        """
        Get the tween value at the specified frame.

        Returns:
            The tween value for the frame. If a frame is requested that is beyond the last frame available, return the value of the final frame.
        """
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
        if not isinstance(value, (int, float)):
            raise ValueError('Numeric value required')

    def check_and_convert_time(self, time, current):
        if not isinstance(time, (int, float)):
            raise ValueError('time must be a number')
        count = int(_FRAME_RATE*time)
        if count < current:
            raise ValueError('New time must not be less than previous time')
        return count - current

    def check_and_convert_time_d(self, time):
        if not isinstance(time, (int, float)):
            raise ValueError('time must be a number')
        if time < 0:
            raise ValueError('time must not be negative')
        return int(_FRAME_RATE*time)

    def __len__(self):
        return len(self.frames)


class TweenVector(Tween):
    '''
    Tweening class for vector quantities.

    Similar to Tween, but the values are vector quantities (ie tuples of lists), such as (x, y) positions or
    (r, g, b, a) colours.

    The vector quantities must have at least 1 element, but normally it will be 2 or more. Every value added must have
    the same length as the initial value, for example if you start with an (x, y) value, every new value must also
    have 2 dimensions.
    '''

    def __init__(self, value=(0, 0)):
        self.check_value(value, None)
        Tween.__init__(self, value)

    def to(self, value, time):
        """
        Make the tween value move from its current value to a new value, finishing at the specified time.
        The transition is linear.

        Args:
            value: sequence of numbers - New tween value.
            time: number - Absolute time to reach final value.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time(time, len(self.frames))
        for i in range(count):
            nextvalue = []
            factor = (i + 1) / count
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def to_d(self, value, time):
        """
        Make the tween value move from its current value to a new value, finishing after the specified time period.
        The transition is linear.

        Args:
            value: sequence of numbers - New tween value.
            time: number - Relative time period to reach final value.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time_d(time)
        for i in range(count):
            nextvalue = []
            factor = (i + 1) / count
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def ease(self, value, time, ease_function):
        """
        Make the tween value move from its current value to a new value, finishing at the specified time.
        The transition is controlled by the easing function.

        Args:
            value: sequence of numbers - New tween value.
            time: number - Absolute time to reach final value.
            ease_function: function - Easing function. Thus accepts a value that varies between 0 and 1.0.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time(time, len(self.frames))
        for i in range(count):
            nextvalue = []
            factor = ease_function((i + 1) / count)
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def ease_d(self, value, time, ease_function):
        """
        Make the tween value move from its current value to a new value, finishing after the specified time period.
        The transition is controlled by the easing function.

        Args:
            value: sequence of numbers - New tween value.
            time: number - Absolute time to reach final value.
            ease_function: function - Easing function. Thus accepts a value that varies between 0 and 1.0.

        Returns:
            self
        """
        self.check_value(value, self.previous)
        count = self.check_and_convert_time_d(time)
        for i in range(count):
            nextvalue = []
            factor = ease_function((i + 1) / count)
            for a, b in zip(self.previous, value):
                nextvalue.append(a + factor * (b - a))
            self.frames.append(nextvalue)
        self.previous = value
        return self

    def check_value(self, value, previous):
        if not isinstance(value, collections.abc.Sequence) or isinstance(value, str):
            raise ValueError('Sequence value required')
        if len(value) <= 0:
            raise ValueError('Vectors of rank 0 are not supported')
        if previous and len(value) != len(self.previous):
            raise ValueError('All values must be vectors of equal rank')


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

