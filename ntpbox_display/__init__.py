from . import widgets, lib, outputs
from PIL import ImageFont
from pkg_resources import resource_stream
from time import sleep
import argparse
import logging

SYM_SATCOUNT = "\uf012"
SYM_SYNCSTATE = "\uf0c2"

logger = logging.getLogger(__name__)


class App:

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()

        parser.add_argument('--width', default=128, type=int)
        parser.add_argument('--height', default=64, type=int)
        parser.add_argument('--output', choices=['png'], default='png')
        parser.add_argument('--output-path', required=False)

        subparser = parser.add_subparsers(dest='command')
        subparser.required = True
        status_parser = subparser.add_parser('status')

        fonts_group = status_parser.add_argument_group('Fonts')

        fonts_group.add_argument('--time-font', default='DejaVuSansMono.ttf')
        fonts_group.add_argument('--time-font-size', default=25, type=int)

        fonts_group.add_argument('--details-font', default='DejaVuSansMono.ttf')
        fonts_group.add_argument('--details-font-size', default=11, type=int)

        fonts_group.add_argument('--icon-font', default=None)
        fonts_group.add_argument('--icon-font-size', default=10, type=int)

        status_parser.add_argument('--once', action='store_true')
        status_parser.set_defaults(func=App.status)

        args = parser.parse_args()

        if args.output == "png" and not args.output_path:
            logger.error("Must specify --output-path for output png")
            exit(1)

        args.func(args)

    @staticmethod
    def _get_output(args):
        if args.output == 'png':
            return outputs.PNGOutput(args.output_path, args.width, args.height)
        else:
            raise NotImplementedError

    @staticmethod
    def status(args):

        fnt_time = ImageFont.truetype(args.time_font, args.time_font_size)
        fnt_d = ImageFont.truetype(args.details_font, args.details_font_size)

        if args.icon_font is None:
            fnt_icon = ImageFont.truetype(
                resource_stream('ntpbox_display', 'fontawesome-webfont.ttf'),
                args.icon_font_size)
        else:
            fnt_icon = ImageFont.truetype(args.icon_font, args.icon_font_size)

        while True:
            App.render(App._get_output(args), fnt_time, fnt_d, fnt_icon, 3, 'o', 0.001, args.width, args.height)
            if args.once:
                break
            sleep(0.5)

    @staticmethod
    def render(output, fnt_time, fnt_d, fnt_icon, sat_count, ntp_status, jitter, x, y):
        draw = output.getcontext()

        root_widget = lib.CompositeWidget(draw=draw, widgets=[])

        sat_count = widgets.IconValueWidget(SYM_SATCOUNT, sat_count, fnt_icon, fnt_d, draw=draw)

        ntp_status = widgets.IconValueWidget(SYM_SYNCSTATE, ntp_status, fnt_icon, fnt_d,
                                             icon_offset=(0, 0.2 * sat_count.height),
                                             draw=draw)

        ntp_status.add_offset(x - ntp_status.width, 0)

        time = widgets.TimeWidget(draw=draw, font=fnt_time)

        ntp_jitter = widgets.CenteredTextWidget(
            font=fnt_d,
            text="±{}µs".format(jitter),
            draw=draw
        )
        ntp_jitter.add_offset(0, time.height * 0.8)

        root_widget.add_widgets(sat_count, ntp_status, time, ntp_jitter)

        root_widget.render()

        output.flush()
