from typing import NamedTuple

from ..bcsv import BCSV
from ..extensions import RARCExtended
from ..SMGObjects.SurprisedGalaxy import SurprisedGalaxy
from ..SMGObjects.Gateway import Gateway
from ...Constants.Names.region_names import GATEWAY
from ...regions import major_galaxy_list, minor_galaxy_list, specials_galaxy_list, boss_galaxy_list, all_galaxy_slots, region_list

ASTRODOME_RELATIVE_PATH = "/DATA/files/StageData/AstroDome.arc"

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int
    orbit_index: int

index_to_layer = {1: 'layera',
                  2: 'layerb',
                  3: 'layerc',
                  4: 'layerd',
                  5: 'layere',
                  6: 'layerf'}

class AstroDome(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRODOME_RELATIVE_PATH
        super().__init__()

        self.surprised_galaxy: SurprisedGalaxy = SurprisedGalaxy()
        self.gateway_galaxy: Gateway = Gateway()

    def create_luma_miniature(self, name: str):
        self.surprised_galaxy.create_luma_miniature(name)

    def create_gateway_miniature(self):
        self.gateway_galaxy.create_miniature()

    def update_dome(self, new_galaxies: list[GalaxyDestination], dome_index: int):
        layer = index_to_layer[dome_index]
        objinfo = next((BCSV(file) for file in self.get_node_by_path(f"jmp/placement/{layer}").files if file.name == "objinfo"), None)
        
        name_index = objinfo.get_field_index("name")
        objarg0_index = objinfo.get_field_index('Obj_arg0')
        miniature_indices = []

        for entry_index in range(objinfo.entry_count):
            name = objinfo.get_value_by_index(entry_index, name_index)
            if name.startswith("Mini"):
                miniature_indices.append(entry_index)

        luma_miniatures  = []
        index = 0
        for galaxy in new_galaxies:
            entry_index = miniature_indices[index]
            index += 1

            print(f"Dome {dome_index} orbit {galaxy.orbit_index + 1} -> {galaxy.name}")

            name = "Mini" + region_list[galaxy.name].in_game_name
            objinfo.set_value_by_index(entry_index, name_index, name)
            
            obj_arg0 = galaxy.orbit_index << 16

            if galaxy.name in major_galaxy_list:
                obj_arg0 += 0
            elif galaxy.name in minor_galaxy_list or galaxy.name in specials_galaxy_list:
                obj_arg0 += 1
            elif galaxy.name in boss_galaxy_list:
                obj_arg0 += 2

            objinfo.set_value_by_index(entry_index, objarg0_index, obj_arg0)

            if galaxy.name == GATEWAY:
                self.create_gateway_miniature()
            elif galaxy.name in specials_galaxy_list:
                self.create_luma_miniature(name)

        objinfo.save_changes()
