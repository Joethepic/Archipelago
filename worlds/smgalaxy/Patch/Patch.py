import hashlib
from pathlib import Path
import os, time

from disc_riider_py import WiiIsoExtractor, rebuild_from_directory
import gclib.fs_helpers as fs
from typing import NamedTuple

from .extensions import RARCExtended, DOLExtended
from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGStages.AstroDome import AstroDome
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy

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

class GalaxyShuffle:
    converter = {"First" : 1,
                 "Second": 2,
                 "Third" : 3,
                 "Fourth": 4,
                 "Fifth" : 5}
    
    def __init__(self, galaxies: dict[str, str], dome_shuffle: dict[int, int]):
        self.galaxies = galaxies
        self.galaxy_destinations: list[GalaxyDestination] = []

        for location, galaxy in self.galaxies.items():
            if location.startswith("Dome"):
                elements = location.split(' ')
                dome_index = int(elements[1])
                orbit_index = self.converter[elements[2]] - 1
                reverse_shuffle = {value: key for key, value in dome_shuffle.items()}
                
                new_galaxy = GalaxyDestination(galaxy, "dome", reverse_shuffle[dome_index], orbit_index)
            elif location.startswith("Gateway"):
                new_galaxy = GalaxyDestination(galaxy, "gateway", None, None)
            else:
                new_galaxy = GalaxyDestination(galaxy, "luma", None, None)
            
            self.galaxy_destinations.append(new_galaxy)

class Patch:
    def __init__(self, base_path: str, iso_path: str, output: dict):
        self.iso_path = iso_path
        self.temp_path = base_path + 'temp'
        self.iso: WiiISO = WiiISO(clean_iso_path=self.iso_path, dest_path=base_path, temp_dir=self.temp_path)

        RARCExtended.iso_base_path = self.temp_path
        DOLExtended.iso_base_path = self.temp_path

        self.counts = output['Galaxy Counts']
        self.galaxies = output['Galaxies']
        self.mario_colours = output['Options']['mario_colors']

        self.old_galaxies = self.galaxies.keys()
        self.new_galaxies = self.galaxies.values()
    
    def unpack_iso(self) -> None:
        """Unpack the contents of the ISO file."""
        self.iso.extract()
    
    def repack_iso(self, delete: bool = True, verbose: bool = False) -> None:
        """Repack the contents of the ISO file."""
        self.iso.repack(delete, verbose)


    def update_mario(self):
        mario = Mario()

        mario.update_colours(self.mario_colours)
        # In the future possibly more functionality

        mario.save()


    def update_astrogalaxy_domes(self, shuffle: dict[int, int]):
        astrogalaxy = AstroGalaxy()
        astrodomescenario = AstroDomeScenario()

        astrogalaxy.shuffle_domes(shuffle)
        astrodomescenario.update(shuffle)

        astrogalaxy.save()
        astrodomescenario.save()
        
    def update_astrodome(self, shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int]):
        astrodome = AstroDome()

        for dome_index in range(1,7):
            reverse_shuffle = {item: key for key, item in dome_shuffle.items()}
            new_index = reverse_shuffle[dome_index]
            astrodome.update_dome([galaxy for galaxy in shuffle if galaxy.dome_index == new_index], dome_index)

        astrodome.save()


    def update_dol(self, dome_galaxies: list[GalaxyDestination], galaxy_counts: dict[str, int]):
        dol = SMGDOL(self.temp_path)
        
        # Overwrite calculating miniature galaxy index
        # Ignore arg0 for koopa model
        address = 0x801ffc44
        new_instruction = b'\x38\x00\x00\x02'
        dol.write_data(fs.write_bytes, address, new_instruction)
        
        # Get obj_arg0 from miniature galaxy
        address = 0x80200758
        new_instruction = b'\x80\x7f\x00\x8c'
        dol.write_data(fs.write_bytes, address, new_instruction)

        # Shift 16 bits to the right to get the custom index
        address = 0x8020075c
        new_instruction = b'\x54\x63\x84\x3e'
        dol.write_data(fs.write_bytes, address, new_instruction)

        # TEMPORARY overwrite miniature count detection, always return 5
        address = 0x801ad614
        new_instruction = b'\x38\x60\x00\x05'
        dol.write_data(fs.write_bytes, address, new_instruction)
        
        address = 0x8037db18
        new_instruction = b'\x38\xc0\x00\x01'
        dol.write_data(fs.write_bytes, address, new_instruction)


        dol.save()
        

class SuperMarioGalaxyRandomiser:
    @staticmethod
    def create_randomiser(base_path: str, iso_path: str, output: dict):
        patch = Patch(base_path, iso_path, output)
        galaxies: dict[str, str] = output["Galaxies"]
        galaxy_counts: dict[str, int] = output["Galaxy Counts"]

        patch.unpack_iso()

        patch.update_mario()

        # TEMPORARY
        dome_shuffle = {1: 3,
                        2: 2,
                        3: 4,
                        4: 1,
                        5: 6,
                        6: 5}
        
        patch.update_astrogalaxy_domes(dome_shuffle)

        galaxy_shuffle: list[GalaxyDestination] = GalaxyShuffle(galaxies, dome_shuffle).galaxy_destinations
        
        dome_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "dome"]
        luma_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "luma"]
        gateway_galaxy = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "gateway"]


        patch.update_astrodome(dome_galaxies, dome_shuffle)

        patch.update_dol(dome_galaxies, galaxy_counts)
        


        patch.repack_iso()



        import winsound
        winsound.MessageBeep(winsound.MB_OK)


if __name__ == "__main__":
    base_path = r"worlds/smgalaxy/Patch/"
    iso_path = base_path + "Super Mario Galaxy (USA) (En,Fr,Es).iso"
    
    with open(base_path + 'example_output.txt', 'r') as f:
        output = eval(f.read())
    
    SuperMarioGalaxyRandomiser.create_randomiser(base_path, iso_path, output)