from generativepy.movie import save_frames
from generativepy.drawing import make_image_frames
from generativepy.color import Color

'''
Create a simple movie of 20 frames
The frames will be stored as PNG images in /tmp with names
 - movie00000000.pngmake_image_frames
 - movie00000001.png
 - movie00000002.png
 - etc
'''

def draw(ctx, width, height, frame_no, frame_count):
    ctx.set_source_rgba(*Color(1).rgba)
    ctx.paint()

    # Draw a rectangle.
    # It's position changes for each frame.
    ctx.set_source_rgba(*Color(0.5, 0, 0).rgba)
    ctx.rectangle(50+20*frame_no, 50+10*frame_no, 100, 100)
    ctx.fill()

frames = make_image_frames(draw, 500, 350, 20)
save_frames("/tmp/movie", frames)
