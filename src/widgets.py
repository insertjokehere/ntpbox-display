import lib


class TimeWidget(lib.TextWidget, lib.CenterWidgetMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(self, text="00:00:00", *args, **kwargs)
