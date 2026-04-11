import hashlib
from pathlib import Path
import os, time

from disc_riider_py import WiiIsoExtractor, rebuild_from_directory
import gclib.fs_helpers as fs
from typing import NamedTuple, Optional

from .extensions import RARCExtended, DOLExtended
from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGStages.AstroDome import AstroDome
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy
from ..regions import region_list

class InvalidCleanISOError(Exception): pass

# Name of the game, which is used in various error messaging.
RANDOMIZER_NAME: str = "Super Mario Galaxy"

# Can pull this from dolphin or a cmd command / bash command
CLEAN_MD5: int = 0xf99a97f9ae4dccd1db45e9aaab9cebd8

# Expected Game ID of the GC/Wii game we expect here.
EXPECTED_GAME_ID: str = "RMGE01"


class WiiISO:
    def __init__(self, clean_iso_path: str, iso_name: str = RANDOMIZER_NAME + " Patched", dest_path: str = r"", temp_dir: str = r"temp"):
        """Initialize a Patch object for Super Mario Galaxy ISO modification.
        Args:
            clean_iso_path (str): Path to the unmodified ISO file to be patched.
            iso_name (str): Name for the newly created patched ISO file. 
                            Defaults to RANDOMIZER_NAME + " Patched".
            dest_path (str): Directory path where the repacked ISO will be saved. 
                             Defaults to current directory if empty string.
            temp_dir (str): Temporary directory path for extracting ISO contents during patching.
                            Defaults to "temp". This directory will be cleaned up after patching.
        Attributes:
            clean_iso_path (str): Path of the unmodified ISO.
            dest_path (str): Output directory for the patched ISO.
            temp_dir (str): Temporary extraction directory.
            iso_name (str): Name of the new ISO file.
        """
        self.clean_iso_path = clean_iso_path
        self.dest_path = dest_path
        self.temp_dir = temp_dir
        self.iso_name = iso_name

        self.progress = None
        self.calling_function = None

    def verify_base_rom(self):
        """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
        of the file matches against the one we expect, and third, we had a game id in the file that matches the games
        official one"""
        # Verifies we have a valid installation of Super Mario Galaxy USA. There are some regional file differences.
        print(f"Verifying if the provided ISO is a valid copy of {RANDOMIZER_NAME}...")
        
        # Reads the file in chunks, as its too big as a file on its own and could lead to the python process slowing
        # down to process and read each byte. After reading each chunk, it updates and calculates the MD5
        base_md5 = hashlib.md5()
        with open(self.clean_iso_path, "rb") as f:
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
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {CLEAN_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                "only supports ISOs in ISO format.")
        if game_id != EXPECTED_GAME_ID:
            # Checks this starts with "RMG" at least, otherwise user provided an entirely different game.
            if game_id and game_id.startswith(EXPECTED_GAME_ID[:3]):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                    "Currently, only the North American / English version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError(f"Non-{RANDOMIZER_NAME} game detected. Please re-select the vanilla " +
                    f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return

    def extract(self):
        """Extracts the ISO into the output directory, preserving the orignal file/folder structure within the ISO.
        Once extracted, you can then read these files individually to change/edit, create new folders/files in the
        structure or delete old ones.
        """
        try:
            # Makes sure the file exists
            if not Path(self.clean_iso_path).exists():
                raise Exception(f"ISO file not found: {self.clean_iso_path}")
                
            # Extract the Wii file into memory and load all the disc partitions/disc structure.
            extractor: WiiIsoExtractor = WiiIsoExtractor(self.clean_iso_path)

            # Prepare the Data section of the disc by reading its file metadata into memory.
            extractor.prepare_extract_section("DATA")

            # Once prepared, we can export it to a directory of our choice.
            print("Initiating extracting ISO")
            self.calling_function = 'extract_iso'
            extractor.extract_to(self.temp_dir, self.progress_callback)

            print("Extacting ISO complete")

        except Exception as e:
            raise Exception(f"ISO extraction failed: {e}")

    def repack(self, delete: bool = True, verbose: bool = True):
        """Takes an extracted ISO directory and re-compiles it into a playable Wii ISO."""
        output_path = Path(self.dest_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("Initiating repacking ISO")
        self.calling_function = 'repack_iso'
        rebuild_from_directory(self.temp_dir, self.dest_path + self.iso_name + '.iso', callback=self.progress_callback)
        
        print("Repacking ISO complete")

        if delete:
            print("Deleting temporary directory...")

            # Delete the extracted ISO after its done repacking
            time.sleep(10)
            self._delete_temp_dir(self.temp_dir, verbose)
            
            print("Done deleting temporary directory!")
        
    def _delete_temp_dir(self, temp_dir, verbose: bool = True):
        """Remove the temporarily created directory for the extracted ISO"""
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            # Remove it if its a file otherwise recurse
            if os.path.isfile(file_path):
                os.remove(file_path)
                if verbose:
                    print(f"Deleting temp file: {file_path}")
            else:
                self._delete_temp_dir(file_path, verbose)
        
        if verbose:
            print(f"Deleting empty directory: {temp_dir}")
        os.rmdir(temp_dir)

    def progress_callback(self, progress):
        """Prints the progress as the callback is completing its steps."""
        out = ''
        if self.calling_function == 'repack_iso':
            out = "repacking ISO"
        elif self.calling_function == 'extract_iso':
            out = "extracting ISO"
        
        if progress % 10 == 0:
            if self.progress != progress:
                self.progress = progress
                print(f"Progress {out}: {self.progress}%")

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int
    orbit_index: int
    old_luma_name: str

class GalaxyShuffle:
    converter = {"First" : 1,
                 "Second": 2,
                 "Third" : 3,
                 "Fourth": 4,
                 "Fifth" : 5}
    galaxy_destinations: list[GalaxyDestination]
    
    def __init__(self, galaxies: dict[str, str], dome_shuffle: dict[int, int]):
        self.galaxies = galaxies
        self.galaxy_destinations = []

        # Generate a list of GalaxyDestinations from the galaxies dict
        for location, galaxy in self.galaxies.items():
            # Convert to its in-game name
            galaxy = region_list[galaxy].in_game_name

            if location.startswith("Dome"):
                # Extract the dome index and orbit index
                elements: list[str] = location.split(' ')
                dome_index: int = int(elements[1])
                orbit_index: int = self.converter[elements[2]] - 1
                reverse_shuffle: dict[int, int] = {value: key for key, value in dome_shuffle.items()}
                
                new_galaxy = GalaxyDestination(galaxy, "dome", reverse_shuffle[dome_index], orbit_index, None)

            elif location.startswith("Gateway"):
                new_galaxy = GalaxyDestination(galaxy, "gateway", None, None, None)

            else:
                luma_name: str = location.replace("Hungry Luma", "Galaxy").replace("Launch Star", "Galaxy")
                new_galaxy = GalaxyDestination(galaxy, "luma", None, None, region_list[luma_name].in_game_name)
            
            self.galaxy_destinations.append(new_galaxy)

class Patch:
    def __init__(self, base_path: str, iso_path: str, output: dict):
        self.iso_path: str = iso_path
        self.temp_path: str = base_path + 'temp'
        self.iso: WiiISO = WiiISO(clean_iso_path=self.iso_path, dest_path=base_path, temp_dir=self.temp_path)

        RARCExtended.iso_base_path = self.temp_path
        DOLExtended.iso_base_path = self.temp_path

        self.counts: dict[str, int] = output['Galaxy Counts']
        self.galaxies: dict[str, str] = output['Galaxies']
        self.mario_colours: dict[str, str] = output['Options']['mario_colors']

        self.old_galaxies: str = self.galaxies.keys()
        self.new_galaxies: str = self.galaxies.values()

        self.unpack_iso()

        self.mario: Mario = Mario()
        self.astrogalaxy: AstroGalaxy = AstroGalaxy()
        self.astrodomescenario: AstroDomeScenario = AstroDomeScenario()
        self.astrodome: AstroDome = AstroDome()
        self.dol: SMGDOL = SMGDOL()

    def unpack_iso(self) -> None:
        """Unpack the contents of the ISO file."""
        self.iso.extract()
    
    def repack_iso(self, delete: bool = True, verbose: bool = False) -> None:
        """Repack the contents of the ISO file."""
        self.iso.repack(delete, verbose)

    def update_mario(self) -> None:
        """
        Update mario. Currently only updates his outfit colours, but might do more stuff in the future.
        """
        # In the future possibly more functionality
        self.mario.update_colours(self.mario_colours)

    def update_astrogalaxy(self, dome_shuffle: dict[int, int], luma_shuffle: list[GalaxyDestination]) -> None:
        """
        Shuffle the domes and luma galaxies within the observatory. This includes both the visual domes (within AstroGalaxy) and the
        loading zones (within AstroDomeScenario). The dome shuffle dict must contain all indices from 1 to 6 as both keys and values.
        Luma shuffle is a list of GalaxyDestinations and if a luma name exists it expect the type to be "luma".
        dome_shuffle:
            key: old dome index (1-6)
            value: new dome index (1-6)
        """
        self.astrogalaxy.shuffle_domes(dome_shuffle)
        self.astrogalaxy.shuffle_lumas(luma_shuffle)
        self.astrogalaxy.save_objinfo()

        self.astrodomescenario.shuffle_loading_zones(dome_shuffle)

    def update_astrodomes(self, galaxy_shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int]) -> None:
        """
        Shuffle the galaxies within a dome. This iterates over all the 6 domes and updates the entry according to the galaxy shuffle.
        Galaxy shuffle is a list of GalaxyDestinations and if a dome and orbit index exists, it expects the type to be "dome". Dome shuffle
        is a mapping of the old dome index to the new dome index. Each key and value must contain all indices from 1 to 6 and is not checked.
        dome_shuffle:
            key: old dome index (1-6)
            value: new dome index (1-6)
        """
        for dome_index in range(1,7):
            reverse_shuffle = {item: key for key, item in dome_shuffle.items()}
            new_index = reverse_shuffle[dome_index]
            self.astrodome.update_dome([galaxy for galaxy in galaxy_shuffle if galaxy.dome_index == new_index], dome_index)

    def update_nameobjfactory(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination]) -> None:
        dome_galaxy_names = [galaxy.name for galaxy in dome_galaxies]
        luma_galaxy_names = [galaxy.name for galaxy in luma_galaxies]
        
        self.dol.set_name_object_factory_galaxies(dome_galaxy_names, luma_galaxy_names)

    def update_galaxyunlocktable(self, dome_galaxies: list[GalaxyDestination], star_requirements: dict[str, int], dome_shuffle) -> None:
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1,7)}
        
        for location, requirement in star_requirements.items():
            dome_index: int = dome_shuffle[int(location[1])]
            orbit_index: int = int(location[3:])

            requirements[dome_index][orbit_index] = requirement
        
        for galaxy in dome_galaxies:
            star_requirement: int = requirements[galaxy.dome_index][galaxy.orbit_index + 1]

            entry = self.dol.get_galaxy_unlock_table_entry_by_name(galaxy.name)
            entry.power_star_requirement = star_requirement
            entry.return_dome = galaxy.dome_index
            self.dol.galaxy_unlock_table.set_entry(entry)

    def update_instructions(self) -> None:
        # BROKEN, NEED TO FIX
        """
        ############################################
        # Skip the prologue (cutscene + gateway 1) #
        ############################################
        # Select the grand star 1 return demo to prepare
        address = 0x803bb434
        new_instruction = b'\x38\x84\xc3\x68'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Set stage name to AstroGalaxy to load
        address = 0x803bb43c
        new_instruction = b'\x38\x7f\x03\xf8'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Set scenario number to 4 to load
        address = 0x803bb440
        new_instruction = b'\x38\x00\x00\x04'
        self.dol.write_data(fs.write_bytes, address, new_instruction)
        """
        ########################
        # Set swing permission #
        ########################
        address = 0x803b55b0
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        #######################################
        # Miniature galaxy orbit manipulation #
        #######################################
        # Get obj_arg0 from miniature galaxy
        address = 0x80200758
        new_instruction = b'\x80\x7f\x00\x8c'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Shift 16 bits to the right to get the upper bits where the custom index is stored
        address = 0x8020075c
        new_instruction = b'\x54\x63\x84\x3e'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        ################################
        # Scenario select star loading #
        ################################
        # Keep loading regular stars even if they're not available yet
        address = 0x8037d9ec
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Calculate all secret/comet stars, including possibly normally unavailable ones
        address = 0x8037da44
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Show secret/comet stars as calculated above
        address = 0x8037db54
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Set visibility to 1 (not collected) if appearing as collected has failed (ensuring it shows up even if not available)
        address = 0x8037db18
        new_instruction = b'\x38\xc0\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Always show up and appear correctly as collected/not collected
        address = 0x8037db74
        new_instruction = b'\x38\xc6\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        ############################################################
        # TEMPORARY TEMPORARY TEMPORARY TEMPORARY TEMPORARY TEMPOR #
        ##### Overwrite miniature count detection, always return 5 #
        ############################################################
        # Set the count as 5
        address = 0x801ad614
        new_instruction = b'\x38\x60\x00\x05'
        self.dol.write_data(fs.write_bytes, address, new_instruction)
        
    def save_all(self) -> None:
        """
        Save all the changes made to the different files back to the ISO.
        Saves:
            Mario.arc
            AstroGalaxy.arc
            AstroDomeScenario.arc
            AstroDome.arc
            main.dol
        """
        self.mario.save()
        self.astrogalaxy.save()
        self.astrodomescenario.save()
        self.astrodome.save()
        self.dol.save()

        self.save_copies()

    def save_copies(self):
        self.mario.save_to_new_file("MarioCopy.arc")
        self.astrogalaxy.save_to_new_file("AstroGalaxyCopy.arc")
        self.astrodomescenario.save_to_new_file("AstroDomeScenarioCopy.arc")
        self.astrodome.save_to_new_file("AstroDomeCopy.arc")

class SuperMarioGalaxyRandomiser:
    @staticmethod
    def create_randomiser(base_path: str, iso_path: str, output: dict) -> None:
        patch = Patch(base_path, iso_path, output)
        galaxies: dict[str, str] = output["Galaxies"]
        galaxy_counts: dict[str, int] = output["Galaxy Counts"]

        patch.update_mario()

        # TEMPORARY
        dome_shuffle = {1: 3,
                        2: 2,
                        3: 4,
                        4: 1,
                        5: 6,
                        6: 5}
        
        galaxy_shuffle: list[GalaxyDestination] = GalaxyShuffle(galaxies, dome_shuffle).galaxy_destinations
        
        dome_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "dome"]
        luma_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "luma"]
        gateway_galaxy = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "gateway"]
        
        patch.update_astrogalaxy(dome_shuffle, luma_galaxies)

        patch.update_astrodomes(dome_galaxies, dome_shuffle)
        patch.update_nameobjfactory(dome_galaxies, luma_galaxies)
        patch.update_galaxyunlocktable(dome_galaxies, galaxy_counts, dome_shuffle)

        patch.update_instructions()

        patch.save_all()

        patch.repack_iso()



        import winsound
        winsound.MessageBeep(winsound.MB_OK)


if __name__ == "__main__":
    base_path = r"worlds/smgalaxy/Patch/"
    iso_path = base_path + "Super Mario Galaxy (USA) (En,Fr,Es).iso"
    
    with open(base_path + 'example_output.txt', 'r') as f:
        output = eval(f.read())
    
    SuperMarioGalaxyRandomiser.create_randomiser(base_path, iso_path, output)
