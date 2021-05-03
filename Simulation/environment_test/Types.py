from enum import Enum


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