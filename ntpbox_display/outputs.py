from PIL import Image, ImageDraw


class Output():

    def getcontext(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError


class PNGOutput(Output):

    def __init__(self, path, x, y):
        self._path = path
        self._x = x
        self._y = y

    def getcontext(self):
        self._im = Image.new(mode='1', size=(self._x, self._y))
        self._draw = ImageDraw.Draw(self._im)
        return self._draw

    def flush(self):
        del self._draw

        with open(self._path, 'wb') as f:
            self._im.save(f, 'png')
