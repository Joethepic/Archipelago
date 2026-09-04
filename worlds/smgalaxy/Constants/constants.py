from enum import IntEnum

# Client Constants
AP_WORLD_VERSION_NAME: str = "APWorldVersion"
CLIENT_VERSION: str = "V0.0.1"
CLIENT_NAME: str = "SMG Client"
GAME_NAME: str = "Super Mario Galaxy"
CLEAN_MD5: int = 0xf99a97f9ae4dccd1db45e9aaab9cebd8
EXPECTED_GAME_ID: str = "RMGE01"

# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS: str = "Detected a non-randomized ROM for SMG. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS: str = "Dolphin connection was lost. Please restart your emulator and make sure SMG is running."
NO_SLOT_NAME_STATUS: str = "No slot name was detected. Ensure a randomized ROM is loaded. Retrying in 5 seconds..."
CONNECTION_VERIFY_SERVER: str = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS: str = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY: str = "Dolphin did not load the ROM correctly. Close only the game / dolphin launcher and try again..."
CONNECTION_CONNECTED_STATUS: str = "Dolphin is connected, AP is connected, Ready to play SMG!"
AP_REFUSED_STATUS: str = "AP Refused to connect for one or more reasons, see above for more details."

DEATH_MESSAGES = [
    "got sucked into a black hole",
    "ran into a goomba",
    "fell into the void",
    "got trampled by Bowser",
    "failed to rescue Princess Peach",
    "missed the power star",
    "missed the grand star"
    "flew too close to the sun"
]

WAIT_TIMER_LONG_TIMEOUT: int = 5
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125
DEATH_LINK_TIMEOUT: int = WAIT_TIMER_LONG_TIMEOUT * 3
# Colors
WHITE = (255,  255,  255)
RED = (255,  0,  0)
PINK = (240, 67, 205)
ORANGE = (247, 161, 2)
GREEN = (0,128,  0)
YELLOW = (255, 247, 0)
BLUE = (0,  0,255)
PURPLE = (128,  0,128)
BLACK = (0, 0, 0)
BROWN = (165, 42, 42)
GRAY = (128,128,128)
colors: dict[str, tuple[int, int, int]] = {"red": RED,
                                           "Orange": ORANGE,
                                           "Yellow": YELLOW,
                                           "Green" : GREEN,
                                           "Blue"  : BLUE,
                                           "Purple": PURPLE,
                                           "Black" : BLACK,
                                           "Brown" : BROWN,
                                           "White" : WHITE,
                                           "Pink"  : PINK,
                                           "Gray"  : GRAY}

class PowerStarColorEnum(IntEnum):
    YELLOW = 0
    BLUE = 1
    GREEN = 2
    RED = 3

class InvalidCleanISOError(Exception): pass
