from io import BytesIO

from wiithon.formats.bcsv import BCSV, BCSVField, calculate_field_hash, BCSVType, BCSVEntry
from wiithon.formats.rarc import Rarc
from wiithon.formats.yaz0 import Yaz0

from ..extensions import SMGObject
from ...Constants.patch_constants import *
from ...Constants.constants import *

keys = ["name", "new_name", "type", "unlock", "radius", "angle",
        "address", "port"]
hash_dict = {key: calculate_field_hash(key) for key in keys}

class PatchFile(SMGObject):
    arc_file: Rarc

    def __init__(self):
        super().__init__("/Archipelago/Patch.arc")

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

    def update(self, galaxy_shuffle: list[GalaxyDestination], star_requirements: dict[str, int], **kwargs):
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1, 7)}

        for location, requirement in star_requirements.items():
            dome_index = int(location[1])
            orbit_index = int(location[3])

            requirements[dome_index][orbit_index] = requirement
        
        fields: list[BCSVField] = [
            BCSVField(hash_dict["name"], 0xFFFFFFFF, 16, 0, BCSVType.STRING_OFFSET),
            BCSVField(hash_dict["new_name"], 0xFFFFFFFF, 20, 0, BCSVType.STRING_OFFSET),
            BCSVField(hash_dict["type"], 0xFFFFFFFF, 8, 0, BCSVType.LONG),
            BCSVField(hash_dict["unlock"], 0xFFFFFFFF, 12, 0, BCSVType.LONG),
            BCSVField(hash_dict["radius"], 0xFFFFFFFF, 0, 0, BCSVType.FLOAT),
            BCSVField(hash_dict["angle"], 0xFFFFFFFF, 4, 0, BCSVType.FLOAT),
        ]

        mini_bcsv = BCSV(fields)

        for galaxy in galaxy_shuffle:
            entry: BCSVEntry = BCSVEntry()
            entry[hash_dict["name"]] = "Mini" + galaxy.patch_test_old_name
            entry[hash_dict["new_name"]] = "Mini" + galaxy.patch_test_new_name

            if galaxy.patch_test_new_name in self.major_galaxy_list:
                galaxy_type = 0
            elif galaxy.patch_test_new_name in self.minor_galaxy_list + self.special_galaxy_list:
                galaxy_type = 1
            elif galaxy.patch_test_new_name in self.boss_galaxy_list:
                galaxy_type = 2
            
            entry[hash_dict["type"]] = galaxy_type
            entry[hash_dict["unlock"]] = requirements[galaxy.dome_index][galaxy.orbit_index + 1]
            entry[hash_dict["radius"]] = (galaxy.orbit_index + 2) * 2000.0
            entry[hash_dict["angle"]] = galaxy.orbit_index * 230.0 % 360.0
            print(entry)
            mini_bcsv.add_bcsv_entry(entry)

        bowser_entry = BCSVEntry()
        bowser_entry[hash_dict["name"]] = "MiniKoopaBattleVs3Galaxy"
        bowser_entry[hash_dict["new_name"]] = "MiniKoopaBattleVs3Galaxy"
        bowser_entry[hash_dict["type"]] = 2
        bowser_entry[hash_dict["unlock"]] = 60 # TODO: goal
        bowser_entry[hash_dict["radius"]] = 0.0
        bowser_entry[hash_dict["angle"]] = 0.0

        mini_bcsv.add_bcsv_entry(entry)

        network_bcsv = BCSV()
        network_bcsv.add_bcsv_field(BCSVField(hash_dict["address"], 0xFFFFFFFF, 0, 0, BCSVType.UNSIGNED_LONG))
        network_bcsv.add_bcsv_field(BCSVField(hash_dict["port"], 0xFFFFFFFF, 4, 0, BCSVType.UNSIGNED_LONG))

        network_entry = BCSVEntry()
        network_entry[hash_dict["address"]] = 0xC0A8A1D1 # temporary (is 192.168.161.209)
        network_entry[hash_dict["port"]] = 0x4150 # temporary (is 'AP')

        arc_file = Rarc.create_empty()

        stream = BytesIO()
        mini_bcsv.write(stream)

        arc_file.add_file("Patch.bcsv", stream.getvalue())
        self.patcher.add_file(self.path, arc_file.get_bytes())
