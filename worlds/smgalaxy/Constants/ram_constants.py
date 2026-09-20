from typing import NamedTuple

from .Names.item_names import POWER, GRAND, GREEN

# The base address of all the pointers
GAMESYSTEM = 0x806A1228

# Gets the current Game status, as if you are in-game, in the menu, viewing the logo, etc.
# GameSystem -> GameSystemSceneController -> SceneControlInfo
CURRENT_SCENE_POINTER_LIST: list[int] = [0x24, 0x0] # 32 chars

# Gets the current galaxy that you are in. This address also says "File-Select" if you have not chosen a file yet.
# GameSystem -> GameSystemSceneController -> SceneControlInfo
CURRENT_GALAXY_POINTER_LIST: list[int] = [0x24, 0x20] # 32 chars

# Gets the current scenario number. Defaults to -1 when none selected (e.g. scenario select)
# GameSystem -> GameSystemSceneController -> SceneControlInfo
CURRENT_SCENARIO_POINTER_LIST: list[int] = [0x24, 0x40]

# RAM Address offset to the start of all Galaxy struct address pointers
# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder -> GameDataAllGalaxyStorage
GALAXY_DATA_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0xC, 0x8]
STAR_BIT_FLAG_OFFSET: int = 0x8

# RAM Address for handling 1-ups
# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder -> GameDataPlayerStatus
ONEUP_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0x8, 0x4]

# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder -> GameDataPlayerStatus
STARBITS_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0x8, 0x8]

# RAM address for getting the Mario actor object.
# GameSystem -> GameSystemSceneController -> Scene -> SceneObjHolder -> MarioHolder -> MarioActor
MARIO_ACTOR_POINTER_LIST: list[int] = [0x24, 0xAC, 0x10, 0x50, 0xC]

# RAM address for being able to spin. 0 = disabled, 1 = enabled
SWING_PERMISSION_POINTER_LIST: list[int] = MARIO_ACTOR_POINTER_LIST + [0xEEB]

# GameSystem -> GameSequenceDirector -> SaveDataHandleSequence -> UserFile -> GameDataHolder
LAST_RECEIVED_ITEM_POINTER_LIST: list[int] = [0xC, 0x8, 0xC, 0x0, 0x30]

STATIC_VARIABLES_POINTER = 0x80004024
STARCOLOUR = "Star Colour"
GREENGALAXY = "Green Galaxies"
LUMAGALAXY = "Luma Galaxies"
FORCEDEATH = "Kill mario forcefully"
ISDEAD = "Is mario dead"
DEATHLINK = "Deathlink"
DEATHTIMER = "Time between deathlink deaths"
LAST_RECV_INDEX = "Last Item Received Idx"
SLOTNAME = "Slot Name"

class StaticVariable(NamedTuple):
    name: str
    size: int

variables: list[StaticVariable] = [
    StaticVariable("Start", 0),
    StaticVariable(POWER, 1),
    StaticVariable(GRAND, 1),
    StaticVariable(GREEN, 1),
    StaticVariable('', 1),

    # Deathlink
    StaticVariable(FORCEDEATH, 1),
    StaticVariable(ISDEAD, 1),
    StaticVariable(DEATHLINK, 1),
    StaticVariable("Death count", 1),
    StaticVariable(DEATHTIMER, 2),
    StaticVariable("Death cooldown", 2),

    StaticVariable(SLOTNAME, 64),
    StaticVariable(STARCOLOUR, 8 * 45),
    StaticVariable(GREENGALAXY, 5 * 32),
    StaticVariable(LUMAGALAXY, 7 * (30 + 2)),
    StaticVariable("End", 0)
]

STATIC_VARIABLE_OFFSETS: dict[str, int] = {var.name: sum(v.size for v in variables[:i]) for i, var in enumerate(variables)}
