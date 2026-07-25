import os
import settings

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
        options["smgalaxy.world_options"]["iso_file"] = file_name

    return file_name
