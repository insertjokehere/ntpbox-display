BLACK = 0
WHITE = 1


class Widget(object):

    def __init__(self, draw, offset_x=0, offset_y=0):
        self.draw = draw
        self.offset_x = offset_x
        self.offset_y = offset_y

    def render(self):
        return

    @property
    def width(self):
        return 0

    @property
    def height(self):
        return 0

    @property
    def x(self):
        return self.offset_x

    @property
    def y(self):
        return self.offset_y

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    def add_offset(self, x, y):
        self.offset_x += x
        self.offset_y += y


class CenterWidgetMixin():

    @property
    def x(self):
        return self.offset_x + (self.draw.im.size[0] / 2) - (self.width / 2)

    @property
    def y(self):
        return self.offset_y + (self.draw.im.size[1] / 2) - (self.height / 2)


class TextWidget(Widget):

    def __init__(self, font, text="", colour=WHITE, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.font = font
        self._text = text
        self.colour = colour

    @property
    def width(self):
        return self.draw.textsize(self.text, self.font)[0]

    @property
    def height(self):
        return self.draw.textsize(self.text, self.font)[1]

    @property
    def text(self):
        return self._text

    def render(self):
        self.draw.text((self.x, self.y), self.text, fill=self.colour, font=self.font)


class CompositeWidget(Widget):

    def __init__(self, widgets, reflow=None, **kwargs):
        super(CompositeWidget, self).__init__(**kwargs)
        self._widgets = widgets
        if reflow is None:
            self._reflow = lambda w, x, y: (0, 0)
        else:
            self._reflow = reflow

    def _max_size(self):
        mx = []
        my = []
        offsets = (self.x, self.y)
        for widget in self._widgets:
            mx.append(widget.width + offsets[0])
            my.append(widget.height + offsets[1])
            offsets = self._reflow(widget, *offsets)
        mx.append(widget.width + offsets[0])
        my.append(widget.height + offsets[1])
        return max(mx), max(my)

    @property
    def width(self):
        return self._max_size()[0]

    @property
    def height(self):
        return self._max_size()[1]

    def add_widgets(self, *widgets):
        self._widgets += widgets

    @staticmethod
    def reflow_horizontal(widget, x, y):
        return (x + widget.width, y)

    def render(self):
        offsets = (self.x, self.y)
        for widget in self._widgets:
            widget.add_offset(*offsets)
            widget.render()
            offsets = self._reflow(widget, *offsets)
