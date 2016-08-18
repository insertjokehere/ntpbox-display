from . import widgets, lib
from PIL import Image, ImageDraw, ImageFont

SYM_SATCOUNT = "\uf012"
SYM_SYNCSTATE = "\uf0c2"

X = 128
Y = 64


class App:

    @staticmethod
    def main():
        fnt_time = ImageFont.truetype('DejaVuSansMono.ttf', 25)
        fnt_d = ImageFont.truetype('DejaVuSansMono.ttf', 11)
        fnt_icon = ImageFont.truetype('fontawesome-webfont.ttf', 10)

        im = Image.new(mode='1', size=(X, Y))

        draw = ImageDraw.Draw(im)

        root_widget = lib.CompositeWidget(draw=draw, widgets=[])

        sat_count = widgets.IconValueWidget(SYM_SATCOUNT, 3, fnt_icon, fnt_d, draw=draw)

        ntp_status = widgets.IconValueWidget(SYM_SYNCSTATE, 'o', fnt_icon, fnt_d,
                                             icon_offset=(0, 0.2 * sat_count.height),
                                             draw=draw)

        ntp_status.add_offset(X - ntp_status.width, 0)

        time = widgets.TimeWidget(draw=draw, font=fnt_time)

        ntp_jitter = widgets.CenteredTextWidget(
            font=fnt_d,
            text="±0.001µs",
            draw=draw
        )
        ntp_jitter.add_offset(0, time.height * 0.8)

        root_widget.add_widgets(sat_count, ntp_status, time, ntp_jitter)

        root_widget.render()

        del draw

        with open('test.png', 'wb') as f:
            im.save(f, 'png')
