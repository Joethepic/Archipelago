from enum import StrEnum
from typing import NamedTuple

from ..extensions import RARCExtended
from ..bcsv import BCSV

ASTRO_GALAXY_RELATIVE_PATH: str = "/DATA/files/StageData/AstroGalaxy.arc"
ASTRO_DOME_ENTRANCE_NAME: str = "AstroDomeEntrance"

COMMON_PATH: str = "jmp/placement/common"

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

class AstroGalaxy(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRO_GALAXY_RELATIVE_PATH
        super().__init__()

        # Get the common objinfo bcsv
        for file in self.get_node_by_path(COMMON_PATH).files:
            if file.name == 'objinfo':
                self.objinfo = BCSV(file)
        
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
            
        self.objinfo.save_changes()
