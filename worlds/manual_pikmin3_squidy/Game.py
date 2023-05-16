from .Data import game_table

game_name = "Manual_%s_%s" % (game_table["game"], game_table["player"])
filler_item_name = game_table["filler_item_name"]

# Programmatically generate starting indexes for items and locations based upon the game name and player name to aim for non-colliding indexes
starting_index = (ord(game_table["game"][:1]) * 1000000) + \
    (ord(game_table["game"][1:2]) * 100000) + \
    (ord(game_table["game"][2:3]) * 100000) + \
    (ord(game_table["game"][3:4]) * 100000) + \
    (ord(game_table["game"][4:5]) * 100000) + \
    (ord(game_table["game"][-1:]) * 100000) + \
    (ord(game_table["player"][:1]) * 10000) + \
    (ord(game_table["player"][1:2]) * 10000) + \
    (ord(game_table["player"][-1:]) * 1000)
