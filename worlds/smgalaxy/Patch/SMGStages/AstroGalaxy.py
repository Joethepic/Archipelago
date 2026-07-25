from wiithon import WiiIsoPatcher
from wiithon.file_helper.bcsv import BCSV

from worlds.smgalaxy.Patch import hashtable

from ...Constants.patch_constants import *
from ..extensions import RARCExtended, SMGObject


class AstroGalaxy(SMGObject):
    def __init__(self, patcher: WiiIsoPatcher):
        super().__init__(patcher, ASTRO_GALAXY_PATH)
    
    def update(self, new_galaxies: list[GalaxyDestination]) -> None:
        self.shuffle_lumas(new_galaxies)

    def shuffle_lumas(self, new_galaxies: list[GalaxyDestination]) -> None:
        """
        Shuffle the lumas within the observatory. The list of new galaxies is expected to all have type "luma". The old luma name
        is used to determine which name to replace with the name. The old luma names are not checked for duplicates.
        """
        # Convert to a dict for easy lookup
        new_galaxies_dict: dict[str, str] = {galaxy.old_luma_name: galaxy.name for galaxy in new_galaxies}

        def edit_objinfo(path: str):
            bcsv: BCSV
            with self.patcher.edit_as(path, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis") as bcsv:
                for entry in bcsv.entries:
                    entry_name: str = entry["name"]

                    if not entry_name.startswith("Surp"):
                        continue
                
                    entry_name = entry_name[4:]

                    if entry_name not in new_galaxies_dict.keys():
                        continue
                
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    entry["name"] = new_entry_name

        edit_objinfo(self.path + COMMON_PATH + FILE_NAME)
        edit_objinfo(self.path + LAYERA_PATH + FILE_NAME)
        edit_objinfo(self.path + LAYERB_PATH + FILE_NAME)
