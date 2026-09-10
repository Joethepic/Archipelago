import os
from dataclasses import fields
from typing import ClassVar
from Utils import visualize_regions
from entrance_rando import randomize_entrances
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
import typing
import logging

from . import items, regions, Rules, web_world, SMGOptions
from .Constants.Names import region_names as regname, item_names as itemname, location_names as locname
from .Constants.constants import AP_WORLD_VERSION_NAME, CLIENT_VERSION, GAME_NAME
from .Rules import rules_from_er_placements
from .locations import LOCATION_NAME_TO_ID, get_location_names_per_category, SMGLocation, location_table
from .items import SMGItem, ITEM_NAME_TO_ID, get_item_names_per_category, all_items_table
from .regions import disconnect_from_option, region_list, SMGRegionData, galaxies_list
from .SMGSettings import SuperMarioGalaxy
from .Patch.Patch import SMGPlayerContainer

def runClient(*args):
    from .SMGClient import launch
    launch_subprocess(launch, name = "SMG Client", args = args)

components.append(Component("SMG Client", func=runClient, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsmg")))

class SMGWorld(World):
    """
    Super Mario Galaxy allows you to explore the cosmos with Rosalina in the Comet Observatory.
    Mario must collect Power Stars and Grand Stars to power the observatory so it can go to the
    center of the universe in order to save Princess Peach from Bowser's clutches.
    """

    game = GAME_NAME
    topology_present = True
    
    web = web_world.SMGWebWorld()
    
    #option definitions
    options_dataclass = SMGOptions.SMGOptions
    options: SMGOptions.SMGOptions
    settings: ClassVar[SuperMarioGalaxy]

    item_name_to_id: ClassVar[dict[str, int]] = ITEM_NAME_TO_ID
    location_name_to_id: ClassVar[dict[str, int]] = LOCATION_NAME_TO_ID

    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    required_client_version = (0, 6, 6)

    hint_blacklist = {"B: Bowser's Galaxy Reactor", "Peach"}

    def __init__(self, *args, **kwargs):
        super(SMGWorld, self).__init__(*args, **kwargs)
        self.origin_region_name: str = regname.SHIP
        self.shuffled_levels: dict[str, str] = {} # Entrance Name (Galaxy Slot): Region name (Galaxy)
        self.starting_galaxy: str = regname.GOODEGG
        self.galaxy_counts: dict[str, int] = {}

    def generate_early(self) -> None:
        self.galaxy_counts = self.get_galaxy_counts()

        if "Random" in self.options.mario_colors.value.keys():
            self.options.mario_colors.value = {
                "Hat": self.random.choice(sorted(self.options.mario_colors.valid_values)),
                "Overalls": self.random.choice(sorted(self.options.mario_colors.valid_values)),
                "Shoes": self.random.choice(sorted(self.options.mario_colors.valid_values)),
                "Gloves": self.random.choice(sorted(self.options.mario_colors.valid_values))
            }
        for key in self.options.mario_colors.valid_keys:
            if key == "Random":
                continue
            if key not in self.options.mario_colors.value.keys():
                self.options.mario_colors.value.update({key: self.random.choice(sorted(self.options.mario_colors.valid_values))})

    def create_regions(self):
        regions.create_regions(self)

    def get_galaxy_counts(self) -> dict[str, int]:
        """Gets all the required galaxy required counts for each dome number and galaxies within that dome."""
        stupid_word_dict: dict[str, int] = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        galaxy_counts: dict[str, int] = {}
        previous_dome_count: int = 0
        previous_orbit_count: int = 0
        for dome_name, dome_num in stupid_word_dict.items():
            # Get each set of dome offsets for each dome
            dome_dict: dict = dict(sorted(dict(getattr(self.options, f"dome_{dome_name}_counts").value).items(),
                                          key=lambda item: item[1]))
            # Each dome offset needs to account for the previous dome's max count. In the case of Dome 1, return 0
            if dome_num != 1:
                previous_dome_count = max([d_val for d_key, d_val in galaxy_counts.items() if f"D{dome_num - 1}" in d_key])
            # Gets the list of all the option counter names from the current option's value
            dome_orbits: list[str] = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]

            for i, dome_orb_name in enumerate(dome_orbits):
                if not dome_orb_name in dome_dict.keys():
                    print(f"Dome {dome_name} did not have orbit name: {dome_orb_name}")

                    # If the first dome, First Orbit would never exist
                    # IF the last dome, Fourth Orbit will never exist
                    if dome_num == 1 and dome_orb_name == "First Orbit":
                        continue

                    # Because OptionCounters can somehow be blank entirely, just force these to have values to 0, which
                    # wouldn't need to be added to dome count.
                    if dome_name == "six" and dome_orb_name != "Fifth Orbit":
                        galaxy_counts[f"D{dome_num}G{i + 1}"] = previous_dome_count
                        continue

                    # Special case for Dome 6, as D6 will only ever have 4 galaxies total
                if dome_name == "six" and dome_orb_name == "Fifth Orbit":
                    continue
                if dome_orb_name == "First Orbit":
                    galaxy_counts[f"D{dome_num}G{i + 1}"] = previous_dome_count + int(dome_dict[dome_orb_name])
                    previous_orbit_count = previous_dome_count + int(dome_dict[dome_orb_name])
                else:
                    galaxy_counts[f"D{dome_num}G{i + 1}"] = previous_orbit_count + int(dome_dict[dome_orb_name])
                    previous_orbit_count = previous_orbit_count + int(dome_dict[dome_orb_name])

        return galaxy_counts

    def set_rules(self):
        Rules.set_rules(self, self.player)
    
    def create_item(self, name: str) -> SMGItem:
        item = items.SMGItem(name, self.player, items.all_items_table[name])
        
        return item

    def get_filler_item_name(self) -> str:
        return itemname.ONEUP
    
    def create_items(self):
        # creates the green stars in each player's itempool
        local_pool: list[SMGItem] = []
        local_pool += [self.create_item(itemname.GREEN) for i in range(3)]
        local_pool += [self.create_item(itemname.GRAND) for i in range(7)]
        self.get_location(locname.GALAXYREACTORSTAR1).place_locked_item(self.create_item("Peach"))
        self.get_location(locname.GALAXYREACTORSTAR1).address = None
        
        # make sure we don't create more stars than locations, somehow
        local_pool += [self.create_item(itemname.POWER) for i in range(self.options.stars_to_finish.value)]

        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        leftover_locations = min([109, (len(list(self.multiworld.get_unfilled_locations(self.player))) - len(local_pool))])

        # Add a random number of extra stars. Later, this can be made into an option.
        if leftover_locations >= 1:
            extra_stars: int = self.random.randint(0, leftover_locations)
        else:
            extra_stars: int = 0
        local_pool += [self.create_item(itemname.POWER) for i in range(extra_stars)]
        n_filler_items = n_locations - len(local_pool)

        # Create filler
        for _ in range(n_filler_items):
            local_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += local_pool

    def connect_entrances(self) -> None:
        if self.options.galaxy_shuffle:
            # Disconnect entrances based on options choice. Also ensures first available slot is a major galaxy
            self.starting_galaxy = disconnect_from_option(self)
            # Run randomize entrances, but do not get pairings - we craete our own method for them
            randomize_entrances(self, True, {0: [0]})
        # Apply rules to newly formed entrances based on within-world access, regardless of randomization
        rules_from_er_placements(self)

    def pre_fill(self) -> None:
        visualize_regions(self.get_region(self.origin_region_name), "SMG_region_graph.puml",show_entrance_names=True)
    # Output options, locations and doors for patcher
    def generate_output(self, output_directory: str):
        self.galaxy_counts.update({"D1G1": 0})
        # Output seed name and slot number to seed RNG in randomizer client
        output_data: dict = {
            AP_WORLD_VERSION_NAME: CLIENT_VERSION,
            "Seed": str(self.multiworld.seed_name)[:16],
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {},
            "Locations": {},
            "Galaxies": self.shuffled_levels,
            "Galaxy Counts": self.galaxy_counts,
            "Hints": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            if field.name == "plando_items":
                continue
            output_data["Options"][field.name] = getattr(self.options, field.name).value
            if isinstance(output_data["Options"][field.name], set):
                output_data["Options"][field.name] = list(output_data["Options"][field.name])
        output_data["Options"]["mario_colors"] = getattr(self.options, "mario_colors").value

        k = ["Dome 1", "Dome 2", "Dome 3", "Dome 4", "Dome 5", "Dome 6"]
        if self.options.dome_shuffle.value:
            self.random.shuffle(k)
        v = [regname.TERRACE, regname.FOUNTAIN, regname.KITCHEN, regname.BEDROOM, regname.ENGINE, regname.GARDEN]
        output_data["Options"]["dome_shuffle"] = dict(zip(k, v))

        # Output which item has been placed at each location
        for location in list(smgloc for smgloc in self.get_locations() if isinstance(smgloc, SMGLocation)):
            if location.address is None:
                continue
            if location.item.code is None:
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": self.game,
                    "classification": location.item.classification,
                    # "type": location.type,
                }
            elif location.item:
                loc_region: SMGRegionData = region_list[location.parent_region.name]
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": location.item.game,
                    "classification": location.item.classification.name,
                    #"type": location.type,
                }
            else:
                item_info = {"name": "Nothing", "game": self.game, "classification": "filler"}
            output_data["Locations"][location.name] = item_info

        # Create the patch file output in patch_file_ending format.
        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                    f"{SMGPlayerContainer.patch_file_ending}")

        player_container: SMGPlayerContainer = SMGPlayerContainer(output_data, patch_path, self.player_name, self.player)
        player_container.write()
    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            er_hint_data = {}
            for galaxy in galaxies_list:
                slot = [key for key, val in self.shuffled_levels.items() if val == galaxy]
                logging.info(slot)
                for region in region_list:
                    if region == galaxy:
                        for location in location_table.values():
                            if location.location_groups[0] == galaxy:
                                er_hint_data.update({location.code: slot[0]})
            hint_data[self.player] = er_hint_data

                                

