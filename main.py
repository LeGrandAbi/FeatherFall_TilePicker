import random
import json

CONFIG = "base_jdb"

EXIT_COMMANDS = ["q", "quit", "x", "exit"]
REROLL_COMMANDS = ["r", "reroll"]

def what_to_do_with_the_chosen_tile(tile):
	print('\t' + tile.upper())
	

with open(f"configs/{CONFIG}.json", 'r', ) as f:
	config = json.load(f)
	f.close()

stack = []
for name, value in config:
	for i in range(value):
		stack.append(name)

random.shuffle(stack)

prompt = ""
sidestack = []
length = len(stack)
while ((stack != []) and (not prompt in EXIT_COMMANDS)):
	t = stack.pop()
	what_to_do_with_the_chosen_tile(t)
	quantity = f"{len(stack)}{f"+{len(sidestack)}" if len(sidestack)!=0 else ""}/{length} tiles left "
	prompt = input(quantity + "[enter to continue] [q  to quit] [r to reroll] :").lower()

	if prompt in REROLL_COMMANDS:
		sidestack.append(t)
	else:
		while sidestack != []:
			stack.append(sidestack.pop(0))