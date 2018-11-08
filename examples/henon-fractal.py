from generativepy import array_image


LINECOLOR = (0, 0, 0.5)
LINEWIDTH = 0.01
A = 1


def draw(img, scale, **extras):
    x = 1.12
    y = 0.09
    for i in range(100000):
        x, y = y+1-1.4*x*x, 0.3*x
        user = scale.user2pixel((x, y))
        if user:
            img[user[0], user[1]] = (1, 1, .5)


array_image.make_array_png("/tmp/henon.png", draw, pixel_size=(1000, 1000), width=3, height=1,
                             startx=-1.5, starty=-0.5, color=(0, 0, 0))
