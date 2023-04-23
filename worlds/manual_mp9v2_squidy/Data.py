import json
import os
import pkgutil

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())

game_table = load_data_file('game.json')
item_table = load_data_file('items.json')
#progressive_item_table = load_data_file('progressive_items.json')
progressive_item_table = {}
location_table = load_data_file('locations.json')
