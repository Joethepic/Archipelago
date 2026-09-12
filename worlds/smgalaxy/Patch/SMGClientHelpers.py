from typing import NamedTuple

from ..regions import region_list
from ..Constants.Names import region_names as regname

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int | None
    orbit_index: int | None
    old_luma_name: str | None


class GalaxyShuffle:
    converter = {"First": 1,
                 "Second": 2,
                 "Third": 3,
                 "Fourth": 4,
                 "Fifth": 5}
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
