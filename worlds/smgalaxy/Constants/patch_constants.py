from enum import IntEnum, StrEnum
from typing import NamedTuple

from .Names.region_names import GATEWAY
from ..regions import region_list

# PATHS
ASTRO_DOME_ENTRANCE_PATH = "/ObjectData/AstroDomeEntrance{0}.arc"
OBJECT_DATA_PATH = "/ObjectData/"
GATEWAY_PATH: str = "/ObjectData/AstroChildRoom.arc"
GATEWAY_BDL_NAME = "astrochildroom.bdl"
MARIO_PATH = "/ObjectData/Mario.arc"
SURPRISED_GALAXY_PATH = "/ObjectData/MiniSurprisedGalaxy.arc"
ASTRODOME_PATH = "/StageData/AstroDome.arc"
ASTRO_DOME_SCENARIO_PATH = "/StageData/AstroDome/AstroDomeScenario.arc"
ASTRO_GALAXY_PATH: str = "/StageData/AstroGalaxy.arc"
DOL_PATH: str = "/DATA/sys/main.dol"

# ASTRODOMEENTRANCES
class Domes(StrEnum):
    TERRACE = "Observatory"
    FOUNTAIN = "Well"
    KITCHEN = "Kitchen"
    BEDROOM = "BedRoom"
    ENGINE = "Machine"
    GARDEN = "Tower"

# GATEWAY
MINIATURE_GATEWAY_NAME: str = "MiniHeavensDoorGalaxy"

# MARIO
WHITE = (255, 255, 255)
OLD_CAP_COLOUR = (181, 0, 0)
OLD_GLOVES_COLOUR = (153, 153, 153)

# ASTRODOME
PLACEMENT_PATH = "/jmp/placement/"
FILE_NAME = "objinfo"

class ObjInfoFieldNames(StrEnum):
    NAME = "name"
    L_ID = "l_id"
    OBJECT_ARGUMENT0 = "Obj_arg0"
    OBJECT_ARGUMENT1 = "Obj_arg1"
    OBJECT_ARGUMENT2 = "Obj_arg2"
    OBJECT_ARGUMENT3 = "Obj_arg3"
    OBJECT_ARGUMENT4 = "Obj_arg4"
    OBJECT_ARGUMENT5 = "Obj_arg5"
    OBJECT_ARGUMENT6 = "Obj_arg6"
    OBJECT_ARGUMENT7 = "Obj_arg7"
    CAMERA_SET_ID = "CameraSetId"
    SWITCH_APPEAR = "SW_APPEAR"
    SWITCH_DEAD = "SW_DEAD"
    SWITCH_A = "SW_A"
    SWITCH_B = "SW_B"
    SWITCH_SLEEP = "SW_SLEEP"
    MESSAGE_ID = "MessageId"
    POSITION_X = "pos_x"
    POSITION_Y = "pos_y"
    POSITION_Z = "pos_z"
    DIRECTION_X = "dir_x"
    DIRECTION_Y = "dir_y"
    DIRECTION_Z = "dir_z"
    SCALE_X = "scale_x"
    SCALE_Y = "scale_y"
    SCALE_Z = "scale_z"
    CAST_ID = "CastId"
    VIEW_GROUP_ID = "ViewGroupId"
    SHAPE_MODEL_NUMBER = "ShapeModelNo"
    COMMON_PATH_ID = "CommonPath_ID"
    CLIPPING_GROUP_ID = "ClippingGroupId"
    GROUP_ID = "GroupId"
    DEMO_GROUP_ID = "DemoGroupId"
    MAP_PARTS_ID = "MapParts_ID"

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
SCENARIO_DATA_FILE_NAME = "/scenariodata.bcsv"

class ScenarioDataFieldName(StrEnum):
    SCENARIO_NUMBER = "ScenarioNo"
    SCENARIO_NAME = "ScenarioName"
    POWER_STAR_ID = "PowerStarId"
    APPEAR_POWER_STAR_OBJect = "AppearPowerStarObj"
    COMET = "Comet"
    LUIGI_MODE_TIMER = "LuigiModeTimer"
    ASTRO_DOME = "AstroDome"
    IS_HIDDEN = "IsHidden"
    ERROR_CHECK = "ErrorCheck"

# ASTROGALAXY
ASTRO_DOME_ENTRANCE_NAME: str = "AstroDomeEntrance"

COMMON_PATH: str = "/jmp/placement/common/" #TODO add stage name root folder once wiithon fixes it.
LAYERA_PATH: str = "/jmp/placement/layera/"
LAYERB_PATH: str = "/jmp/placement/layerb/"

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

GATEWAY_ENTRANCE_ADDRESS_ONE: int = 0x8001f024
GATEWAY_ENTRANCE_ADDRESS_TWO: int = 0x8001f028
GATEWAY_EXIT_ADDRESS_ONE: int = 0x803bb2fc
GATEWAY_EXIT_ADDRESS_TWO: int = 0x803bb300

class GalaxyUnlockTableFieldNames(StrEnum):
    NAME = "name"
    MAP_PANE_NAME = "MapPaneName"
    OPEN_CONDITION0 = "OpenCondition0"
    OPEN_CONDITION1 = "OpenCondition1"
    OPEN_CONDITION2 = "OpenCondition2"
    POWER_STAR_REQUIREMENT = "PowerStarNum"
    RETURN_DOME = "GrandGalaxyNo"
