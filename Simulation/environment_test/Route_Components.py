from environment_test.Types import *


def generate_obj_id():
    id = 0
    while True:
        yield id
        id += 1


id_generator = generate_obj_id()


class Route_Component:
    def __init__(self):
        self.id = next(id_generator)


class Tile(Route_Component):
    def __init__(self, coord, tile_char):
        super().__init__()
        self.coord = coord
        if tile_char.isnumeric():
            self.tile_type = Tile_Types.road
            self.road_value = int(tile_char)
        else:
            for type in Tile_Types:
                if type.value[0] is tile_char:
                    self.tile_type = type
                    return
            raise TypeError("tile char not valid tile. char is " + tile_char)


class Road(Route_Component):
    def __init__(self, start_coord, is_incoming):
        super().__init__()
        self.route = [start_coord]
        self.finished = False
        self.is_incoming = is_incoming
        self.route_value = -1
        self.end = None

    # noinspection PyDefaultArgument
    def solve(self, _tile_array, found_direction_tile=False, banned_coords=[], prev_non_car_tile=None):
        # stuurt terug volgende startpunt, als dat er is
        # er zou op een kloppende kaart altijd maar 1 mogelijke optie moten zijn, maar daar word niet voor gecheckt.
        if self.finished:
            return
        else:
            head = self.get_last()
            targets = []
            if head.x > 0:
                targets.append(head.translate(-1, 0))
            if head.y > 0:
                targets.append(head.translate(0, -1))
            if head.x < len(_tile_array[0]) - 1:
                targets.append(head.translate(1, 0))
            if head.y < len(_tile_array) - 1:
                targets.append(head.translate(0, 1))
            targets = list(filter(lambda t: t not in banned_coords and t not in self.route, targets))
            if not found_direction_tile:
                # ga op zoek naar volgende road tegel
                for target in targets:
                    if _tile_array[target.y][target.x].tile_type == Tile_Types.road:
                        if _tile_array[target.y][target.x].road_value == self.route_value + 1:
                            self.route.append(target)
                            self.route_value += 1
                            return self.solve(_tile_array)
                # ga op zoek naar aan een voet/fiets pad
                for target in targets:
                    if _tile_array[target.y][target.x].tile_type in non_car_tiles and \
                            _tile_array[target.y][target.x].tile_type != prev_non_car_tile:
                        self.route.append(target)
                        self.route_value += 1

                        return self.solve(_tile_array, prev_non_car_tile=_tile_array[target.y][target.x].tile_type)
                # ga op zoek naar een aan een kruispunt genzende tegel
                for target in targets:
                    if _tile_array[target.y][target.x].tile_type in directioned_tiles:
                        self.route.append(target)
                        return self.solve(_tile_array, True)
                # ga op zoek naar merge/split punt
                for target in targets:
                    if _tile_array[target.y][target.x].tile_type in merge_or_split:
                        self.end = target
                        self.finished = True
                        return target
            # ga op zoek naar kruispunt
            for target in targets:
                if _tile_array[target.y][target.x].tile_type == Tile_Types.crossing:
                    self.end = target
                    self.finished = True
                    return target
        raise Exception("road found dead end at " + str(self.get_last()))

    def get_start(self):
        return self.route[0]

    def get_last(self):
        return self.route[len(self.route) - 1]

# merges en splits moeten als laatste geevalueerd worden.

# class Split(Road):
#    # a sort of wrapper class that manages 2 or 3 internal road classes
#    def __init__(self, start_coord, is_incoming):
#        super().__init__(start_coord, is_incoming)


class Merge(Road):
    def __init__(self, start_coord, is_incoming, inflow_coord):
        super().__init__(start_coord, is_incoming)
        self.banned_coords = [inflow_coord]

    def add_inflow(self, coord):
        self.banned_coords.append(coord)

    def solve(self, _tile_array, found_direction_tile=False, banned_coords=(), prev_non_car_tile=None):
        return super(Merge, self).solve(_tile_array, banned_coords=self.banned_coords,
                                        prev_non_car_tile=prev_non_car_tile)
