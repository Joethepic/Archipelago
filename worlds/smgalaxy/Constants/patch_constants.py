from enum import IntEnum, StrEnum
from typing import NamedTuple

from .Names.region_names import GATEWAY
from ..regions import region_list

# PATHS
ASTRO_DOME_ENTRANCE_PATH = "ObjectData/AstroDomeEntrance{0}.arc"
OBJECT_DATA_PATH = "ObjectData/"
GATEWAY_PATH: str = "ObjectData/AstroChildRoom.arc"
MARIO_PATH = "ObjectData/Mario.arc"
OBJECT_DATA_PATH = "ObjectData/"
SURPRISED_GALAXY_PATH = "ObjectData/MiniSurprisedGalaxy.arc"
ASTRODOME_PATH = "StageData/AstroDome.arc"
ASTRO_DOME_SCENARIO_PATH = "StageData/AstroDome/AstroDomeScenario.arc"
ASTRO_GALAXY_PATH: str = "StageData/AstroGalaxy.arc"
DOL_PATH: str = "/DATA/sys/main.dol"

# ASTRODOMEENTRANCES
DOMES: dict[int, str] = {1: "Observatory",
                         2: "Well",
                         3: "Kitchen",
                         4: "BedRoom",
                         5: "Machine",
                         6: "Tower"}

class Domes(IntEnum):
    TERRACE = 1
    FOUNTAIN = 2
    KITCHEN = 3
    BEDROOM = 4
    ENGINE = 5
    GARDEN = 6

# GATEWAY
MINIATURE_GATEWAY_NAME: str = "MiniHeavensDoorGalaxy"

# MARIO
WHITE = (255, 255, 255)
OLD_CAP_COLOUR = (181, 0, 0)
OLD_GLOVES_COLOUR = (153, 153, 153)

# ASTRODOME
PLACEMENT_PATH = "Stage/jmp/placement/"
FILE_NAME = "objinfo"

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

index_to_layer = {1: 'layera',
                  2: 'layerb',
                  3: 'layerc',
                  4: 'layerd',
                  5: 'layere',
                  6: 'layerf'}

# ASTRODOMESCENARIO
SCENARIO_DATA_FILE_NAME = "AstroDomeScenario/ScenarioData.bcsv"

class ScenarioDataFieldName(StrEnum):
    SCENARIO_NUMBER: str = "ScenarioNo"
    SCENARIO_NAME: str = "ScenarioName"
    POWER_STAR_ID: str = "PowerStarId"
    APPEAR_POWER_STAR_OBJect: str = "AppearPowerStarObj"
    COMET: str = "Comet"
    LUIGI_MODE_TIMER: str = "LuigiModeTimer"
    ASTRO_DOME: str = "AstroDome"
    IS_HIDDEN: str = "IsHidden"
    ERROR_CHECK: str = "ErrorCheck"

# ASTROGALAXY
ASTRO_DOME_ENTRANCE_NAME: str = "AstroDomeEntrance"

COMMON_PATH: str = "Stage/jmp/placement/common/"
LAYERA_PATH: str = "Stage/jmp/placement/layera/"
LAYERB_PATH: str = "Stage/jmp/placement/layerb/"
FILE_NAME: str = "objinfo"

# SMGDOL
GATEWAY_IN_GAME: str = region_list[GATEWAY].in_game_name

NAME_TO_CREATE_FUNCTION_START_ADDRESS = 0x80533980
NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT = 1183
NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE = 0xC

NAME_TO_ARCHIVE_START_ADDRESS = 0x805370f4
NAME_TO_ARCHIVE_ELEMENT_COUNT = 440
NAME_TO_ARCHIVE_ELEMENT_SIZE = 0x8

NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS = 0x80537eb4
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT = 91
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE = 0x8

GALAXY_UNLOCK_TABLE_START_ADDRESS = 0x8053c800
GALAXY_UNLOCK_TABLE_END_ADDRESS = 0x8053d520

CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS = 0x8026a8cc
CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS = 0x8026a90c
STRING_ADDRESS_MINISURPRISEDGALAXY = 0x8059838c

ASTRO_DOME_ARRAY_ADDRESS = 0x8057a9e0
ASTRO_DOME_SKY_ARRAY_ADDRESS = 0x8057aa24
ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS = 0x8057aad4
ASTRO_STAR_PLATE_ARRAY_ADDRESS = 0x8057ab70
