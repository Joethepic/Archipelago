from .Data import item_table, progressive_item_table, location_table
from .Game import game_name, filler_item_name
from .Locations import location_id_to_name, location_name_to_id, location_name_to_location
from .Items import item_id_to_name, item_name_to_id, item_name_to_item, advancement_item_names

from .Regions import create_regions
from .Items import ManualItem
from .Rules import set_rules
from .Options import get_option_value, manual_options

from BaseClasses import ItemClassification, Tutorial, Item
from ..AutoWorld import World, WebWorld


class ManualWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up manual game integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Fuzzy"]
    )]


class ManualWorld(World):
    """
    Manual games allow you to set custom check locations and custom item names that will be rolled into a multiworld.
    This allows any variety of game -- PC, console, board games, Microsoft Word memes... really anything -- to be part of a multiworld randomizer.
    The key component to including these games is some level of manual restriction. Since the items are not actually withheld from the player, 
    the player must manually refrain from using these gathered items until the tracker shows that they have been acquired or sent.
    """
    game: str = game_name
    web = ManualWeb()

    option_definitions = manual_options
    data_version = 2
    required_client_version = (0, 3, 4)

    # These properties are set from the imports of the same name above.
    item_table = item_table
    progressive_item_table = progressive_item_table
    item_id_to_name = item_id_to_name
    item_name_to_id = item_name_to_id
    item_name_to_item = item_name_to_item
    advancement_item_names = advancement_item_names
    location_table = location_table
    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id
    location_name_to_location = location_name_to_location

    def pre_fill(self):
        location_game_complete = self.multiworld.get_location("__Manual Game Complete__", self.player)
        location_game_complete.address = None

        location_game_complete.place_locked_item(
            ManualItem("__Victory__", ItemClassification.progression, None, player=self.player))

    def generate_basic(self):
        # Generate item pool
        pool = []
        configured_item_names = self.item_id_to_name.copy()

        for name in configured_item_names.values():
            if name == "__Victory__":
                continue

            # If it's the filler item, skip it until we know if we need any extra items
            if name == filler_item_name:
                continue

            # if (hasattr(self.multiworld, "progressive_items") and len(self.multiworld.progressive_items) > 0):
            #     shouldUseProgressive = (self.multiworld.progressive_items[self.player].value);

            #     if shouldUseProgressive and name in self.progressive_item_table:
            #         name = self.progressive_item_table[name]

            item = self.item_name_to_item[name]
            item_count = 1

            if "count" in item:
                item_count = int(item["count"])

            for i in range(item_count):
                new_item = self.create_item(name)
                pool.append(new_item)
                

        extras = len(location_table) - len(pool) - 1 # subtracting 1 because of Victory; seems right

        if extras > 0:
            for i in range(0, extras):
                extra_item = self.create_item(filler_item_name)
                pool.append(extra_item)

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item = self.item_name_to_item[name]
        classification = ItemClassification.filler

        if "trap" in item and item["trap"]:
            classification = ItemClassification.trap

        if "useful" in item and item["useful"]:
            classification = ItemClassification.useful

        if "progression" in item and item["progression"]:
            classification = ItemClassification.progression

        return ManualItem(name, classification,
                        self.item_name_to_id[name], player=self.player)

    def set_rules(self):
        set_rules(self, self.multiworld, self.player)

    def create_regions(self):
        create_regions(self, self.multiworld, self.player)
    
    def get_pre_fill_items(self):
        return []
    
    def fill_slot_data(self):
        # return {
        #     "DeathLink": bool(self.multiworld.death_link[self.player].value)
        # }

        pass
