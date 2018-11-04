from pytexture import vector_image


def draw(ctx, **extras):
    # Example, replace with your own code
    ctx.rectangle(0.5, 0.7, 2, 1)
    ctx.set_source_rgb(1, .5, 0)
    ctx.fill()


vector_image.make_vector_png("/tmp/vector.png", draw, pixel_size=(300, 200),
                             width=3, color=(1, 1, 1))
