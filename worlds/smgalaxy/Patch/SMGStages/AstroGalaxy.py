from enum import StrEnum
from typing import NamedTuple

from ..extensions import RARCExtended

ASTRO_GALAXY_RELATIVE_PATH: str = "/DATA/files/StageData/AstroGalaxy.arc"
ASTRO_DOME_ENTRANCE_NAME: str = "AstroDomeEntrance"

COMMON_PATH: str = "jmp/placement/common"
LAYERA_PATH: str = "jmp/placement/layera"
LAYERB_PATH: str = "jmp/placement/layerb"
FILE_NAME: str = "objinfo"

class ObjInfoFieldNames(StrEnum):
    NAME: str = "name"
    L_ID: str = "l_id"
    OBJECT_ARGUMENT0: str = "Obj_arg0"
    OBJECT_ARGUMENT1: str = "Obj_arg1"
    OBJECT_ARGUMENT2: str = "Obj_arg2"
    OBJECT_ARGUMENT3: str = "Obj_arg3"
    OBJECT_ARGUMENT4: str = "Obj_arg4"
    OBJECT_ARGUMENT5: str = "Obj_arg5"
    OBJECT_ARGUMENT6: str = "Obj_arg6"
    OBJECT_ARGUMENT7: str = "Obj_arg7"
    CAMERA_SET_ID: str = "CameraSetId"
    SWITCH_APPEAR: str = "SW_APPEAR"
    SWITCH_DEAD: str = "SW_DEAD"
    SWITCH_A: str = "SW_A"
    SWITCH_B: str = "SW_B"
    SWITCH_SLEEP: str = "SW_SLEEP"
    MESSAGE_ID: str = "MessageId"
    POSITION_X: str = "pos_x"
    POSITION_Y: str = "pos_y"
    POSITION_Z: str = "pos_z"
    DIRECTION_X: str = "dir_x"
    DIRECTION_Y: str = "dir_y"
    DIRECTION_Z: str = "dir_z"
    SCALE_X: str = "scale_x"
    SCALE_Y: str = "scale_y"
    SCALE_Z: str = "scale_z"
    CAST_ID: str = "CastId"
    VIEW_GROUP_ID: str = "ViewGroupId"
    SHAPE_MODEL_NUMBER: str = "ShapeModelNo"
    COMMON_PATH_ID: str = "CommonPath_ID"
    CLIPPING_GROUP_ID: str = "ClippingGroupId"
    GROUP_ID: str = "GroupId"
    DEMO_GROUP_ID: str = "DemoGroupId"
    MAP_PARTS_ID: str = "MapParts_ID"

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int
    orbit_index: int
    old_luma_name: str

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
        self.obj_arg0_index = self.objinfo.get_field_index(ObjInfoFieldNames.OBJECT_ARGUMENT0)
    
    def is_valid_shuffle(self, dome_shuffle: dict[int, int]) -> bool:
        """Validate that the dome shuffle mapping contains all indices 1-6 as both keys and values."""
        for index in range(1,7):
            if index not in dome_shuffle.keys() or index not in dome_shuffle.values():
                return False
        return True
    
    def shuffle_domes(self, shuffle: dict[int, int]) -> None:
        """
        Shuffle the visual dome entrances within the observatory. The shuffle maps the old dome index to the new dome index (from 1 to 6).
        The shuffle dict must contain all indices from 1 to 6 as both keys and values. The information to load the dome is contained in
        jmp/placement/common/objinfo. Field "obj_arg0" determines which dome it should load and gets set according to the shuffle dict.
        shuffle:
            key: old dome index (1-6)
            value: new dome index (1-6)
        """
        # Make sure its a valid shuffle
        if not self.is_valid_shuffle(shuffle):
            raise ValueError(f"Invalid shuffle: {shuffle}")

        dome_entrances: dict[int, int] = {}

        # Get all the obj_arg0 of each dome
        for entry_index in range(self.objinfo.entry_count):
            if self.objinfo.get_value_by_index(entry_index, self.name_index) == ASTRO_DOME_ENTRANCE_NAME:
                dome_index = self.objinfo.get_value_by_index(entry_index, self.obj_arg0_index)
                dome_entrances[dome_index] = entry_index

        print("Shuffling domes...")
        
        # Set all the new obj_arg0 of each dome
        for old_dome_index, entry_index in dome_entrances.items():
            new_dome_index = shuffle[old_dome_index]

            print(f"Dome {old_dome_index} -> Dome {new_dome_index}")
            
            self.objinfo.set_value_by_index(entry_index, self.obj_arg0_index, new_dome_index)
    
    def shuffle_lumas(self, new_galaxies: list[GalaxyDestination]) -> None:
        """
        Shuffle the lumas within the observatory. The list of new galaxies is expected to all have type "luma". The old luma name
        is used to determine which name to replace with the name. The old luma names are not checked for duplicates.
        """
        # Convert to a dict for easy lookup
        new_galaxies_dict: dict[str, str] = {galaxy.old_luma_name: galaxy.name for galaxy in new_galaxies}
        
        def rename_bcsv_entries(bcsv):
            for entry_index in range(bcsv.entry_count):
                entry_name: str = bcsv.get_value_by_index(entry_index, self.name_index)

                if entry_name.startswith("Surp"):
                    entry_name = entry_name[4:]

                    if entry_name in new_galaxies_dict.keys():
                        new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                        print(f"Luma Surp{entry_name} -> {new_entry_name}")

                        bcsv.set_value_by_index(entry_index, self.name_index, new_entry_name)
            
            return bcsv

        # Check the objinfos for the luma galaxies
        self.objinfo = rename_bcsv_entries(self.objinfo)
        self.objinfo_layera = rename_bcsv_entries(self.objinfo_layera)
        self.objinfo_layerb = rename_bcsv_entries(self.objinfo_layerb)

    def save_objinfo(self) -> None:
        self.objinfo.save_changes()
        self.objinfo_layera.save_changes()
        self.objinfo_layerb.save_changes()
