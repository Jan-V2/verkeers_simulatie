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

    generate_sensor_nodes(sensors)
    #generate_path_nodes(route_components, 4)
    print("done")
