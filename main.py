import sys
import subprocess
import json
import random


def place(tile):
    tilepath = f"tiles/{tile}.png"
    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', tilepath], check=True)
    return input("")

def place_from_stack(stack):
    if stack != []:
        i = random.randint(0, len(stack)-1)
        tile = stack.pop(i)

        print(f"placez {tile.upper()} ({len(stack)} left)")
        prompt = place(tile)

        if prompt.lower() == "n":
            place_from_stack(stack)
            stack.append(tile)

config_name = sys.argv[1]
config_path = f"configs/{config_name}.json"

with open(config_path, 'r') as f:
    config = json.load(f)
    f.close()

stacks = {}
for stack_name, tileset in config["stacks"].items():
    stack = []
    for tile, amount in tileset.items():
        for i in range(amount):
            stack.append(tile)
    stacks[stack_name] = stack

for instruction in config["instructions"]:
    command = instruction["command"]
    args = instruction["args"]
    print(f"========= {command.upper()} ===========")
    match command:

        case "place":
            stack = args["stack"]
            n = args["n"]
            i = 0
            while i != n:
                place_from_stack(stacks[stack])
                i += 1

        case "place_all":
            stack = args["stack"]
            while stacks[stack] != []:
                place_from_stack(stacks[stack])

        case "place_corner":
            stack = args["stack"]
            n = args["n"]
            corner = args["corner"]

            print(f"placez la prochaine tuile sur la position la plus au {corner.upper()} de la carte")
            i = 0
            while i != n:
                place_from_stack(stacks[stack])
                i += 1

        case "place_ville":
            print("placez la ville au centre de la carte")
            place("graan_holtgard")

        case "place_village":
            village = args["village"]
            print(f"placez le village {village}")
            place(village)

        case "place_village_corner":
            village = args["village"]
            corner = args["corner"]
            print(f"placez le village {village} sur la position la plus {corner.upper()} de la carte")
            place(village)

        case "place_village_biome":
            village = args["village"]
            biome = args["biome"]
            print(f"placez le village {village} n'importe quelle position adjacente a une tuile {biome}")
            place(village)

        case _:
            raise ValueError(f"Incorrect command given : \"{instruction}\"")