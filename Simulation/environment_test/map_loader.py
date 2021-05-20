from environment_test.Coord import Coord
from environment_test.Route_Components import *
from environment_test.Crossing import Crossing
from environment_test.Types import *

map_file = "kruispunt3_new.txt"


class Tile():
    def __init__(self, coord, tile_str):
        self.target_road = None  # alleen voor sensor tiles
        self.coord = coord
        tile_char = tile_str[0]
        if tile_char.isnumeric():
            self.tile_type = Tile_Types.road
            self.road_value = int(tile_char)
        else:
            self.tile_type = None
            for type in Tile_Types:
                if type.value[0] is tile_char:
                    self.tile_type = type
            if self.tile_type is None:
                raise TypeError("tile char not valid tile. char is " + tile_char)
        if self.tile_type == Tile_Types.sensor:
            target_str = tile_str[2:].split(".")
            self.target = Coord(int(target_str[0]), int(target_str[1]))
        if self.tile_type in non_car_tiles:
            try:
                self.road_value = int(tile_str[1])
            except IndexError:
                # als een non car tile niet een weg kruist heeft het geen roadnum
                if self.tile_type == Tile_Types.sensor:
                    raise IndexError("unable to find road num in sensor tile")

    def find_target_road(self, road_list):
        if self.tile_type != Tile_Types.sensor:
            raise NotImplementedError
        for road in road_list:
            if road.is_incoming:
                #print(road.get_last())
                if road.get_last() == self.target:
                    self.target_road = road
                    return
        raise Exception("sensor tile unable to find targeted road at " + str(self.target))


def create_tile_array():
    # laad het kruispunt bestand en maakt er een Tile array van
    ret = []
    with open(map_file, "r") as file:
        char_map = file.read().split("\n")
        # ruimt lege regel aan het einde van het bestand op
        if char_map[len(char_map) - 1] == "":
            char_map = char_map[:len(char_map) - 1]

    for row_num in range(len(char_map)):
        # noinspection PyTypeChecker
        char_map[row_num] = char_map[row_num].split(",")
        char_map[row_num] = char_map[row_num][:len(char_map[row_num]) - 1]
        for col_num in range(len(char_map[row_num])):
            if char_map[row_num][col_num][1] == " ":
                char_map[row_num][col_num] = char_map[row_num][col_num][0]

    for y in range(len(char_map)):
        new_row = []
        for x in range(len(char_map[y])):
            new_row.append(Tile(Coord(x, y), char_map[y][x]))
        ret.append(new_row)
    return ret


def generate_path_nodes(_route_components, subresource_start):
    subresource_str_start = "[sub_resource type=\"Curve3D\" id="
    subresource_str_end = "]\n_data = {\n\"points\": PoolVector3Array(  ),\n\"tilts\": PoolRealArray(  )\n}\n\n"
    node_str = \
        """[node name="{}" type="Path" parent="paths"]\ncurve = SubResource( {} )\n\n"""

    out_res = ""
    out_node = ""
    for road in _route_components:
        name = "{},{}|{},{}".format(road.get_start().x,road.get_start().y, road.get_last().x, road.get_last().y)
        out_res+= subresource_str_start + str(subresource_start) + subresource_str_end
        out_node += node_str.format(name, subresource_start)
        subresource_start += 1

    print(out_res)

def generate_sensor_nodes(_sensors):
    node_str = "[node name=\"{}\" type=\"Area\" parent=\"sensor_coming\"]\n\n[node name=\"CollisionShape\" type=\"CollisionShape\" parent=\"sensor_coming/{}\"]\ntransform = Transform( 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0 )\nshape = SubResource( 4 )\n\n"
    out = ""
    for sens in _sensors:
        name = "target={},{}".format(sens.target.x, sens.target.y)
        out += node_str.format(name, name)
    print(out)


def generate_path_tree(destination_coords, crossing_routes, road, _route_components):

    def ord_to_letter(ord):
        if ord is Ordinal.north:
            return "N"
        elif ord is Ordinal.west:
            return "W"
        elif ord is Ordinal.south:
            return "S"
        elif ord is Ordinal.east:
            return "E"
        raise TypeError("invalid ordinal")

    get_road_name = lambda r: "{},{}|{},{}".format(r.get_start().x, r.get_start().y, r.get_last().x, r.get_last().y)

    destination_roads = []
    crossing_route_names = []

    for lst in destination_coords:
        coord_names = []
        for coord in lst:
            for _comp in _route_components:
                if _comp.get_last() == coord:
                    coord_names.append(get_road_name(_comp))
        destination_roads.append(coord_names)

    for route in crossing_routes:
        crossing_route_names.append("{}->{}".format(ord_to_letter(route[0]), ord_to_letter(route[1])))

    ret = [get_road_name(road), []]

    for i in range(len(destination_roads)):
        ret[1].append(crossing_route_names[i])
        ret[1].append(destination_roads[i])
    return ret



if __name__ == '__main__':
    # in deze methode word de data opgebouwd, de volgorde is hierbij belangrijk.
    # je kan bijvoorbeeld geen stoplichten generen als het kruispunt niet af is.

    # tile_array is een array met een Tile voor elke tegel op de kaart
    # het is een 2d array die overeen komt met de ascii kaart
    tile_array = create_tile_array()
    # de route_components is een array van alle wegonderelen, zoals inkomende en uitgaande wegen, en in/uit voegen
    route_components = []
    crossings = []  # array van alle kruispunten
    sensors = []  # array van alle sensor tegels

    # pakt alle startpunten en sensor uit de tile array
    for row in tile_array:
        for tile in row:
            if tile.tile_type in starting_tiles:
                if tile.tile_type == Tile_Types.despawn:
                    route_components.append(Road(tile.coord, False))
                else:
                    route_components.append(Road(tile.coord, True))
            elif tile.tile_type == Tile_Types.sensor:
                sensors.append(tile)

    # loop waarin de wegen en kruispunten worden gegenereerd
    while True:
        # als alle wegen af zijn stopt de loop
        # dit moet in een loop omdat een merge/split pas gesolved kan worden, als alle ernaartoe leidende wegen af zijn
        all_finished = True
        for component in route_components:
            if not component.finished:
                all_finished = False
                break
        if all_finished:
            break

        for component in route_components:
            if not component.finished:
                # de solve method bouwt de weg op vanaf het startpunt naar een eindpunt
                end_point = component.solve(tile_array)
                if tile_array[end_point.y][end_point.x].tile_type == Tile_Types.crossing:
                    # als de weg eindigt bij een kruispunt word het aan een kruispunt toegevoegd.
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
                    # als een weg eindigd bij een merge of split point word een nieuwe weg gegenereerd
                    # todo maak split af
                    found_existing = False
                    for comp in route_components:
                        if end_point == comp.get_start():
                            comp.add_inflow(component.get_last())
                            found_existing = True
                    if not found_existing:
                        route_components.append(Merge(end_point, component.is_incoming, component.get_last()))

    # alles wat hierna gebeurd werkt alleen als alle wegen gegeneeerd zijn
    # genereed de stoplichten voor de kruispunten
    for crossing in crossings:
        crossing.create_traffic_lights()
    # lost de colisons voor het kruispunt op en geeft een collison matrix van bools als resultaat
    light_matrix = crossings[0].solve_collisions()
    for sensor in sensors:
        sensor.find_target_road(route_components)

    #generate_sensor_nodes(sensors)
    #generate_path_nodes(route_components, 26)

    # genereerd paths
    print("paths =[")
    for road in route_components:
        if road.is_incoming is True:
            destination_coords, crossing_routes= crossings[0].get_destinations(road)
            routes = generate_path_tree(destination_coords, crossing_routes, road, route_components)
            print("{},".format(routes))
    print("]\n")

    print("done")

paths =[
    ['8,15|8,19', ['N->E', '22,25|15,25']],
    ['9,15|9,19', ['N->S1', '8,31|8,26']],
    ['10,15|10,19', ['N->S2', '9,31|9,26']],
    ['11,15|11,19', ['N->E', '22,25|15,25']],
    ['22,20|15,20', ['E->N1', '14,15|14,19']],
    ['22,21|15,21', ['E->N2', '13,15|13,19']],
    ['22,22|15,22', ['E->W', '0,21|7,21'], ['E->S', '9,31|9,26']],
    ['0,23|7,23', ['W->N', '13,15|13,19']],
    ['0,24|7,24', ['W->E', '22,25|15,25']],
    ['0,25|7,25', ['W->S', '8,31|8,26']],
    ['11,31|11,26', ['S->W',  '0,21|7,21']],
    ['12,31|12,26', ['S->N1', '13,15|13,19']],
    ['13,31|13,26', ['S->N2', '14,15|14,19']],
    ['14,31|14,26', ['S->E', '22,25|15,25']],
]

paths =[['8,15|8,19', ['N->E', '22,25|15,25']],['9,15|9,19', ['N->S1', '8,31|8,26']],['10,15|10,19', ['N->S2', '9,31|9,26']],['11,15|11,19', ['N->E', '22,25|15,25']],['22,20|15,20', ['E->N1', '14,15|14,19']],['22,21|15,21', ['E->N2', '13,15|13,19']],['22,22|15,22', ['E->W', '0,21|7,21'], ['E->S', '9,31|9,26']],['0,23|7,23', ['W->N', '13,15|13,19']],['0,24|7,24', ['W->E', '22,25|15,25']],['0,25|7,25', ['W->S', '8,31|8,26']],['11,31|11,26', ['S->W',  '0,21|7,21']],['12,31|12,26', ['S->N1', '13,15|13,19']],['13,31|13,26', ['S->N2', '14,15|14,19']],['14,31|14,26', ['S->E', '22,25|15,25']],]
