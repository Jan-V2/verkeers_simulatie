maps = ["kruispunt3.txt"]
spaces = 1
seperator = ","

for map_file in maps:
    ret = ""
    with open(map_file, "r") as file:
        char_map = file.read().split("\n")
        # ruimt lege regel aan het einde van het bestand op
        if char_map[len(char_map) - 1] == "":
            char_map = char_map[:len(char_map) - 1]

    addition = ""
    for i in range(spaces):
        addition += " "
    addition += seperator

    for row in char_map:
        for char in row:
            ret += char + addition
        ret += "\n"

    if ret[len(ret) - 1] == "":
        ret = ret[:len(ret) - 1]

    with open("kruispunt3_new.txt", "w") as file:
        file.write(ret)