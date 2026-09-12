from wiithon import WiiIsoPatcher
from wiithon.formats.dol import DOL
from wiithon.ppc import instructions as PPC

from ..Constants.patch_constants import GATEWAY_ENTRANCE_ADDRESS, GATEWAY_EXIT_ADDRESS
from ..Patch.extensions import SMGObject

from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGObjects.AstroDomeEntrances import AstroDomeEntrances
from .SMGObjects.PowerStar import PowerStar
from .SMGStages.AstroDome import AstroDomes
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy
from .SMGClientHelpers import GalaxyDestination

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
        self.star_colours: int = output['Options']['star_colors']

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
                        slot_name=self.slot_name,
                        hide_star_colours=self.star_colours)

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

