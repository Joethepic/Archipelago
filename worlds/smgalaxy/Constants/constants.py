# Client Constants
AP_WORLD_VERSION_NAME: str = "APWorldVersion"
CLIENT_VERSION: str = "V0.0.1"
CLIENT_NAME: str = "SMG Client"
GAME_NAME: str = "Super Mario Galaxy"

# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS: str = "Detected a non-randomized ROM for SMG. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS: str = "Dolphin connection was lost. Please restart your emulator and make sure SMG is running."
NO_SLOT_NAME_STATUS: str = "No slot name was detected. Ensure a randomized ROM is loaded. Retrying in 5 seconds..."
CONNECTION_VERIFY_SERVER: str = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS: str = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY: str = "Dolphin did not load the ROM correctly. Close only the game / dolphin launcher and try again..."
CONNECTION_CONNECTED_STATUS: str = "Dolphin is connected, AP is connected, Ready to play SMG!"
AP_REFUSED_STATUS: str = "AP Refused to connect for one or more reasons, see above for more details."

EXPECTED_GAME_ID: str = "RMGE01"
WAIT_TIMER_LONG_TIMEOUT: int = 5
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125