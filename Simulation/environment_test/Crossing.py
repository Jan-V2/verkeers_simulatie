from copy import copy
from dataclasses import dataclass
from environment_test.Types import *
from environment_test.Coord import Coord
from environment_test.Types import Ordinal
from environment_test.Route_Components import *


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
            raise Exception("road does not appear to be connected to crossing " + str(in_from) )

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
