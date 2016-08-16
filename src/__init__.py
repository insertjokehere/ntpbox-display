import widgets
from PIL import Image, ImageDraw, ImageFont

fnt_time = ImageFont.truetype('DejaVuSansMono.ttf', 25)
fnt_d = ImageFont.truetype('DejaVuSansMono.ttf', 11)
fnt_icon = ImageFont.truetype('fontawesome-webfont.ttf', 10)

im = Image.new(mode='1', size=(128, 64))

draw = ImageDraw.Draw(im)

widgets.TimeWidget(draw=draw, font=fnt_time)

del draw

with open('test.png', 'wb') as f:
    im.save(f, 'png')
