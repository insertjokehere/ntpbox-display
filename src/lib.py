BLACK = 0
WHITE = 1


class Widget():

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


class CenterWidgetMixin():

    @property
    def x(self):
        return self.offset_x + (self.draw.im.size[0] / 2) - (self.width / 2)

    @property
    def y(self):
        return self.offset_y + (self.draw.im.size[1] / 2) - (self.height / 2)


class TextWidget(Widget):

    def __init__(self, font, text, colour=WHITE, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.font = font
        self.text = text
        self.colour = colour

    @property
    def width(self):
        return self.draw.textsize(self.text, self.font)[0]

    @property
    def height(self):
        return self.draw.textsize(self.text, self.font)[1]

    def render(self):
        self.draw.text((self.x, self.y), self.text, fill=self.colour, font=self.font)
