from generativepy.bitmap import makeBitmapImage


def draw(img, pixelSize, channels):
    img[:,:] = 1
    img[:50, :50] = (1, 0, 0)
    img[50:100, :50] = (0, 1, 0)
    img[100:150, :50] = (0, 0, 1)
    return img


makeBitmapImage("/tmp/makeBitmapImage.png", draw, pixelSize=(300, 200))
