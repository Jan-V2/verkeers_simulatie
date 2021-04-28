# todo specify road with north/south road, and combine merge splits
from copy import copy
from enum import Enum, auto
from functools import reduce
from pprint import pprint

from environment_test.Coord import Coord
from dataclasses import dataclass


class Tile_Types(Enum):
    empty = 'X',  # leeg
    crossing = '*',  # kruispunt
    road = None,  # weg, als het grenst aan een kruispunt rechtdoorgaande weg
    b_lane = 'P',  # fietspad
    sidewalk = "S"  # voedgangerpad
    car_spawn = 'A',  # auto spawn punt
    b_spawn = 'F',  # fiets spawn punt
    despawn = "V",  # despawn punt
    left = 'L',  # als het grenst aan een kruispunt linksafslaande weg
    right = 'R',  # als het grenst aan een kruispunt rechtsafslaande weg
    left_straight = 'E',  # als het grenst aan een kruispunt linksafslaande en rechtdoor gaande weg
    right_straight = 'Q',  # als het grenst aan een kruispunt rechtsafslaande en rechtdoor gaande weg
    split = "U",  # voor uitvoegen
    merge = "I"  # voor invoegen
    straight = "W"  # rechtdoor


class Ordinal(Enum):
    north = 0
    east = 1
    south = 2
    west = 3


directioned_tiles = [Tile_Types.left, Tile_Types.right, Tile_Types.left_straight,
                     Tile_Types.right_straight, Tile_Types.straight]
merge_or_split = [Tile_Types.merge, Tile_Types.split]
starting_tiles = [Tile_Types.car_spawn, Tile_Types.b_spawn, Tile_Types.despawn]
non_car_tiles = [Tile_Types.b_lane, Tile_Types.sidewalk]


# elk routeonderdeel heeft een id, wat overeenkomt met de plek in de route_components array
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
            if head.x < len(tile_array[0]) - 1:
                targets.append(head.translate(1, 0))
            if head.y < len(tile_array) - 1:
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


@dataclass
class Incoming:
    in_from: Coord
    in_from_ord: Ordinal
    destination_ordinals: list
    id: int


@dataclass
class Outgoing:
    out_from: Coord
    out_from_ord: Ordinal
    id: int


@dataclass
class Traffic_Light:
    id: int
    ordinal_in: Ordinal
    ordinals_out: []
    coords_in: []
    coords_out: []
    collision_x_high: int
    collision_x_low: int
    collision_y_high: int
    collision_y_low: int


class Crossing:
    # er word ervan uitgegaan dat een kruispunt rechthoekig is
    def __init__(self, coord, _tile_array):
        self.incoming = []
        self.outgoing = []
        self.x_highest = coord.x
        self.y_highest = coord.y
        self.x_lowest = coord.x
        self.y_lowest = coord.y
        self.contains = []
        self.traffic_lights = []
        self.__find_neighbours(_tile_array, [coord])
        for coord in self.contains:
            if coord.x > self.x_highest:
                self.x_highest = coord.x
            if coord.x < self.x_lowest:
                self.x_lowest = coord.x
            if coord.y > self.y_highest:
                self.y_highest = coord.y
            if coord.y < self.y_lowest:
                self.y_lowest = coord.y

    # noinspection PyDefaultArgument
    def __find_neighbours(self, _tile_array, to_be_visited, visited=[]):
        if len(to_be_visited) > 0:
            _next = to_be_visited.pop(0)
        else:
            return
        in_visited = False
        for coord in visited:
            if coord == _next:
                in_visited = True
                break
        if not in_visited:
            if _tile_array[_next.y][_next.x].tile_type == Tile_Types.crossing:
                self.contains.append(_next)
                to_be_visited.append(_next.translate(-1, 0))
                to_be_visited.append(_next.translate(0, -1))
                to_be_visited.append(_next.translate(1, 0))
                to_be_visited.append(_next.translate(0, 1))
        visited.append(_next)
        self.__find_neighbours(_tile_array, to_be_visited, visited)

    def __direction_translator(self, in_ordinal, direction):
        # translate handedness to ordinals
        # straight ahead is 2
        # left is + 1
        # right is -1
        in_val = in_ordinal.value + direction
        if in_val < 0:
            in_val = 4 - in_val
        if in_val > 3:
            in_val -= 4
        for _ord in Ordinal:
            if _ord.value == in_val:
                return _ord

    def includes(self, coord):
        # todo optimize
        for item in self.contains:
            if item == coord:
                return True
        return False

    def add_road(self, road, _tile_map):
        if not isinstance(road, Road):
            raise TypeError("Crossing can only add Road type")
        in_from = road.get_last()
        in_from_ordinal = None
        dest_ordinals = []
        in_type = _tile_map[in_from.y][in_from.x].tile_type
        if self.x_lowest - 1 < in_from.x < self.x_highest + 1:
            if in_from.y > self.y_highest:
                in_from_ordinal = Ordinal.south
            if in_from.y < self.y_lowest:
                in_from_ordinal = Ordinal.north
        elif self.y_lowest - 1 < in_from.y < self.y_highest + 1:
            if in_from.x > self.x_highest:
                in_from_ordinal = Ordinal.east
            if in_from.x < self.x_lowest:
                in_from_ordinal = Ordinal.west
        if in_from_ordinal is None:
            raise Exception("road does not appear to be connected to crossing")

        if road.is_incoming:
            # check each of the three directions
            if in_type == Tile_Types.road or in_type == Tile_Types.straight:
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, 2))
            elif in_type == Tile_Types.left:
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, 1))
            elif in_type == Tile_Types.right:
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, -1))
            elif in_type == Tile_Types.left_straight:
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, 2))
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, 1))
            elif in_type == Tile_Types.right_straight:
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, 2))
                dest_ordinals.append(self.__direction_translator(in_from_ordinal, -1))
            else:
                raise TypeError("tile type nog found")
            self.incoming.append(Incoming(road.get_last(), in_from_ordinal, dest_ordinals, road.id))
        else:
            self.outgoing.append(Outgoing(in_from, in_from_ordinal, road.id))

    def get_destinations(self, coord):
        pass

    def create_traffic_lights(self):
        def check_if_light_created(incoming_road):
            for light in self.traffic_lights:
                if light.ordinal_in == incoming_road.in_from_ord:
                    if len(light.ordinals_out) == len(incoming_road.destination_ordinals):
                        for ord in incoming_road.destination_ordinals:
                            if ord not in light.ordinals_out:
                                return None
                        return light
            return None

        # checken of licht er al in zit
        # licht toevoegen
        light_id = 0
        for in_road in self.incoming:
            dest_light = check_if_light_created(in_road)
            if dest_light == None:
                out_roads = list(filter(lambda o: o.out_from_ord in in_road.destination_ordinals, self.outgoing))
                # out_coords = list(map(lambda o: o.out_from, out_roads))
                out_coords = []
                for road in out_roads:
                    out_coords.append(road.out_from)
                self.traffic_lights.append(Traffic_Light(id=light_id,
                                                         ordinal_in=in_road.in_from_ord,
                                                         ordinals_out=in_road.destination_ordinals,
                                                         coords_in=[in_road.in_from],
                                                         coords_out=out_coords,
                                                         collision_x_low=None,
                                                         collision_x_high=None,
                                                         collision_y_low=None,
                                                         collision_y_high=None))
                light_id += 1
            else:
                dest_light.coords_in.append(in_road.in_from)

        # check if every road has been added to the crossing
        # in_coords = list(map(lambda in_road: in_road.in_from, self.incoming))
        # for out_road in self.outgoing
        pass

    def solve_collisions(self):
        # todo check kruislinks
        matrix = []
        for light in self.traffic_lights:
            row = []
            light_ords = copy(light.ordinals_out)
            light_ords.append(light.ordinal_in)
            for opposing_light in self.traffic_lights:
                if opposing_light.id == light.id:
                    row.append(True)
                else:
                    can_cross = True
                    for _ord in opposing_light.ordinals_out:
                        if _ord in light_ords:
                            can_cross = False
                            break
                    if opposing_light.ordinal_in in light.ordinals_out:
                        can_cross = False

                    row.append(can_cross)
            matrix.append(row)
        return matrix


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


if __name__ == '__main__':
    tile_array = []
    route_components = []
    crossings = []

    with open("kruispunt3.txt", "r") as file:
        char_map = file.read().split("\n")
        # ruimt lege regel aan het einde van het bestand op
        if char_map[len(char_map) - 1] == "":
            char_map = char_map[:len(char_map) - 1]

    for y in range(len(char_map)):
        new_row = []
        for x in range(len(char_map[y])):
            new_row.append(Tile(Coord(x, y), char_map[y][x]))
        tile_array.append(new_row)

    # get starting points for road generation
    for row in tile_array:
        for tile in row:
            if tile.tile_type in starting_tiles:
                if tile.tile_type == Tile_Types.despawn:
                    route_components.append(Road(tile.coord, False))
                else:
                    route_components.append(Road(tile.coord, True))

    while True:
        all_finished = True
        for component in route_components:
            if not component.finished:
                all_finished = False
                break
        if all_finished:
            break

        for component in route_components:
            if not component.finished:
                end_point = component.solve(tile_array)
                if tile_array[end_point.y][end_point.x].tile_type == Tile_Types.crossing:
                    found_existing = False
                    for crossing in crossings:
                        if crossing.includes(end_point):
                            found_existing = True
                            crossing.add_road(component, tile_array)
                    if not found_existing:
                        cr = Crossing(end_point, tile_array)
                        cr.add_road(component, tile_array)

                        crossings.append(cr)
                elif tile_array[end_point.y][end_point.x].tile_type == Tile_Types.merge:
                    found_existing = False
                    for comp in route_components:
                        if end_point == comp.get_start():
                            comp.add_inflow(component.get_last())
                            found_existing = True
                    if not found_existing:
                        route_components.append(Merge(end_point, component.is_incoming, component.get_last()))

    crossings[0].create_traffic_lights()
    light_matrix = crossings[0].solve_collisions()
    print("test")
