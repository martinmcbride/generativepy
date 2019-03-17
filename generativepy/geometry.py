# Author:  Martin McBride
# Created: 2018-10-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import math

def angleMarker(canvas, a, b, c, count=1, radius=8, gap=2, rightangle=False):
    ang1 = math.atan2(a[1] - b[1], a[0] - b[0])
    ang2 = math.atan2(c[1] - b[1], c[0] - b[0])
    radius = canvas.page2user(radius)
    gap = canvas.page2user(gap)
    if rightangle:
        radius /= 2
        v = (math.cos(ang1), math.sin(ang1));
        pv = (math.cos(ang2), math.sin(ang2));
        canvas.polygon([(b[0] + v[0]*radius, b[1] + v[1]*radius),
                        (b[0] + (v[0] + pv[0])*radius, b[1] + (v[1]+pv[1])*radius),
                        (b[0] + pv[0]*radius, b[1] + pv[1]*radius)], False)
    elif count==2:
        canvas.arc(b[0], b[1], radius-gap/2, radius-gap/2, ang1, ang2)
        canvas.arc(b[0], b[1], radius+gap/2, radius+gap/2, ang1, ang2)
    elif count == 3:
        canvas.arc(b[0], b[1], radius - gap, radius - gap, ang1, ang2)
        canvas.arc(b[0], b[1], radius, radius, ang1, ang2)
        canvas.arc(b[0], b[1], radius + gap, radius + gap, ang1, ang2)
    else:
        canvas.arc(b[0], b[1], radius, radius, ang1, ang2)

def tick(canvas, a, b, count=1, length=4, gap=1):
    length = canvas.page2user(length)
    gap = canvas.page2user(gap)

    # Midpoint ofgline
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    if count==1:
        pos = (pmid[0], pmid[1])
        canvas.line(pos[0] + pvector[0]*length/2, pos[1] + pvector[1]*length/2, pos[0] - pvector[0]*length/2, pos[1] - pvector[1]*length/2)
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        canvas.line(pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2,
                    pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2)
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        canvas.line(pos[0] + pvector[0] * length / 2, pos[1] + pvector[1] * length / 2,
                    pos[0] - pvector[0] * length / 2, pos[1] - pvector[1] * length / 2)
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        canvas.line(pos[0] + pvector[0]*length/2, pos[1] + pvector[1]*length/2, pos[0] - pvector[0]*length/2, pos[1] - pvector[1]*length/2)
        pos = (pmid[0], pmid[1])
        canvas.line(pos[0] + pvector[0]*length/2, pos[1] + pvector[1]*length/2, pos[0] - pvector[0]*length/2, pos[1] - pvector[1]*length/2)
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        canvas.line(pos[0] + pvector[0]*length/2, pos[1] + pvector[1]*length/2, pos[0] - pvector[0]*length/2, pos[1] - pvector[1]*length/2)

def paratick(canvas, a, b, count=1, length=4, gap=1):
    length = canvas.page2user(length)
    gap = canvas.page2user(gap)

    def draw(x, y, ox1, oy1, ox2, oy2):
        canvas.line(x, y, x + ox1, y + oy1)
        canvas.line(x, y, x + ox2, y + oy2)

    # Midpoint ofgline
    pmid = ((a[0] + b[0])/2, (a[1] + b[1])/2)
    # Length of line
    len = math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))
    # Unit vector along line
    vector = ((b[0] - a[0]) / len, (b[1] - a[1]) / len)
    # Unit vector perpendicular to line
    pvector = (-vector[1], vector[0])

    if count==1:
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count == 2:
        pos = (pmid[0] - vector[0] * gap / 2, pmid[1] - vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0] * gap / 2, pmid[1] + vector[1] * gap / 2)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
    elif count==3:
        pos = (pmid[0] - vector[0]*gap, pmid[1] - vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0], pmid[1])
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
        pos = (pmid[0] + vector[0]*gap, pmid[1] + vector[1]*gap)
        draw(pos[0], pos[1], (-vector[0]+pvector[0])*length/2, (-vector[1]+pvector[1])*length/2, (-vector[0]-pvector[0])*length/2, (-vector[1]-pvector[1])*length/2)
