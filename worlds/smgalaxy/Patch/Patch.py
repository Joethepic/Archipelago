import zipfile, json
from typing import NamedTuple

from wiithon import WiiIsoPatcher
from wiithon.formats.dol import DOL
from wiithon.ppc import instructions as PPC

from worlds.Files import APAutoPatchInterface, APPlayerContainer, AutoPatchRegister
from NetUtils import convert_to_base_types

from worlds.smgalaxy.Constants.patch_constants import GATEWAY_ENTRANCE_ADDRESS, GATEWAY_EXIT_ADDRESS
from worlds.smgalaxy.Patch.extensions import SMGObject

from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGObjects.AstroDomeEntrances import AstroDomeEntrances
from .SMGObjects.PowerStar import PowerStar
from .SMGStages.AstroDome import AstroDomes
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy
from ..regions import region_list
from ..SMGSettings import get_base_rom_path
from ..Constants.constants import GAME_NAME
from ..Constants.Names import region_names as regname

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

            elif "Hungry Luma" in location:
                luma_name: str = location.replace("Hungry Luma", "Galaxy")

                if luma_name == regname.SWEETSWEET:
                    dome_index = 0
                elif luma_name == regname.SLINGPOD:
                    dome_index = 1
                elif luma_name == regname.DRIPDROP:
                    dome_index = 2
                elif luma_name == regname.BOOBONE:
                    dome_index = 3
                elif luma_name == regname.SNOWCAP:
                    dome_index = 4
                elif luma_name == regname.SANDSPIRAL:
                    dome_index = 5
                elif luma_name == regname.BIGMOUTH:
                    dome_index = 6

                new_galaxy = GalaxyDestination(galaxy, "luma", dome_index, None, region_list[luma_name].in_game_name)

            elif "Launch Star" in location:
                luma_name: str = location.replace("Launch Star", "Galaxy")

                if luma_name == regname.ROLLINGGIZ:
                    orbit_index = 0
                elif luma_name == regname.LOOPDEESWOOP:
                    orbit_index = 1
                elif luma_name == regname.BUBBLEBLAST:
                    orbit_index = 2
                elif luma_name == regname.FINALE:
                    orbit_index = 3

                new_galaxy = GalaxyDestination(galaxy, "luma", None, orbit_index, region_list[luma_name].in_game_name)

            self.galaxy_destinations.append(new_galaxy)

class Patch:
    seed: int
    dol: SMGDOL
    counts: dict[str, int]
    galaxies: dict[str, str]
    mario_colours: dict[str, str]
    dome_shuffle: dict[str, str]
    old_galaxies: list
    new_galaxies: list

    objects: dict[str, SMGObject]

    def __init__(self, patcher: WiiIsoPatcher, output: dict):
        self.seed = int(output["Seed"])

        self.counts: dict[str, int] = output['Galaxy Counts']
        self.galaxies: dict[str, str] = output['Galaxies']
        self.locations: dict = output['Locations']
        self.slot_name: str = output["Name"]

        # Options
        self.mario_colours: dict[str, str] = output['Options']['mario_colors']
        self.dome_shuffle: dict[str, str] = output['Options']['dome_shuffle']
        self.show_galaxies: int = output['Options']['hide_galaxy']

        self.old_galaxies: list = list(self.galaxies.keys())
        self.new_galaxies: list = list(self.galaxies.values())

        SMGObject.patcher = patcher

        self.objects = {
            "Mario": Mario(),
            "AstroGalaxy": AstroGalaxy(),
            "AstroDomeScenario": AstroDomeScenario(),
            "AstroDomes": AstroDomes(),
            "AstroDomeEntrances": AstroDomeEntrances(),
            "PowerStar": PowerStar()
        }

    def update(self, galaxy_shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int], luma_shuffle: list[GalaxyDestination]) -> None:
        for object_name, object in self.objects.items():
            print(f"Updating {object_name}")

            object.update(mario_colours=self.mario_colours,
                          galaxy_shuffle=galaxy_shuffle,
                          dome_shuffle=dome_shuffle,
                          luma_shuffle=luma_shuffle,
                          show_galaxies=self.show_galaxies)

    def build_dol(self, dol: DOL) -> None:
        self.dol = SMGDOL(dol)

    def update_dol(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination], dome_shuffle: dict[int, int], star_requirements: dict[str, int], gateway_galaxy: GalaxyDestination):
        self.dol.update(dome_galaxies=dome_galaxies,
                        luma_galaxies=luma_galaxies,
                        dome_shuffle=dome_shuffle,
                        star_requirements=star_requirements,
                        locations=self.locations,
                        show_galaxies=self.show_galaxies,
                        slot_name=self.slot_name)

        galaxy_name = gateway_galaxy.name
        if galaxy_name == "HeavensDoorGalaxy":
            return
    
        mini_galaxy = self.dol.objects["NameObjectFactory"].create_mgr.get_create_funcs_by_name("Mini" + galaxy_name)
        surp_galaxy = self.dol.objects["NameObjectFactory"].create_mgr.get_create_funcs_by_name("Surp" + galaxy_name)

        if mini_galaxy:
            name_address = mini_galaxy[0].name.pointing_address
        elif surp_galaxy:
            name_address = surp_galaxy[0].name.pointing_address
        else:
            raise ValueError(f"{galaxy_name} cannot be found.")

        print(f"Loading zone Gateway -> {galaxy_name}")

        # +4 to the name address to skip over the galaxy identifier tag (Mini/Surp)
        name_address += 4
        
        upper_bytes: int = name_address >> 16
        lower_bytes: int = name_address & 0xFFFF

        self.dol.write_instruction(PPC.lis(3, upper_bytes), GATEWAY_ENTRANCE_ADDRESS)
        self.dol.write_instruction(PPC.ori(3, 3, lower_bytes))


        self.dol.write_instruction(PPC.lis(3, upper_bytes), GATEWAY_EXIT_ADDRESS)
        self.dol.write_instruction(PPC.ori(3, 3, lower_bytes))
        
        
class SuperMarioGalaxyRandomiser(APAutoPatchInterface, metaclass=AutoPatchRegister):
    game = GAME_NAME
    patch_file_ending = ".apsmg"
    result_file_ending = ".iso"
    input_path: str

    def __init__(self, apsmg_path: str):
        super().__init__()
        self.input_path = apsmg_path

    def patch(self, target: str) -> None:
        vanilla_rom_path = get_base_rom_path()

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

            def dol_patch(dol: DOL):
                patch.build_dol(dol)
                patch.update_dol(dome_galaxies, luma_galaxies, dome_shuffle, galaxy_counts, gateway_galaxy)

            patcher.patch_dol(dol_patch)

            print("Starting building...")

            patcher.build(target)
        

class SMGPlayerContainer(APPlayerContainer):
    game = GAME_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsmg"

    def __init__(self, player_choices: dict, input_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(input_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.json", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)
