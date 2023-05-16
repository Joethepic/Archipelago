import json
import os
import pkgutil

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

game_table = load_data_file('game.json')
item_table = load_data_file('items.json')
#progressive_item_table = load_data_file('progressive_items.json')
progressive_item_table = {}
location_table = load_data_file('locations.json')
region_table = load_data_file('regions.json')
