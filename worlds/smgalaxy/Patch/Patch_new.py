import hashlib, zipfile, json
from typing import NamedTuple

from wiithon import WiiIsoPatcher

from worlds.Files import APAutoPatchInterface, APPlayerContainer, AutoPatchRegister
from NetUtils import convert_to_base_types

from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGObjects.AstroDomeEntrances import AstroDomeEntrances
from .SMGStages.AstroDome import AstroDome
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy
from ..regions import region_list
from ..SMGSettings import get_base_rom_path

class InvalidCleanISOError(Exception): pass

# Name of the game, which is used in various error messaging.
RANDOMIZER_NAME: str = "Super Mario Galaxy"

# Can pull this from dolphin or a cmd command / bash command
CLEAN_MD5: int = 0xf99a97f9ae4dccd1db45e9aaab9cebd8

# Expected Game ID of the GC/Wii game we expect here.
EXPECTED_GAME_ID: str = "RMGE01"


def verify_base_rom(clean_iso_path: str):
    """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
    of the file matches against the one we expect, and third, we had a game id in the file that matches the games
    official one"""
    # Verifies we have a valid installation of Super Mario Galaxy USA. There are some regional file differences.
    print(f"Verifying if the provided ISO is a valid copy of {RANDOMIZER_NAME}...")

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

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int | None
    orbit_index: int | None
    old_luma_name: str | None

class GalaxyShuffle:
    converter = {"First" : 1,
                 "Second": 2,
                 "Third" : 3,
                 "Fourth": 4,
                 "Fifth" : 5}
    galaxy_destinations: list[GalaxyDestination]
    
    def __init__(self, galaxies: dict[str, str]):
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
                
                new_galaxy = GalaxyDestination(galaxy, "dome", dome_index, orbit_index, None)

            elif location.startswith("Gateway"):
                new_galaxy = GalaxyDestination(galaxy, "gateway", None, None, None)

            else:
                luma_name: str = location.replace("Hungry Luma", "Galaxy").replace("Launch Star", "Galaxy")
                new_galaxy = GalaxyDestination(galaxy, "luma", None, None, region_list[luma_name].in_game_name)
            
            self.galaxy_destinations.append(new_galaxy)

class Patch:
    seed: int
    counts: dict[str, int]
    galaxies: dict[str, str]
    mario_colours: dict[str, str]
    dome_shuffle: dict[str, str]
    old_galaxies: list
    new_galaxies: list

    def __init__(self, patcher: WiiIsoPatcher, output: dict):
        self.seed = int(output["Seed"])
        self.dol: SMGDOL = SMGDOL(patcher)

        self.counts: dict[str, int] = output['Galaxy Counts']
        self.galaxies: dict[str, str] = output['Galaxies']
        self.mario_colours: dict[str, str] = output['Options']['mario_colors']
        self.dome_shuffle: dict[str, str] = output['Options']['dome_shuffle']

        self.old_galaxies: list = list(self.galaxies.keys())
        self.new_galaxies: list = list(self.galaxies.values())

        self.mario: Mario = Mario(patcher)
        self.astrogalaxy: AstroGalaxy = AstroGalaxy(patcher)
        self.astrodomescenario: AstroDomeScenario = AstroDomeScenario(patcher)
        self.astrodome: AstroDome = AstroDome(patcher, self.dol)
        self.astrodomeentrances: AstroDomeEntrances = AstroDomeEntrances(patcher)

    def update(self, galaxy_shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int], luma_shuffle: list[GalaxyDestination]) -> None:
        self.mario.update(self.mario_colours)

        self.astrogalaxy.update(luma_shuffle)

        self.astrodomescenario.update(dome_shuffle)

        for index in range(1, 7):
            self.astrodome.update([galaxy for galaxy in galaxy_shuffle if galaxy.dome_index == index], index, dome_shuffle[index])

        self.astrodomeentrances.update(dome_shuffle)

    def update_gateway_location(self, gateway_galaxy: GalaxyDestination) -> None:
        galaxy_name = gateway_galaxy.name
        if galaxy_name == "HeavensDoorGalaxy":
            return
        
        mini_galaxy = self.dol.name_object_factory.get_name_to_create_function_elements_by_name("Mini" + galaxy_name)
        surp_galaxy = self.dol.name_object_factory.get_name_to_create_function_elements_by_name("Surp" + galaxy_name)

        if mini_galaxy:
            name_address = mini_galaxy[0].name_pointer.pointing_address
        elif surp_galaxy:
            name_address = surp_galaxy[0].name_pointer.pointing_address
        else:
            raise ValueError(f"{galaxy_name} cannot be found.")

        print(f"Loading zone gateway -> {galaxy_name}")

        # +4 to the name address to skip over the galaxy identifier tag (Mini/Surp)
        self.astrodome.gateway_galaxy.replace_loading(name_address + 4)
        return

    def update_nameobjfactory(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination]) -> None:
        dome_galaxy_names = [galaxy.name for galaxy in dome_galaxies]
        luma_galaxy_names = [galaxy.name for galaxy in luma_galaxies]
        
        self.dol.set_name_object_factory_galaxies(dome_galaxy_names, luma_galaxy_names)

    def update_galaxyunlocktable(self, dome_galaxies: list[GalaxyDestination], star_requirements: dict[str, int]) -> None:
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1,7)}
        
        for location, requirement in star_requirements.items():
            dome_index: int = int(location[1])
            orbit_index: int = int(location[3:])

            requirements[dome_index][orbit_index] = requirement
        
        for galaxy in dome_galaxies:
            star_requirement: int = requirements[galaxy.dome_index][galaxy.orbit_index + 1]

            entry = self.dol.get_galaxy_unlock_table_entry_by_name(galaxy.name)
            entry.power_star_requirement = star_requirement
            entry.return_dome = galaxy.dome_index
            self.dol.galaxy_unlock_table.set_entry(entry)

    def update_instructions(self) -> None:
        #######################################################
        # Skip opening cutscene and go immediately to gateway #
        #######################################################
        address = 0x803bb3cc
        new_instruction = b'\x38\x60\x00\x00'
        self.dol.dol.write_at(address, new_instruction)
        
        address = 0x803bb3d8
        new_instruction = b'\x38\x7f\x03\xf8'
        self.dol.dol.write_at(address, new_instruction)

        address = 0x803bb3dc
        new_instruction = b'\x38\x00\x00\x04'
        self.dol.dol.write_at(address, new_instruction)

        ########################
        # Set swing permission #
        ########################
        address = 0x803b55b0
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.dol.write_at(address, new_instruction)
                                
        #####################################################
        # TEMPORARY TEMPORARY TEMPORARY TEMPORARY TEMPORARY #
        #####################################################
        self.dol.dol.write_at(0x8053bb44, (1).to_bytes(1, "big"))
        self.dol.dol.write_at(0x8053bb46, (0).to_bytes(1, "big"))

        #######################################
        # Miniature galaxy orbit manipulation #
        #######################################
        # Get obj_arg0 from miniature galaxy
        address = 0x80200758
        new_instruction = b'\x80\x7f\x00\x8c'
        self.dol.dol.write_at(address, new_instruction)

        # Shift 16 bits to the right to get the upper bits where the custom index is stored
        address = 0x8020075c
        new_instruction = b'\x54\x63\x84\x3e'
        self.dol.dol.write_at(address, new_instruction)

        ################################
        # Scenario select star loading #
        ################################
        # Keep loading regular stars even if they're not available yet
        address = 0x8037d9ec
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.dol.write_at(address, new_instruction)

        # Calculate all secret/comet stars, including possibly normally unavailable ones
        address = 0x8037da44
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.dol.write_at(address, new_instruction)

        # Show secret/comet stars as calculated above
        address = 0x8037db54
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.dol.write_at(address, new_instruction)

        # Set visibility to 1 (not collected) if appearing as collected has failed (ensuring it shows up even if not available)
        address = 0x8037db18
        new_instruction = b'\x38\xc0\x00\x01'
        self.dol.dol.write_at(address, new_instruction)

        # Always show up and appear correctly as collected/not collected
        address = 0x8037db74
        new_instruction = b'\x38\xc6\x00\x01'
        self.dol.dol.write_at(address, new_instruction)
        
        #######################################
        # Read star count from memory address #
        #######################################
        # Load upper 2 bytes of memory pointer (0x8000)
        address = 0x803b10fc
        new_instruction = b'\x3f\x80\x80\x00'
        self.dol.dol.write_at(address, new_instruction)

        # Load lower 2 bytes of memory pointer (0x1880), and load the byte at 0x80001880 into r3
        address = 0x803b1100
        new_instruction = b'\x88\x7c\x18\x80'
        self.dol.dol.write_at(address, new_instruction)

        # Skip the rest of the normal function
        address = 0x803b1104
        new_instruction = b'\x48\x00\x00\x38'
        self.dol.dol.write_at(address, new_instruction)

        ###################################
        # Custom powerstar colour loading #
        ###################################
        address = 0x8020f270
        new_instruction = b'\x7c\x7f\x1b\x78\x48\x1e\x68\x45\x7c\x64\x1b\x78\x48\x1a\x12\xc9\x80\x63\x00\x0c\x48\x1a\x21\x0d\x3c\x80\x80\x00\x60\x84\x18\xff\x1c\x63\x00\x08\x7c\x63\x22\x14\x7c\x63\xf8\xae'
        self.dol.dol.write_at(address, new_instruction)

        ##################################
        # Custom grandstar count loading #
        ##################################
        address = 0x803b1d10
        new_instruction = b'\x3c\x60\x80\x00\x88\x63\x18\x82\x38\x63\x00\x01\x7c\x03\x20\x00\x41\x80\x00\x0c\x38\x60\x00\x01\x42\x80\x00\x08\x38\x60\x00\x00\x60\x00\x00\x00\x60\x00\x00\x00\x60\x00\x00\x00\x60\x00\x00\x00\x60\x00\x00\x00'
        #self.dol.dol.write_at(address, new_instruction)

        #########################
        # Skip wii strap screen #
        #########################
        address = 0x80340408
        new_instruction = b'\x38\x8d\xcf\x80'
        self.dol.dol.write_at(address, new_instruction)

        address = 0x803406ac
        new_instruction = b'\x38\x80\x00\x00'
        self.dol.dol.write_at(address, new_instruction)

        address = 0x803406d0
        new_instruction = b'\x38\x80\x00\x00'
        self.dol.dol.write_at(address, new_instruction)

        #################################################
        # Show the bros button to select Mario or Luigi #
        #################################################
        address = 0x8017cd70
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.dol.write_at(address, new_instruction)

        ####################
        # Custom Functions #
        ####################
        # Jump to custom section
        address = 0x803995c0
        new_instruction = b'\x48\x31\x49\xd1'
        self.dol.dol.write_at(address, new_instruction)
        self.dol.save()
        

class SuperMarioGalaxyRandomiser(APAutoPatchInterface, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    patch_file_ending = ".apsmg"
    result_file_ending = ".iso"
    input_path: str

    def __init__(self, apsmg_path: str):
        super().__init__()
        self.input_path = apsmg_path

    def patch(self, target: str) -> None:
        vanilla_rom_path = get_base_rom_path()
        verify_base_rom(vanilla_rom_path)

        with WiiIsoPatcher(vanilla_rom_path) as patcher:
            # Get the data from the generated output to use for patching
            with zipfile.ZipFile(self.input_path, "r") as zf:
                output = json.loads(zf.read("patch.json").decode('shift-jis'))

            patch = Patch(patcher, output)

            galaxies: dict[str, str] = patch.galaxies
            galaxy_counts: dict[str, int] = patch.counts
            dome_shuffle = {i: int(patch.dome_shuffle[f"Dome {i}"].removeprefix("Dome ")) for i in range(1,7)}

            galaxy_shuffle: list[GalaxyDestination] = GalaxyShuffle(galaxies).galaxy_destinations

            dome_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "dome"]
            luma_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "luma"]
            gateway_galaxy = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "gateway"][0]

            patch.update(dome_galaxies, dome_shuffle, luma_galaxies)

            patch.update_gateway_location(gateway_galaxy)

            patch.update_nameobjfactory(dome_galaxies, luma_galaxies)
            patch.update_galaxyunlocktable(dome_galaxies, galaxy_counts)
            patch.update_instructions()

            patcher.build(target)
        

class SMGPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsmg"

    def __init__(self, player_choices: dict, input_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(input_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.json", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

if __name__ == "__main__":
    patch_path = r"C:/Users/sebas/Documents/GitHub/Archipelago/output/AP_91073106683428351458_P1_Player1.apsmg"
    
    #SuperMarioGalaxyRandomiser.patch(patch_path)
