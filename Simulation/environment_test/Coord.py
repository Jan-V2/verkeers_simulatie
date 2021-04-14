class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other_coord):
        self.x -= other_coord.x
        self.y -= other_coord.y
        return self

    def __add__(self, other_coord):
        self.x += other_coord.x
        self.y += other_coord.y
        return self

    def translate(self, x, y):
        return Coord(self.x + x, self.y + y)

    def translate_x(self, x):
        return self.translate(x, 0)

    def translate_y(self, y):
        return self.translate(0, y)

    def __str__(self):
        return "(x={}, y={})".format(self.x, self.y)
