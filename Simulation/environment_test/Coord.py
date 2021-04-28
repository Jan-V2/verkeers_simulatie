class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other_coord):
        if not isinstance(other_coord, Coord):
            return NotImplemented
        return Coord(self.x - other_coord.x,
                     self.y - other_coord.y)

    def __add__(self, other_coord):
        if not isinstance(other_coord, Coord):
            return NotImplemented
        return Coord(self.x + other_coord.x,
                     self.y + other_coord.y)

    def __eq__(self, other):
        if not isinstance(other, Coord):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def translate(self, x, y):
        return Coord(self.x + x, self.y + y)

    def translate_x(self, x):
        return self.translate(x, 0)

    def translate_y(self, y):
        return self.translate(0, y)

    def __str__(self):
        return "(x={}, y={})".format(self.x, self.y)

