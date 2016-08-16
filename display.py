#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

BLACK = 0
WHITE = 1

SYM_SATCOUNT = "\uf012"
SYM_SYNCSTATE = "\uf0c2"


X = 128
Y = 64


def center_text(text, font):
    w, h = draw.textsize(text, font=font)
    return ((X / 2) - (w / 2), (Y / 2) - (h / 2))

fnt_time = ImageFont.truetype('DejaVuSansMono.ttf', 25)
fnt_d = ImageFont.truetype('DejaVuSansMono.ttf', 11)
fnt_icon = ImageFont.truetype('fontawesome-webfont.ttf', 10)

im = Image.new(mode='1', size=(X, Y))

draw = ImageDraw.Draw(im)

timestr = datetime.now().strftime("%H:%M:%S")
draw.text(center_text(timestr, fnt_time), timestr, fill=WHITE, font=fnt_time)
draw.text((0, 0), SYM_SATCOUNT, fill=WHITE, font=fnt_icon)
draw.text((draw.textsize(SYM_SATCOUNT, fnt_icon)[0] + 2, 0), "9", fill=WHITE, font=fnt_d)

sync_state = "?"
draw.text((X - draw.textsize(SYM_SYNCSTATE, fnt_icon)[0] - draw.textsize(sync_state, fnt_d)[0], 2), SYM_SYNCSTATE, fill=WHITE, font=fnt_icon)
draw.text((X - draw.textsize(sync_state, fnt_d)[0], 0), sync_state, fill=WHITE, font=fnt_d)

t = "±0.001µs"
tx, ty = center_text(t, fnt_d)
ty += draw.textsize("0", fnt_time)[1] * .95

draw.text((tx, ty), t, fill=WHITE, font=fnt_d)
del draw

with open('test.png', 'wb') as f:
    im.save(f, 'png')
