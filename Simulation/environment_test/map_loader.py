from asciimatics.screen import Screen

from Coord import Coord

# todo specify road with north/south road, and combine merge splits

symbols ={
    "empty":'0', # leeg
    "crossing":'*', # kruispunt
    "road":'W', # weg, als het grenst aan een kruispunt rechtdoorgaande weg
    "b_lane":'P', # fietspad, als het grenst aan een kruispunt rechtdoorgaande
    "car_spawn":'A', # auto spawn punt
    "b_spawn":'F', # fiets spawn punt
    "despawn":"V", # despawn punt
    "left":'L', # als het grenst aan een kruispunt linksafslaande weg
    "right":'R', # als het grenst aan een kruispunt rechtsafslaande weg
    "left_straight":'E', # als het grenst aan een kruispunt linksafslaande en rechtdoor gaande weg
    "right_straight":'Q', # als het grenst aan een kruispunt rechtsafslaande en rechtdoor gaande weg
    "split":"U", # voor uitvoegen
    "merge":"I"  # voor invoegen
}
tile_size = 3


class Neighbours:
    def __init__(self, neighbours):
        self.data = neighbours

    def north(self):
        return self.data[0][1]

    def south(self):
        return self.data[2][1]

    def east(self):
        return self.data[1][2]

    def west(self):
        return self.data[1][0]


with open("kruispunt1.txt", "r") as file:
    map = file.read().split("\n")
    # ruimt lege regel aan het einde van het bestand op
    if map[len(map) -1] == "":
        map = map[:len(map) -1]


def get_neighbours(coord):
    # target coord not included in returned array
    try:
        result = [["0","0","0"],["0","0","0"],["0","0","0"]]

        def get_symbol(_coord):
            if 0 < _coord.x < len(map[0]):
                return map[_coord.y][_coord.x]
            return ""

        if coord.y > 0:
            for i in range(3):
                result[0][i] = get_symbol(coord.translate(i-1, -1))
        result[1][0] = get_symbol(coord.translate(-1, 0))
        result[1][2] = get_symbol(coord.translate(1, 0))
        if coord.y < len(map) -1:
            for i in range(3):
                result[2][i] = get_symbol(coord.translate(i-1, 1))
        return Neighbours(result)

    except IndexError:
        raise IndexError("are you sure the map is rectangular")


def demo(screen):
    while True:
        for row in range(len(map)):
            for column in range(len(map[0])):
                if map[row][column] == symbols["road"]:
                    neb = get_neighbours(Coord(column, row))
                    tile_top = Coord( tile_size * column, tile_size * row)
                    if neb.north() == symbols["road"] or neb.south() == symbols["road"] or \
                            neb.north() == symbols["crossing"] or neb.south() == symbols["crossing"]:
                        screen.move(tile_top.x, tile_top.y)
                        screen.draw(tile_top.x, tile_top.y + 3)
                        screen.move(tile_top.x + 2, tile_top.y)
                        screen.draw(tile_top.x + 2, tile_top.y + 3)
                    elif neb.east() == symbols["road"] or neb.west() == symbols["road"] or \
                            neb.east() == symbols["crossing"] or neb.west() == symbols["crossing"]:
                        screen.move(tile_top.x, tile_top.y)
                        screen.draw(tile_top.x + 3, tile_top.y )
                        screen.move(tile_top.x , tile_top.y + 2)
                        screen.draw(tile_top.x + 3 , tile_top.y + 2 )


    #    screen.move(0, 0)
     #   screen.draw(10, 10)

        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()




def test():
    for row in range(len(map)):
        for column in range(len(map[0])):
            if map[row][column] == symbols["road"]:
                neb = get_neighbours(Coord(column, row))
                tile_top = Coord( tile_size * column, tile_size * row)

#test()

Screen.wrapper(demo)