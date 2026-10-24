""" Module for launching dolphin emulator """
import subprocess
import psutil
import settings
import Utils

from .SMGSettings import SuperMarioGalaxySettings, EmulatorSettings

class DolphinLauncher:
    """
    Manages interactions between the LMClient and the dolphin emulator.
    """
    emulator_settings: EmulatorSettings
    dolphin_process_name = "dolphin"
    exclusion_dolphin_process_name: list[str] = ["dolphinmemoryengine"]

    def __init__(self, supermariogalaxy_settings: SuperMarioGalaxySettings = None):
        if supermariogalaxy_settings is None:
            self.emulator_settings: EmulatorSettings = getattr(settings.get_settings(),"smgalaxy.world_options").dolphin_settings
        else:
            self.emulator_settings = supermariogalaxy_settings.dolphin_settings

    async def launch_dolphin_async(self, rom: str):
        """
        Launches the emulator process if not already running.

        :param rom: The rom to load into emulator when starting the process,
            if 'None' the process won't load any rom.
        """
        if not self.emulator_settings.auto_start:
            return

        if _check_emulator_process_open(self):
            return

        path = self.emulator_settings.path
        if Utils.is_linux and path in [ "", "./" ]:
            raise ValueError("The emulator path is not set, please update the host.yaml file with the emulator path.")

        args = [ path ] + self.emulator_settings.additional_args

        if rom:
            args.append(f"--exec={rom}")

        subprocess.Popen(
            args,
            cwd=None,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def _check_emulator_process_open(dl: DolphinLauncher) -> bool:
    for proc in psutil.process_iter():
        if (dl.dolphin_process_name in proc.name().lower() and not any(
            exclude_name for exclude_name in dl.exclusion_dolphin_process_name if exclude_name in proc.name().lower())):
            return True
    return False
