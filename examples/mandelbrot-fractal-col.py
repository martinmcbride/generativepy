from generativepy import array_image


def calc(c1, c2):
    x = y = 0
    for i in range(1000):
        x, y = x*x - y*y + c1, 2*x*y + c2
        if x*x + y*y > 4:
            return i+1
    return 0

def create_color(v):
    values = [0, 64, 128, 196]
    b = values[v % 4]
    g = values[(v//4) % 4]
    r = values[(v//16) % 4]
    return (r, g, b)

def draw(img, scale, **extras):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x, y = scale.pixel2user((i, j))
            v = calc(x, y)
            img[i, j] = create_color(v)


array_image.make_array_png("/tmp/mandelbrot-col.png", draw, pixel_size=(500, 500), width=3, height=3,
                             startx=-2, starty=-1.5, color=(0, 0, 0))
