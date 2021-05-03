# todo specify road with north/south road, and combine merge splits

from environment_test.Coord import Coord
from environment_test.Route_Components import *
from environment_test.Crossing import Crossing
from environment_test.Types import *

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
    print("done")
