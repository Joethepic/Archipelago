from wiithon import WiiIsoPatcher
from wiithon.formats.bcsv import BCSV

from worlds.smgalaxy.Patch import hashtable

from ...Constants.patch_constants import *
from ..extensions import SMGObject
from ..SMGObjects.SurprisedGalaxy import SurprisedGalaxy
from ..SMGObjects.Gateway import Gateway
from ...Constants.Names.region_names import GATEWAY
from ...regions import region_list

class AstroDomes(SMGObject):
    def __init__(self):
        super().__init__(ASTRO_DOME_PATH)

        self.surprised_galaxy: SurprisedGalaxy = SurprisedGalaxy(self.patcher)
        self.gateway_galaxy: Gateway = Gateway(self.patcher)

        # Get the in-game names from the region list
        self.major_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                             if data.type == "Major"]
        self.minor_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                             if data.type == "Minor"]
        self.boss_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                            if data.type == "Boss"]
        self.special_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                      if data.type == "Special"]
        self.gateway: str = region_list[GATEWAY].in_game_name

    def update(self, galaxy_shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int], **kwargs):
        for index in range(1, 7):
            self.update_dome([galaxy for galaxy in galaxy_shuffle if galaxy.dome_index == index], index, dome_shuffle[index])

    def update_dome(self, new_galaxies: list[GalaxyDestination], dome_index: int, interior_dome_index: int, show_galaxies: int):
        """
        Update the dome with new galaxies. The dome to update is determined by the dome index (from 1 to 6). The list of new galaxies
        is expected to all have type "dome" and contain all the galaxies that should be in the dome. The dome index of the new galaxies
        are ignored and should be used to determine the list to input in this function. The orbit index of the new galaxies is not
        checked for duplicates. Creates mini gateway and surprised galaxies if necessary. Interior dome index determines what the inside
        of the dome should look like in correspondance with the given index.
        """
        # Get the objinfo path of the dome corresponding to the dome index.
        OBJINFO_PATH = PLACEMENT_PATH + index_to_layer[dome_index] + '/' + FILE_NAME

        galaxy_index = 0
        with self.patcher.edit_as(self.path + '/' + OBJINFO_PATH, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis") as bcsv:
            for entry in bcsv.entries:
                if entry["name"].startswith("Mini"):
                    galaxy: GalaxyDestination = new_galaxies[galaxy_index]
                    galaxy_index += 1

                    # Set the new name
                    entry["name"] = "Mini" + galaxy.name

                    # Store the orbit index in the upper bits
                    obj_arg0 = galaxy.orbit_index << 16
    
                    # Store the galaxy type in the lower bits
                    if galaxy.name in self.major_galaxy_list:
                        if show_galaxies == 2:
                            obj_arg0 += 1
                        else:
                            obj_arg0 += 0
                    elif galaxy.name in self.minor_galaxy_list or galaxy.name in self.special_galaxy_list:
                        obj_arg0 += 1
    
                        if galaxy.name == self.gateway:
                            self.gateway_galaxy.create_miniature()
                        elif galaxy.name in self.special_galaxy_list:
                            self.surprised_galaxy.create_luma_miniature("Mini" + galaxy.name)
                    elif galaxy.name in self.boss_galaxy_list:
                        if show_galaxies == 2:
                            obj_arg0 += 1
                        else:
                            obj_arg0 += 2

                    entry["Obj_arg0"] = obj_arg0

                if entry["name"].startswith("AstroDome"):
                    entry["Obj_arg0"] = interior_dome_index
