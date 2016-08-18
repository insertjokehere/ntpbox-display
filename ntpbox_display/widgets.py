from datetime import datetime

from . import lib


class CenteredTextWidget(lib.CenterWidgetMixin, lib.TextWidget):

    def __init__(self, **kwargs):
        super(CenteredTextWidget, self).__init__(**kwargs)


class TimeWidget(CenteredTextWidget):

    @property
    def text(self):
        return datetime.now().strftime("%H:%M:%S")


class IconValueWidget(lib.CompositeWidget):

    def __init__(self, icon, value, icon_font, text_font, draw,
                 icon_offset=None, text_offset=None, spacing=0.25, **kwargs):

        icon = lib.TextWidget(font=icon_font, text=icon, draw=draw)
        if icon_offset is not None:
            icon.add_offset(*icon_offset)

        text = lib.TextWidget(font=text_font, text=str(value), draw=draw)
        if text_offset is not None:
            text.add_offset(*text_offset)

        text.add_offset(spacing * icon.width, 0)

        widgets = [icon, text]

        super(IconValueWidget, self).__init__(
            widgets=widgets,
            reflow=lib.CompositeWidget.reflow_horizontal,
            draw=draw,
            **kwargs
        )
