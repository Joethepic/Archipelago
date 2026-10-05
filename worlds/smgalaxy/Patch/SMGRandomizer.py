import os, sys, tempfile, zipfile, json
import shutil
import ssl, certifi, urllib.request
from importlib import resources
from typing import Any
from logging import getLogger

import requests

import Utils
from .SMGClientHelpers import GalaxyDestination, GalaxyShuffle
from ..SMGSettings import get_base_rom_path
from ..Constants.constants import GAME_NAME, CLIENT_NAME, CLIENT_VERSION

from worlds.Files import APAutoPatchInterface, AutoPatchRegister


class SuperMarioGalaxyRandomiser(APAutoPatchInterface, metaclass=AutoPatchRegister):
    game = GAME_NAME
    patch_file_ending = ".apsmg"
    result_file_ending = ".iso"
    input_path: str

    def __init__(self, apsmg_path: str, *args: Any, **kwargs: Any):
        super(SuperMarioGalaxyRandomiser, self).__init__(*args, **kwargs)
        self.input_path = apsmg_path
        self._client_logger = getLogger(CLIENT_NAME)

    def patch(self, target: str) -> None:
        vanilla_rom_path = get_base_rom_path()

        try:
            self.create_iso(vanilla_rom_path, target) # Does not have hash verification, will want ot add
        except ImportError as ex:
            self._client_logger.warning("Error while trying to import third party dependencies. Details: " + str(ex))
            self._update_deps()
            self.create_iso(vanilla_rom_path, target)

    def _update_deps(self):
        self._client_logger.info("Updating SMG dependencies...")
        local_dir_path = _get_temp_folder_name()

        # Skip install if already present for this version
        if os.path.isdir(local_dir_path) and os.listdir(local_dir_path):
            self._client_logger.info(f"SMG Dependencies already exist, including them in sys.path: {local_dir_path}")
            sys.path.append(local_dir_path)
            return

        lib_path = _get_archive_name()
        self._client_logger.info(f"Dependency archive name to use: {lib_path}")
        os.makedirs(local_dir_path, exist_ok=True)
        self.download_lib_zip(local_dir_path, lib_path)

        self._client_logger.info(f"Appending the following to sys path to get dependencies correctly: {local_dir_path}")
        sys.path.insert(0, local_dir_path)

    def create_iso(self, vanilla_rom_path: str, target: str):
        try:
            from wiithon import WiiIsoPatcher
            from wiithon.formats.dol import DOL
        except:
            raise ImportError(f"Cannot continue patching {GAME_NAME} due to missing libraries.")

        from .Patch import Patch
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

    def download_lib_zip(self, tmp_dir_path: str, lib_path: str) -> None:
        self._client_logger.info("Getting missing dependencies for Super Mario Galaxy from remote source.")
        lib_path_base = f"https://github.com/Joethepic/Archipelago/releases/download/{CLIENT_VERSION}"
        download_path = f"{lib_path_base}/{lib_path}{sys.version_info.major}-{sys.version_info.minor}.zip"

        temp_zip_path = os.path.join(tmp_dir_path, "temp.zip")
        try:
            with requests.get(download_path, stream=True) as response:
                response.raise_for_status()
                with open(temp_zip_path, 'wb') as created_zip:
                    for chunk in response.iter_content(chunk_size=8192):
                        created_zip.write(chunk)
        except Exception as downloadEx:
            self._client_logger.error(
                "While trying to download LM dependencies from the release page, an unexpected error " +
                f"occurred while using the requests library. Additional details: {str(downloadEx)}")
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(download_path, context=ssl_context) as response, \
                    open(temp_zip_path, 'wb') as created_zip:
                created_zip.write(response.read())

        with zipfile.ZipFile(temp_zip_path) as z:
            z.extractall(tmp_dir_path)

def _get_temp_folder_name() -> str:
    """Gets a temp file based on the current OS, then a subdirectory for game, version, and libs."""
    return os.path.join(tempfile.gettempdir(), "super_mario_galaxy", CLIENT_VERSION, "libs")

def _get_archive_name() -> str:
    if not (Utils.is_linux or Utils.is_windows):
        message = f"Your OS is not supported with this randomizer {sys.platform}."
        raise RuntimeError(message)

    lib_path = ""
    if Utils.is_windows:
        lib_path = f"windows-{sys.version_info.major}-{sys.version_info.minor}"
    elif Utils.is_linux:
        lib_path = f"linux-{sys.version_info.major}-{sys.version_info.minor}"

    return lib_path