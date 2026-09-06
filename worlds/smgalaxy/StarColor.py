from SMGClient import Pointer
from typing import NamedTuple
from .Constants.constants import *
from .Constants.Names.item_names import *
from .Constants.ram_constants import *
from locations import location_table, SMGLocationData
class StarColor(NamedTuple):
    name: str
    pointer: Pointer

class StarColorHandler:
    pointers: dict[str, Pointer]
    star_colors: list[StarColor] = []
    initialised: bool

    def __init__(self, pointers: dict[str, Pointer]):
        self.star_colors = []
        self.pointers = pointers
        self.initialised = False

    def set_star_colors(self, galaxyName: str, starNum: int):
        for star in self.star_colors:
            if star.name == galaxyName + "Colours" + str(starNum):
                star.pointer.write_value(PowerStarColorEnum.GREEN)

    def init_all_star_colors(self):
        if self.initialised == True:
            return 
        
        self.star_colors = []
        for location in location_table.values():
            starname = self.get_pointer_name(location)
            star_color = StarColor(starname, self.pointers[starname])
            self.star_colors.append(star_color)
        
        self.initialised = True

    def get_pointer_name(self, location: SMGLocationData):
        return location.in_game_galaxy_name + "Colours" + str(location.game_address)
  