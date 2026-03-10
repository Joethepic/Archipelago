import hashlib
from pathlib import Path
import os, time, random

from disc_riider_py import WiiIsoExtractor, rebuild_from_directory
from dicts import miniature_to_galaxy, galaxy_to_miniature
from gclib.rarc import RARC
from gclib.dol import DOL
from gclib.j3d import BDL
from gclib.yaz0_yay0 import Yaz0
from io import BytesIO

import random
from bcsv import BCSV
from change_mario_colours import change_mario_colours
from change_dome_galaxies import change_dome_miniature
from add_miniature import replace_miniatures, adjust_nameobjfactory_table
import change_dol as ch_dol

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
            time.sleep(3)
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

miniature_galaxies = galaxy_to_miniature.keys()

major_galaxies = """Good Egg Galaxy
Honeyhive Galaxy
Space Junk Galaxy
Battlerock Galaxy
Beach Bowl Galaxy
Ghostly Galaxy
Gusty Garden Galaxy
Freezeflame Galaxy
Dusty Dunes Galaxy
Gold Leaf Galaxy
Sea Slide Galaxy
Toy Time Galaxy
Deep Dark Galaxy
Dreadnought Galaxy
Melty Molten Galaxy"""

minor_galaxies = """Gateway Galaxy
Sweet Sweet Galaxy
Sling Pod Galaxy
Drip Drop Galaxy
Bigmouth Galaxy
Sand Spiral Galaxy
Snow Cap Galaxy
Boo's Boneyard Galaxy
Rolling Gizmo Galaxy
Loopdeeswoop Galaxy
Bubble Blast Galaxy
Loopdeeloop Galaxy
Flipswitch Galaxy
Rolling Green Galaxy
Hurry-Scurry Galaxy
Bubble Breeze Galaxy
Buoy Base Galaxy
Honeyclimb Galaxy
Bonefin Galaxy
Matter Splatter Galaxy"""

boss_galaxies = """Bowser Jr.'s Robot Reactor
Bowser Jr.'s Airship Armada
Bowser Jr.'s Lava Reactor
Bowser's Star Reactor
Bowser's Dark Matter Plant"""

default_galaxies: dict[str, str] =  {"Dome 1 First Orbit Galaxy" : "Good Egg Galaxy",
                                     "Dome 2 First Orbit Galaxy" : "Space Junk Galaxy",
                                     "Dome 3 First Orbit Galaxy" : "Beach Bowl Galaxy",
                                     "Dome 4 First Orbit Galaxy" : "Gusty Garden Galaxy",
                                     "Dome 5 First Orbit Galaxy" : "Gold Leaf Galaxy",
                                     "Dome 6 First Orbit Galaxy" : "Deep Dark Galaxy",
                                     "Dome 1 Second Orbit Galaxy": "Honeyhive Galaxy",
                                     "Dome 2 Third Orbit Galaxy" : "Battlerock Galaxy",
                                     "Dome 3 Third Orbit Galaxy" : "Ghostly Galaxy",
                                     "Dome 4 Second Orbit Galaxy": "Freezeflame Galaxy",
                                     "Dome 5 Second Orbit Galaxy": "Sea Slide Galaxy",
                                     "Dome 6 Second Orbit Galaxy": "Dreadnought Galaxy",
                                     "Dome 4 Third Orbit Galaxy" : "Dusty Dune Galaxy",
                                     "Dome 5 Third Orbit Galaxy" : "Toy Time Galaxy",
                                     "Dome 6 Fourth Orbit Galaxy" : "Melty Molten Galaxy",
                                     "Dome 1 Third Orbit Galaxy" : "Loopdeeloop Galaxy",
                                     "Dome 2 Second Orbit Galaxy": "Rolling Green Galaxy",
                                     "Dome 3 Second Orbit Galaxy": "Bubble Breeze Galaxy",
                                     "Dome 4 Fourth Orbit Galaxy": "Honeyclimb Galaxy",
                                     "Dome 5 Fourth Orbit Galaxy": "Bonefin Galaxy",
                                     "Dome 6 Third Orbit Galaxy" : "Matter Splatter Galaxy",
                                     "Dome 1 Fourth Orbit Galaxy": "Flipswitch Galaxy",
                                     "Dome 2 Fourth Orbit Galaxy": "Hurry-Scurry Galaxy",
                                     "Dome 3 Fourth Orbit Galaxy": "Buoy Base Galaxy",
                                     "Sweet Sweet Hungry Luma"   : "Sweet Sweet Galaxy",
                                     "Sling Pod Hungry Luma"     : "Sling Pod Galaxy",
                                     "Drip Drop Hungry Luma"     : "Drip Drop Galaxy",
                                     "Bigmouth Hungry Luma"      : "Bigmouth Galaxy",
                                     "Sand Spiral Hungry Luma"   : "Sand Spiral Galaxy",
                                     "Snow Cap Hungry Luma"      : "Snow Cap Galaxy",
                                     "Gateway Dome"              : "Gateway Galaxy",
                                     "Boo's Boneyard Hungry Luma": "Boo's Boneyard Galaxy",
                                     "Rolling Gizmo Launch Star" : "Rolling Gizmo Galaxy",
                                     "Loopdeeswoop Launch Star"  : "Loopdeeswoop Galaxy",
                                     "Bubble Blast Launch Star"  : "Bubble Blast Galaxy",
                                     "Dome 1 Fifth Orbit Galaxy" : "Bowser Jr.'s Robot Reactor",
                                     "Dome 2 Fifth Orbit Galaxy" : "Bowser's Star Reactor",
                                     "Dome 3 Fifth Orbit Galaxy" : "Bowser Jr.'s Airship Armada",
                                     "Dome 4 Fifth Orbit Galaxy" : "Bowser's Dark Matter Plant",
                                     "Dome 5 Fifth Orbit Galaxy" : "Bowser Jr.'s Lava Reactor"}

example_input = {
        "Dome 1 First Orbit Galaxy" : "Honeyhive Galaxy",
        "Dome 1 Second Orbit Galaxy": "Dusty Dune Galaxy",
        "Dome 1 Third Orbit Galaxy" : "Loopdeeloop Galaxy",
        "Dome 1 Fourth Orbit Galaxy": "Bowser's Dark Matter Plant",
        "Dome 2 First Orbit Galaxy" : "Battlerock Galaxy",
        "Dome 2 Second Orbit Galaxy": "Honeyclimb Galaxy",
        "Dome 2 Third Orbit Galaxy" : "Good Egg Galaxy",
        "Dome 2 Fourth Orbit Galaxy": "Bowser's Star Reactor",
        "Dome 3 First Orbit Galaxy" : "Sea Slide Galaxy",
        "Dome 3 Second Orbit Galaxy": "Sling Pod Galaxy",
        "Dome 3 Third Orbit Galaxy" : "Melty Molten Galaxy",
        "Dome 3 Fourth Orbit Galaxy": "Snow Cap Galaxy",
        "Dome 4 First Orbit Galaxy" : "Ghostly Galaxy",
        "Dome 4 Second Orbit Galaxy": "Dreadnought Galaxy",
        "Dome 4 Third Orbit Galaxy" : "Gusty Garden Galaxy",
        "Dome 4 Fourth Orbit Galaxy": "Loopdeeswoop Galaxy",
        "Dome 5 First Orbit Galaxy" : "Toy Time Galaxy",
        "Dome 5 Second Orbit Galaxy": "Space Junk Galaxy",
        "Dome 5 Third Orbit Galaxy" : "Deep Dark Galaxy",
        "Dome 5 Fourth Orbit Galaxy": "Gateway Galaxy",
        "Dome 6 First Orbit Galaxy" : "Gold Leaf Galaxy",
        "Dome 6 Second Orbit Galaxy": "Beach Bowl Galaxy",
        "Dome 6 Third Orbit Galaxy" : "Rolling Green Galaxy",
        "Dome 6 Fourth Orbit Galaxy": "Freezeflame Galaxy",
        "Sweet Sweet Hungry Luma"   : "Flipswitch Galaxy",
        "Sling Pod Hungry Luma"     : "Drip Drop Galaxy",
        "Drip Drop Hungry Luma"     : "Matter Splatter Galaxy",
        "Bigmouth Hungry Luma"      : "Bowser Jr.'s Robot Reactor",
        "Sand Spiral Hungry Luma"   : "Hurry-Scurry Galaxy",
        "Snow Cap Hungry Luma"      : "Bowser Jr.'s Lava Reactor",
        "Gateway Dome"              : "Sweet Sweet Galaxy",
        "Boo's Boneyard Hungry Luma": "Bubble Breeze Galaxy",
        "Rolling Gizmo Launch Star" : "Bigmouth Galaxy",
        "Loopdeeswoop Launch Star"  : "Boo's Boneyard Galaxy",
        "Bubble Blast Launch Star"  : "Bubble Blast Galaxy",
        "Dome 1 Fifth Orbit Galaxy" : "Bowser Jr.'s Airship Armada",
        "Dome 2 Fifth Orbit Galaxy" : "Rolling Gizmo Galaxy",
        "Dome 3 Fifth Orbit Galaxy" : "Buoy Base Galaxy",
        "Dome 4 Fifth Orbit Galaxy" : "Bonefin Galaxy",
        "Dome 5 Fifth Orbit Galaxy" : "Sand Spiral Galaxy"}

Galaxy_Counts = {"D1G1": 0,
                 "D1G2": 0,
                 "D1G3": 1,
                 "D1G4": 0,
                 "D1G5": 0,
                 "D2G1": 8,
                 "D2G2": 9,
                 "D2G3": 3,
                 "D2G4": 10,
                 "D2G5": 4,
                 "D3G1": 20,
                 "D3G2": 12,
                 "D3G3": 15,
                 "D3G4": 12,
                 "D3G5": 18,
                 "D4G1": 20,
                 "D4G2": 20,
                 "D4G3": 20,
                 "D4G4": 22,
                 "D4G5": 20,
                 "D5G1": 31,
                 "D5G2": 26,
                 "D5G3": 22,
                 "D5G4": 22,
                 "D5G5": 22,
                 "D6G1": 31,
                 "D6G2": 31,
                 "D6G3": 31,
                 "D6G4": 49}

converter = {"First" : 1,
             "Second": 2,
             "Third" : 3,
             "Fourth": 4,
             "Fifth" : 5}

def change_galaxies(astrodome: RARC, dol: DOL, galaxies: dict[str, str]):
    mini_to_surp_galaxies = {}
    mini_to_mini_galaxies = {}

    old_galaxies = [[] for i in range(6)]
    new_galaxies = [[] for i in range(6)]
    values = [[] for i in range(6)]

    for location in galaxies.keys():
        default_galaxy = default_galaxies[location]
        new_galaxy = galaxies[location]
        
        if 'Gateway' in location or 'Gateway' in new_galaxy:
            continue
        elif location.startswith("Dome"):
            dome_index = int(location[5]) - 1
            orbit_index = converter[location[7:-13]] - 1
            old_galaxy = galaxy_to_miniature[default_galaxy]

            print(miniature_to_galaxy[old_galaxy] + ' -> ' + new_galaxy)
            
            if new_galaxy in major_galaxies:
                obj_arg0 = 0
            elif new_galaxy in minor_galaxies:
                obj_arg0 = 1
            elif new_galaxy in boss_galaxies:
                obj_arg0 = 2

            new_galaxy = galaxy_to_miniature[new_galaxy]
            
            if new_galaxy.startswith('Surp'):
                mini_to_surp_galaxies[old_galaxy] = new_galaxy
            else:
                mini_to_mini_galaxies[old_galaxy] = new_galaxy

            old_galaxies[dome_index].append(old_galaxy)
            new_galaxies[dome_index].append(new_galaxy)
            values[dome_index].append((orbit_index << 16) | obj_arg0)
    
    change_dome_miniature(astrodome, old_galaxies, new_galaxies, values)
    
    old_galaxies = list(mini_to_mini_galaxies.keys())
    new_galaxies = list(mini_to_mini_galaxies.values())
    adjust_nameobjfactory_table(dol, old_galaxies, new_galaxies)
    replace_miniatures(dol, iso.temp_dir + "/DATA/files/ObjectData/", mini_to_surp_galaxies)

def update_gameeventflagtable(dol: DOL):
    address = 0x8053bbd0
    ch_dol.write_to_dol(dol, address, b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def update_star_requirements(dol: DOL, example_input, galaxy_counts):
    begin_address = 0x8053c800
    end_address = 0x8053d520
    size = end_address - begin_address

    bcsv_data = ch_dol.read_from_dol(dol, begin_address, size)
    bcsv = BCSV(BytesIO(bcsv_data))
    
    opencondition0_index = bcsv.get_field_index("OpenCondition0")
    opencondition1_index = bcsv.get_field_index("OpenCondition1")
    powerstarnum_index = bcsv.get_field_index("PowerStarNum")
    grandgalaxyno_index = bcsv.get_field_index("GrandGalaxyNo")

    for location, galaxy in example_input.items():
        if 'Gateway' in galaxy:
            continue
        entry_name = galaxy_to_miniature[galaxy][4:]
        entry_index = bcsv.get_entry_index_by_name(entry_name)

        if location.startswith('Dome'):
            dome_index = int(location[5])
            orbit_index = converter[location[7:-13]]

            star_requirement_key = 'D' + str(dome_index) + 'G' + str(orbit_index)
            star_requirement = galaxy_counts[star_requirement_key]

            bcsv.set_value_by_index(entry_index, opencondition0_index, f"SpecialStarGrand{dome_index}")
            bcsv.set_value_by_index(entry_index, opencondition1_index, '')
            bcsv.set_value_by_index(entry_index, powerstarnum_index, star_requirement)
            bcsv.set_value_by_index(entry_index, grandgalaxyno_index, dome_index)
    
    bcsv.save_changes()
    if bcsv.data.seek(0,2) > size:
        raise ValueError(f"BCSV has gotten too big. Max allowed size: {size}, current size: {bcsv.data.seek(0,2)}")
    ch_dol.write_to_dol(dol, begin_address, bcsv.data.getvalue(), verbose=False)
    for entry in bcsv.entries:
        print(entry)

def update_dol(dol: DOL, example_input, galaxy_counts):
    # Overwrite calculating miniature galaxy index
    # Ignore arg0 for koopa model
    address = 0x801ffc44
    old_instruction = b'\x80\x03\x00\x8c'
    new_instruction = b'\x38\x00\x00\x02'
    ch_dol.replace_instruction(dol, address, old_instruction, new_instruction)

    # Get obj_arg0 from miniature galaxy
    address = 0x80200758
    old_instruction = b'\x7f\xe4\xfb\x78'
    new_instruction = b'\x80\x7f\x00\x8c'
    ch_dol.replace_instruction(dol, address, old_instruction, new_instruction)

    # Shift 16 bits to the right to get the custom index
    address = 0x8020075c
    old_instruction = b'\x4b\xff\xfe\x01'
    new_instruction = b'\x54\x63\x84\x3e'
    ch_dol.replace_instruction(dol, address, old_instruction, new_instruction)
    update_star_requirements(dol, example_input, galaxy_counts)
    update_gameeventflagtable(dol)

def update_iso(iso: WiiISO, example_input, galaxy_counts):
    mario_file = iso.temp_dir + "/DATA/files/ObjectData/Mario.arc"
    mario = RARC(mario_file)
    
    change_mario_colours(mario, 'Hat', (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    change_mario_colours(mario, 'Overalls', (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    with open(mario_file, 'wb') as f:
        f.write(Yaz0.compress(mario.data).getvalue())
    
    # Get the AstroDome file from the ISO
    astrodome_file = iso.temp_dir + "/DATA/files/StageData/AstroDome.arc"
    astrodome = RARC(astrodome_file)
    
    dol_path = iso.temp_dir + "/DATA/sys/main.dol"
    dol = ch_dol.get_dol(dol_path)

    change_galaxies(astrodome, dol, example_input)
    astrodome.save_changes()

    with open(astrodome_file, 'wb') as f:
        f.write(Yaz0.compress(astrodome.data).getvalue())
    
    update_dol(dol, example_input, galaxy_counts)
    dol.save_changes()

if __name__ == '__main__':
    base_path = r"worlds/smgalaxy/Patch/"
    iso_path = base_path + "Super Mario Galaxy (USA) (En,Fr,Es).iso"
    iso = WiiISO(iso_path, dest_path=base_path, temp_dir=base_path + "temp")
    
    
    #iso.verify_base_rom()
    iso.extract()

    update_iso(iso, example_input, Galaxy_Counts)

    iso.repack(delete=True, verbose=False)
    