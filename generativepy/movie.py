# Author:  Martin McBride
# Created: 2019-01-24
# Copyright (C) 2018, Martin McBride
# License: MIT

import numpy as np
from PIL import Image
from generativepy.utils import temp_file
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import subprocess as sp
import pathlib


'''
The movie functions operate pn lazy sequences of images. The images are stored as numpy arrays.
'''

def normalise_array(array):
    """
    If greyscale array has a shape [a, b, 1] it must be normalised to [a, b] otherwise
    the pillow fromarray function will give n#an error
    :param array: The array
    :return: squeezed array if necessary, else the original array
    """
    if array.ndim == 3 and array.shape[2] == 1:
        return np.squeeze(array, axis=2)
    return array

def duplicate_frame(frame, count):
    '''
    Duplicate a single frame, multiple times
    :param frame: the frame, a numpy array
    :param count: Number of times to duplicate
    :return: Generator
    '''
    for i in range(count):
        yield frame

def save_frame(outfile, frame):
    """
    Save a frame as a png image
    :param outfile: Full name and path of the file (.png extension optional)
    :param frame: The sequence of frames
    :return:
    """

    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    image = Image.fromarray(normalise_array(frame))
    image.save(outfile + '.png')

def save_frames(outfile, frames):
    """
    Save a sequence of frame as a sequence of png images
    :param outfile: Base name and path of the file (.png extension optional)
    :param frames: The sequence of frames
    :return:
    """

    if outfile.lower().endswith('.png'):
        outfile = outfile[:-4]
    for i, frame in enumerate(frames):
        image = Image.fromarray(normalise_array(frame))
        image.save(outfile + str(i).zfill(8) + '.png')


def create_videoclip(frames, duration, frame_rate, audio_in=None):
    """
    Create a VideoClip object
    :param frames: a iterator returning numpy frame objects
    :param duration: Duration of clip in seconds
    :param audio_in: file name of audio file, or None
    :return:
    """

    def make_frame(t):
        nonlocal current_frame
        nonlocal current_frame_index
        required_frame_index = int(t*frame_rate)
        if required_frame_index > current_frame_index:
            current_frame = next(frames)
            current_frame_index += 1
        rgb_frame = np.empty((current_frame.shape[0], current_frame.shape[1], 3), dtype=np.uint8)
        rgb_frame[:, :] = current_frame[:, :, 0:3]
        return rgb_frame

    current_frame = next(frames)
    current_frame_index = 0
    video_clip = VideoClip(make_frame, duration=duration)
    if audio_in:
        print("Adding audio clip", audio_in)
        audio_clip = AudioFileClip(audio_in).subclip(0, duration)
        video_clip = video_clip.set_audio(audio_clip)
    return video_clip


class MovieBuilder():
    """
    Builds up a movie
    """

    def __init__(self, frame_rate):
        self.frame_rate = frame_rate
        self.frame_sources = []
        self.audio_files = []
        self.duration = []

    def add_scene(self, frame_source_duration, audio_file=None):
        """
        Add a clip
        :param frame_source_duration: Tuple of (frame_source, duration). frame_source is a iterator returning
        numpy frame objects, duration is the clip duration in seconds
        :param audio_file:
        :return:
        """
        self.frame_sources.append(frame_source_duration[0])
        self.duration.append(frame_source_duration[1])
        self.audio_files.append(audio_file)

    def make_movie(self, video_out, source=None):
        """
        Make a movie of either all the clips that have been added, or just a single clip if source is not None
        :param video_out: Filename of output file.
        :param source: set to index of a clip to use just that clip, or None to join all clips
        :return:
        """
        if source is not None:
            video = create_videoclip(self.frame_sources[source], self.duration[source], self.frame_rate, self.audio_files[source])
        else:
            clips = [create_videoclip(s, d, self.frame_rate, a) for s, d, a in zip(self.frame_sources, self.duration, self.audio_files)]
            video = concatenate_videoclips(clips)

        # Due to a bug in moviepy 1.0.1, when we write a video out in this mode the audio is not included.
        # So we write the video and audio out to separate temporary files.
        # We then use ffmpeg directly to combine the video and audio.
        temp_video_filename = temp_file(pathlib.Path(video_out).stem + "TEMP.mp4")
        temp_audio_filename = temp_file(pathlib.Path(video_out).stem + "TEMP.m4a")

        if not self.audio_files[0]:
            video.write_videofile(video_out, codec="libx264", fps=self.frame_rate)
        else:
            video.write_videofile(temp_video_filename, temp_audiofile=temp_audio_filename, codec="libx264",
                                  remove_temp=False, audio_codec="aac", fps=self.frame_rate)

            command = ["ffmpeg",
                       "-y", #approve output file overwite
                       "-i", temp_video_filename,
                       "-i", temp_audio_filename,
                       "-c:v", "copy",
                       "-c:a", "copy",
                       "-shortest",
                       "-r", str(self.frame_rate),
                       video_out ]
            process = sp.Popen(command)