from generativepy import vector_image


def draw(ctx, **extras):
    # Example, replace with your own code
    ctx.move_to(0, 1.5)
    ctx.line_to(1, -1)
    ctx.line_to(-1.5, 0)
    ctx.line_to(1, 1)
    ctx.line_to(0, -1.5)
    ctx.line_to(-1, 1)
    ctx.line_to(1.5, 0)
    ctx.line_to(-1, -1)
    ctx.close_path()
    ctx.set_source_rgb(0.5, 0.5, 0)
    ctx.set_line_width(0.05)
    ctx.stroke()


vector_image.make_vector_png("/tmp/vector-origin.png", draw, pixel_size=(400, 400),
                             width=4, color=(1, 1, 1), startx=-2, starty=-2)
