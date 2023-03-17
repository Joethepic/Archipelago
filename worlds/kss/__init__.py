import string
from typing import Optional
from .items import all_items, KSSItems
from .locations import location_table, KSSLocation
from .options import kss_options, Goldgoal
from .Rules import set_rules
from .regions import create_regions
from BaseClasses import Item, Tutorial, ItemClassification, Region, Location, RegionType, Entrance, MultiWorld  
from ..AutoWorld import World, WebWorld

client_version = 1


class KSSWeb(WebWorld):
    theme = "party" #placeholder TODO: pick theme best for the game
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Kirby Super Star for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["squidy"]
    )]


class SuperMarioGalaxy(World):
    # TODO: write game info 
    """
    """

    game: str = "Kirby Super Star"
    topology_present = False
    item_name_to_id = all_items
    location_name_to_id = location_table
    
    web = KSSWeb()

    data_version = 0
    required_client_version = (0, 3, 10)
    option_definitions = kss_options

    def create_regions(self):
        create_regions(self.multiworld, self.player, self)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self)
    
    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "Ability":
            classification = ItemClassification.progression
        else: 
            classification = ItemClassification.filler
        item = KSSItem(name, classification, item_id, self.player)
        
        return item
    
    def generate_basic(self): 
        self.multiworld.get_location("B: Bowser's Galaxy Reactor", self.player).place_locked_item(self.create_item("Victory"))
