import string
from .items import item_table, SMGItem
from .locations import location_table, SMGLocation
from .Options import smg_options
from .rules import set_star_rules
from .regions import create_regions
from BaseClasses import Item, Tutorial, ItemClassification, Region, Location, RegionType, Entrance, MultiWorld  
from ..AutoWorld import World, WebWorld

client_version = 1


class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SMG for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["squidy"]
    )]
class SuperMarioGalaxy(World):
    """
    Super Mario Galaxy allows you to explore the cosomos with rosalinna in the comet obserbatory. 
    Mario must collect Power Stars and Grand Stars to power the obserbatory so it can go to the 
    center of the universe in order to save peach.
    """
    
    game: str = "Super Mario Galaxy"
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table
    
    data_version = 1
    forced_auto_forfeit = False

    options = smg_options

    def create_regions(self):
        create_regions(self.world,self.player, location_table)
    
    def set_star_rules(self):
        set_star_rules(self.world,self.player)
    
    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "Power Star":
            classification = ItemClassification.progression_skip_balancing
        else:
            classification = ItemClassification.progression
        item = SMGItem(name, True, item_id, self.player)
        
        return item
   
    
    def generate_basic(self, player): 
        gstaritem = self.create_item("Green Star")
        self.world.itempool += [gstaritem for i in range(0,3)]
        
        staritem = self.create_item("Power Star")
        if(self.world.enable_purple_coin_stars.value == 1 [self.player]):
           self.world.itempool += [staritem for i in range(0,117)]
        
        elif self.world.enable_purple_coin_stars.value == 0 [self.player]:
            self.world.itempool += [staritem for i in range(0,118)]
        
        else:
            self.world.itempool += [staritem for i in range(0,101)]
        
        grandstar1 = self.create_item("Grand Star Terrace")   
        grandstar2 = self.create_item("Grand Star Fountain")  
        grandstar3 = self.create_item("Grand Star Kitchen")
        grandstar4 = self.create_item("Grand Star Bedroom")
        grandstar5 = self.create_item("Grand Star Engine Room")          
        self.world.itempool += [grandstar1,grandstar2,grandstar3,grandstar4,grandstar5]    
