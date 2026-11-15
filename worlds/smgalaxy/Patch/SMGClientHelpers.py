from typing import NamedTuple

from ..regions import region_list
from ..Constants.Names import region_names as regname

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int | None
    orbit_index: int | None
    old_luma_name: str | None
    patch_test_old_name: str
    patch_test_new_name: str


almost_full_shuffle = {
    "Dome 1 First Orbit Galaxy": "Good Egg Galaxy",
    "Dome 2 First Orbit Galaxy": "Space Junk Galaxy",
    "Dome 3 First Orbit Galaxy": "Beach Bowl Galaxy",
    "Dome 4 First Orbit Galaxy": "Gusty Garden Galaxy",
    "Dome 5 First Orbit Galaxy": "Gold Leaf Galaxy",
    "Dome 6 First Orbit Galaxy": "Deep Dark Galaxy",
    "Dome 1 Second Orbit Galaxy": "Honeyhive Galaxy",
    "Dome 2 Third Orbit Galaxy": "Battlerock Galaxy",
    "Dome 3 Third Orbit Galaxy": "Ghostly Galaxy",
    "Dome 4 Second Orbit Galaxy": "Freezeflame Galaxy",
    "Dome 5 Second Orbit Galaxy": "Sea Slide Galaxy",
    "Dome 6 Second Orbit Galaxy": "Dreadnought Galaxy",
    "Dome 4 Third Orbit Galaxy": "Dusty Dune Galaxy",
    "Dome 5 Third Orbit Galaxy": "Toy Time Galaxy",
    "Dome 6 Fourth Orbit Galaxy": "Melty Molten Galaxy",
    "Dome 1 Third Orbit Galaxy": "Loopdeeloop Galaxy",
    "Dome 2 Second Orbit Galaxy": "Rolling Green Galaxy",
    "Dome 3 Second Orbit Galaxy": "Bubble Breeze Galaxy",
    "Dome 4 Fourth Orbit Galaxy": "Honeyclimb Galaxy",
    "Dome 5 Fourth Orbit Galaxy": "Bonefin Galaxy",
    "Dome 6 Third Orbit Galaxy": "Matter Splatter Galaxy",
    "Dome 1 Fourth Orbit Galaxy": "Flipswitch Galaxy",
    "Dome 2 Fourth Orbit Galaxy": "Hurry-Scurry Galaxy",
    "Dome 3 Fourth Orbit Galaxy": "Buoy Base Galaxy",
    "Sweet Sweet Hungry Luma": "Sand Spiral Galaxy",
    "Sling Pod Hungry Luma": "Gateway Galaxy",
    "Drip Drop Hungry Luma": "Sling Pod Galaxy",
    "Bigmouth Hungry Luma": "Bigmouth Galaxy",
    "Sand Spiral Hungry Luma": "Bubble Blast Galaxy",
    "Snow Cap Hungry Luma": "Snow Cap Galaxy",
    "Gateway Dome": "Drip Drop Galaxy",
    "Boo's Boneyard Hungry Luma": "Rolling Gizmo Galaxy",
    "Rolling Gizmo Launch Star": "Sweet Sweet Galaxy",
    "Loopdeeswoop Launch Star": "Loopdeeswoop Galaxy",
    "Bubble Blast Launch Star": "Boo's Boneyard Galaxy",
    "Dome 1 Fifth Orbit Galaxy": "Bowser Jr.'s Robot Reactor",
    "Dome 2 Fifth Orbit Galaxy": "Bowser's Star Reactor",
    "Dome 3 Fifth Orbit Galaxy": "Bowser Jr.'s Airship Armada",
    "Dome 4 Fifth Orbit Galaxy": "Bowser's Dark Matter Plant",
    "Dome 5 Fifth Orbit Galaxy": "Bowser Jr.'s Lava Reactor"
}


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

                new_galaxy = GalaxyDestination(galaxy, "dome", dome_index, orbit_index, None, region_list[almost_full_shuffle[location]].in_game_name, galaxy)

            elif location.startswith("Gateway"):
                new_galaxy = GalaxyDestination(galaxy, "gateway", None, None, None, region_list[almost_full_shuffle[location]].in_game_name, galaxy)

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

                new_galaxy = GalaxyDestination(galaxy, "luma", dome_index, None, region_list[luma_name].in_game_name, region_list[almost_full_shuffle[location]].in_game_name, galaxy)

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

                new_galaxy = GalaxyDestination(galaxy, "luma", None, orbit_index, region_list[luma_name].in_game_name, region_list[almost_full_shuffle[location]].in_game_name, galaxy)

            self.galaxy_destinations.append(new_galaxy)
