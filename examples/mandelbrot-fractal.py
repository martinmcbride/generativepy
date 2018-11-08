from generativepy import array_image


def calc(c1, c2):
    x = y = 0
    for i in range(1000):
        x, y = x*x - y*y + c1, 2*x*y + c2
        if x*x + y*y > 4:
            return i+1
    return 0


def draw(img, scale, **extras):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x, y = scale.pixel2user((i, j))
            v = calc(x, y)
            img[i, j] = (0, 0, 0) if not v else (1, 1, 1)


array_image.make_array_png("/tmp/mandelbrot.png", draw, pixel_size=(200, 200), width=3, height=3,
                             startx=-2, starty=-1.5, color=(0, 0, 0))
