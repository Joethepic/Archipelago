import os
import zipfile, json

# Handle import requirement updates before anything else.
import ModuleUpdate
local_dir = os.path.dirname(__file__)
smg_reqs = os.path.join(local_dir, 'requirements.txt')
ModuleUpdate.requirements_files.update(smg_reqs)
ModuleUpdate.update(True, True)

from wiithon import WiiIsoPatcher
from wiithon.formats.dol import DOL

from .SMGClientHelpers import GalaxyDestination, GalaxyShuffle
from ..SMGSettings import get_base_rom_path
from ..Constants.constants import GAME_NAME

from worlds.Files import APAutoPatchInterface, AutoPatchRegister


class SuperMarioGalaxyRandomiser(APAutoPatchInterface, metaclass=AutoPatchRegister):
    game = GAME_NAME
    patch_file_ending = ".apsmg"
    result_file_ending = ".iso"
    input_path: str

    def __init__(self, apsmg_path: str):
        super().__init__()
        self.input_path = apsmg_path

    def patch(self, target: str) -> None:
        from .Patch import Patch
        vanilla_rom_path = get_base_rom_path()

        with WiiIsoPatcher(vanilla_rom_path) as patcher:
            # Get the data from the generated output to use for patching
            with zipfile.ZipFile(self.input_path, "r") as zf:
                output = json.loads(zf.read("patch.json").decode('shift-jis'))

            patch = Patch(patcher, output)

            galaxies: dict[str, str] = patch.galaxies
            galaxy_counts: dict[str, int] = patch.counts
            dome_shuffle = {i: int(patch.dome_shuffle[f"Dome {i}"].removeprefix("Dome ")) for i in range(1, 7)}

            galaxy_shuffle: list[GalaxyDestination] = GalaxyShuffle(galaxies).galaxy_destinations

            dome_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "dome"]
            luma_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "luma"]
            gateway_galaxy = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "gateway"][0]

            patch.update(dome_galaxies, dome_shuffle, luma_galaxies)

            def dol_patch(dol: DOL):
                patch.build_dol(dol)
                patch.update_dol(dome_galaxies, luma_galaxies, dome_shuffle, galaxy_counts, gateway_galaxy)

            patcher.patch_dol(dol_patch)

            print("Starting building...")

            patcher.build(target)