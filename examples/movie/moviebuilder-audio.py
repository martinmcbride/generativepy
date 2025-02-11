from generativepy.geometry import Circle, Rectangle
from generativepy.color import Color
from generativepy.drawing import setup, make_image_frames
from generativepy.movie import MovieBuilder
from generativepy.tween import TweenVector
from generativepy.utils import temp_file

# Create a movie with two scenes and audio files
WIDTH = 200         # Nominal width, used for all drawing
HEIGHT = 300        # Nominal width, used for all drawing
OUTPUTWIDTH = 200   # Final video width, could be made larger for 4k output
OUTPUTHEIGHT = 300  # Final video height, could be made larger for 4k output

FRATE = 10
VIDEONAME = temp_file("movie-audio.mp4")

def t2f(t):   # Convert a time in seconds to a number of frames
    return int(t*FRATE)

def scene1(duration):

    position = TweenVector((0, 0)).to((200, 300), t2f(duration))

    def draw(ctx, pixel_width, pixel_height, fn, frame_count):
        setup(ctx, pixel_width, pixel_height, width=OUTPUTWIDTH, height=OUTPUTHEIGHT, background=Color(0.5))

        Circle(ctx).of_center_radius(position[fn], 30).fill(Color("red"))

    return make_image_frames(draw, WIDTH, HEIGHT, t2f(duration)), duration

def scene2(duration):

    position = TweenVector((0, 0)).to((200, 300), t2f(duration))

    def draw(ctx, pixel_width, pixel_height, fn, frame_count):
        setup(ctx, pixel_width, pixel_height, width=OUTPUTWIDTH, height=OUTPUTHEIGHT, background=Color(0.5))

        Rectangle(ctx).of_corner_size(position[fn], 50, 50).fill(Color("green"))

    return make_image_frames(draw, WIDTH, HEIGHT, t2f(duration)), duration



builder = MovieBuilder(FRATE)
builder.add_scene(scene1(5), "scene1-audio.mp3")
builder.add_scene(scene2(5), "scene2-audio.mp3")

# builder.make_movie(VIDEONAME, n) creates video of just scene n
# builder.make_movie(VIDEONAME) creates full video
builder.make_movie(VIDEONAME)