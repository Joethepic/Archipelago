from ...Constants.patch_constants import *
from ..extensions import RARCExtended

class AstroGalaxy(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRO_GALAXY_RELATIVE_PATH
        super().__init__()

        # Get the objinfo bcsvs
        self.objinfo = self.get_bcsv_file(COMMON_PATH, FILE_NAME)
        self.objinfo_layera = self.get_bcsv_file(LAYERA_PATH, FILE_NAME)
        self.objinfo_layerb = self.get_bcsv_file(LAYERB_PATH, FILE_NAME)

        # Get the indices of the fields
        self.name_index = self.objinfo.get_field_index(ObjInfoFieldNames.NAME)
    
    def shuffle_lumas(self, new_galaxies: list[GalaxyDestination]) -> None:
        """
        Shuffle the lumas within the observatory. The list of new galaxies is expected to all have type "luma". The old luma name
        is used to determine which name to replace with the name. The old luma names are not checked for duplicates.
        """
        # Convert to a dict for easy lookup
        new_galaxies_dict: dict[str, str] = {galaxy.old_luma_name: galaxy.name for galaxy in new_galaxies}
        
        for entry_index in range(self.objinfo.entry_count):
            entry_name: str = self.objinfo.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo.save_changes()

        for entry_index in range(self.objinfo_layera.entry_count):
            entry_name: str = self.objinfo_layera.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo_layera.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo_layera.save_changes()

        for entry_index in range(self.objinfo_layerb.entry_count):
            entry_name: str = self.objinfo_layerb.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo_layerb.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo_layerb.save_changes()
