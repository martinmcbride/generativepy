from generativepy.bitmap import makeBitmapImage, BM_ROWCOL

def draw(img, scaling):
    img[:,:] = 1
    start = scaling.u2p([0.5, 0.1])
    end = scaling.u2p([2.75, 1.1])
    img[start[0]:end[0], start[1]:end[1]] = (1, 0, 0)
    return img


makeBitmapImage("/tmp/makeBitmapImage.png", draw, pixelSize=(300, 200), width=3, height=2)
makeBitmapImage("/tmp/makeBitmapImage2.png", draw, pixelSize=(300, 200), width=3, height=2, orientation=BM_ROWCOL)
