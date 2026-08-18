import os
import settings
from .Constants.constants import GAME_NAME,EXPECTED_GAME_ID, CLEAN_MD5, InvalidCleanISOError

class EmulatorExecutable(settings.UserFilePath):
    """
    Emulator executable path. Automatically starts rom upon patching completion.
    If using Flatpak, specify the path here.
    """
    is_exe = True
    description = "The path for emulator executable. If using Flatpak, specify this path instead."

class EmulatorAdditionalArguments(list):
    """ Additional arugments to be passed in when auto starting emulator."""
    pass

class EmulatorSettings(settings.Group):
    """Various Emulator specific settings (such as Dolphin)"""
    path: EmulatorExecutable = EmulatorExecutable()
    additional_args: EmulatorAdditionalArguments = EmulatorAdditionalArguments()
    auto_start: bool = True

class ISOFile(settings.UserFilePath):
    """Locate your Super Mario Galaxy ISO"""
    description = "Super Mario Galaxy (USA) ISO"
    copy_to = None

class DolphinProcessName(str):
    """The name of the Dolphin process to connect to. Leave blank for system default."""
    pass

class SuperMarioGalaxy(settings.Group):
    """Various Super Mario Galaxy Settings"""
    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_settings: EmulatorSettings = EmulatorSettings()
    dolphin_process_name: DolphinProcessName = DolphinProcessName("")

def get_base_rom_path() -> str:
    import Utils

    """Gets the base rom path from the host.yml settings."""
    options: settings.Settings = settings.get_settings()
    file_name = options["smgalaxy.world_options"]["iso_file"]
    
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
        verify_base_rom(file_name)
        options["smgalaxy.world_options"]["iso_file"] = file_name

    return file_name

def verify_base_rom(clean_iso_path: str):
    import hashlib
    """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
    of the file matches against the one we expect, and third, we had a game id in the file that matches the games
    official one"""
    # Verifies we have a valid installation of Super Mario Galaxy USA. There are some regional file differences.
    print(f"Verifying if the provided ISO is a valid copy of {GAME_NAME}...")

    # Reads the file in chunks, as its too big as a file on its own and could lead to the python process slowing
    # down to process and read each byte. After reading each chunk, it updates and calculates the MD5
    base_md5 = hashlib.md5()
    with open(clean_iso_path, "rb") as f:
        while chunk := f.read(1024 * 1024):  # Read the file in chunks.
            base_md5.update(chunk)

        # Grab the Magic Code and Game_ID with the file still open
        f.seek(0)
        game_id = f.read(6).decode("shift_jis")
        magic = game_id[:4]
        print(f"Magic Code: {magic}; Game ID: {game_id}")

    # Verify that the file has the right has format first, as the wrong file could have been loaded.
    md5_conv = int(base_md5.hexdigest(), 16)
    if md5_conv != CLEAN_MD5:
        raise InvalidCleanISOError(f"Invalid vanilla {GAME_NAME} ISO.\nYour ISO may be corrupted or your " +
                                   f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {CLEAN_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

    # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    if magic == "CISO":
        raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {GAME_NAME} randomizer " +
                                   "only supports ISOs in ISO format.")
    if game_id != EXPECTED_GAME_ID:
        # Checks this starts with "RMG" at least, otherwise user provided an entirely different game.
        if game_id and game_id.startswith(EXPECTED_GAME_ID[:3]):
            raise InvalidCleanISOError(f"Invalid version of {GAME_NAME}. " +
                                       "Currently, only the North American / English version is supported by this randomizer.")
        else:
            raise InvalidCleanISOError(f"Non-{GAME_NAME} game detected. Please re-select the vanilla " +
                                       f"{GAME_NAME}'s ISO (North American version).")
    return
