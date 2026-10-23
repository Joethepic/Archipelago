import os
import threading
from dataclasses import fields
from typing import ClassVar
from math import ceil

from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
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
from .locations import LOCATION_NAME_TO_ID, get_location_names_per_category, SMGLocation, all_location_table, hungry_luma_events_table
from .items import SMGItem, ITEM_NAME_TO_ID, get_item_names_per_category, all_items_table
from .regions import disconnect_from_option, region_list, SMGRegionData, galaxies_list
from .SMGSettings import SuperMarioGalaxySettings
from .Patch.SMGPlayerContainer import SMGPlayerContainer

# Module-level, computed once
PER_GAME_OPTION_NAMES = {f.name for f in fields(PerGameCommonOptions)}

def runClient(*args):
    from .SMGClient import launch
    launch_subprocess(launch, name = "SMG Client", args = args)

components.append(Component("SMG Client", func=runClient, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsmg")))


def _set_gen_thread_finished(multiworld: MultiWorld, game_name: str):
    for world in multiworld.get_game_worlds(game_name):
        world.finished_post_generation.set()

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
    settings: ClassVar[SuperMarioGalaxySettings]

    item_name_to_id: ClassVar[dict[str, int]] = ITEM_NAME_TO_ID
    location_name_to_id: ClassVar[dict[str, int]] = LOCATION_NAME_TO_ID

    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    required_client_version = (0, 6, 6)

    hint_blacklist = {"B: Bowser's Galaxy Reactor", "Peach"}
    starbit_luma_spheres: dict[str, int]
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, *args, **kwargs):
        super(SMGWorld, self).__init__(*args, **kwargs)
        self.finished_post_generation = threading.Event()
        self.origin_region_name: str = regname.SHIP
        self.shuffled_levels: dict[str, str] = {} # Entrance Name (Galaxy Slot): Region name (Galaxy)
        self.starting_galaxy: str = regname.GOODEGG
        self.galaxy_counts: dict[str, int] = {}
        self.starbit_luma_spheres = {}


    def generate_early(self) -> None:
        regen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if regen_passthrough and self.game in regen_passthrough:
            slot_data = regen_passthrough[self.game]

            for key, value in slot_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    getattr(self.options, key).value = value

            return

        for key in self.options.observatory_luma_counts.valid_keys:
            if key not in self.options.observatory_luma_counts.value.keys():
                self.options.observatory_luma_counts.value.update({key: 0})
        if self.options.observatory_hungry_luma_behavior.value == self.options.observatory_hungry_luma_behavior.option_Vanilla:
            self.options.observatory_luma_counts.value = self.options.observatory_luma_counts.default
        elif self.options.observatory_hungry_luma_behavior.value >= 3: # If We're using one of the progressive value options
            luma_list: list[str] = list(sorted(self.options.observatory_luma_counts.valid_keys))
            sorted_counts: list[int] = list(sorted(self.options.observatory_luma_counts.value.values()))
            last_starbit_count: int = 0
            starbit_cap: int = 5000 if self.options.observatory_hungry_luma_behavior.value == 3 else 9999
            for i, luma, in enumerate(luma_list):
                if luma == "Dome 1 Hungry Luma":
                    self.options.observatory_luma_counts.value[luma] = min(sorted_counts[i], starbit_cap)
                    last_starbit_count = min(sorted_counts[i], starbit_cap)
                else:
                    if sorted_counts[i] < last_starbit_count:
                        if last_starbit_count == starbit_cap:
                            self.options.observatory_luma_counts.value[luma] = starbit_cap
                        else:
                            self.options.observatory_luma_counts.value[luma] = self.random.randrange(last_starbit_count,starbit_cap)
                    else:
                        self.options.observatory_luma_counts.value[luma] = min(self.options.observatory_luma_counts.value[luma], starbit_cap)
                    last_starbit_count = self.options.observatory_luma_counts.value[luma]

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
            if not self.options.mario_colors.value[key] in self.options.mario_colors.valid_values:
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
                        getattr(self.options, f"dome_{dome_name}_counts").value.update({dome_orb_name: previous_dome_count})
                        galaxy_counts[f"D{dome_num}G{i + 1}"] = previous_dome_count
                        continue

                    dome_dict[dome_orb_name] = previous_dome_count
                    getattr(self.options, f"dome_{dome_name}_counts").value.update({dome_orb_name: previous_dome_count})

                    # Special case for Dome 6, as D6 will only ever have 4 galaxies total
                if dome_name == "six" and dome_orb_name == "Fifth Orbit":
                    continue
                if dome_orb_name == "First Orbit":
                    count = min(self.options.stars_to_finish.value, previous_dome_count + int(dome_dict[dome_orb_name]))
                    galaxy_counts[f"D{dome_num}G{i + 1}"] = count
                    previous_orbit_count = count
                else:
                    count = min(self.options.stars_to_finish.value, previous_orbit_count + int(dome_dict[dome_orb_name]))
                    galaxy_counts[f"D{dome_num}G{i + 1}"] = count
                    previous_orbit_count = count

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
        
        # make sure we don't create more stars than locations, somehow
        self.options.stars_to_finish.value = min(self.options.stars_to_finish.value,
            len(self.multiworld.get_unfilled_locations(self.player)) - len(local_pool))
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
        # Since UT will already have the levels shuffled, rather than randomly picking them, we have the list
        #   that was already chosen, so we should just disconnect, reconnect, then add rules.
        if self.shuffled_levels:
            from entrance_rando import disconnect_entrance_for_randomization
            for entr_name, reg_name in self.shuffled_levels.items():
                entrance = self.get_entrance(entr_name)
                if entrance.connected_region.name != reg_name:
                    disconnect_entrance_for_randomization(entrance, 0, entrance.connected_region.name)
                    entrance.connect(self.get_region(reg_name))

        elif self.options.galaxy_shuffle:
            # Disconnect entrances based on options choice. Also ensures first available slot is a major galaxy
            self.starting_galaxy = disconnect_from_option(self)
            # Run randomize entrances, but do not get pairings - we create our own method for them
            randomize_entrances(self, True, {0: [0]})

        # Apply rules to newly formed entrances based on within-world access, regardless of randomization
        rules_from_er_placements(self)
        return

    # def pre_fill(self) -> None:
    #     visualize_regions(self.get_region(self.origin_region_name), "SMG_region_graph.puml", show_entrance_names=True)

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        luma_worlds = {world.player for world in multiworld.get_game_worlds(cls.game)
                      if world.options.observatory_hungry_luma_behavior.value == world.options.observatory_hungry_luma_behavior.option_By_Sphere}
        try:
            def check_boo_players_done() -> None:
                done_players = set()
                for player in luma_worlds:
                    player_luma_world = multiworld.worlds[player]
                    if len(player_luma_world.starbit_luma_spheres.keys()) == len(hungry_luma_events_table.keys()):
                        done_players.add(player)
                luma_worlds.difference_update(done_players)
            if luma_worlds:
                for sphere_num, sphere in enumerate(multiworld.get_spheres(), 1):
                    for loc in sphere:
                        if loc.player in luma_worlds and loc.name in hungry_luma_events_table.keys():
                            player_world = multiworld.worlds[loc.player]
                            player_world.starbit_luma_spheres.update({loc.name: sphere_num})
                        check_boo_players_done()
                    if not luma_worlds:
                        return
        except Exception:
            import traceback
            traceback.print_exc()
            raise
        finally:
            _set_gen_thread_finished(multiworld, cls.game)

    # Output options, locations and doors for patcher
    def generate_output(self, output_directory: str):
        if self.options.observatory_hungry_luma_behavior.value == self.options.observatory_hungry_luma_behavior.option_By_Sphere:
            max_value: int = self.options.observatory_luma_counts.value["Gateway Hungry Luma"]
            max_sphere: int = max(self.starbit_luma_spheres.values())
            sphere_unit = ceil(max_value/max_sphere)
            for luma in self.starbit_luma_spheres:
                self.options.observatory_luma_counts.value[luma] = self.starbit_luma_spheres[luma]*sphere_unit

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
                    "classification": location.item.classification.name,
                }
            elif location.item:
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": location.item.game,
                    "classification": location.item.classification.name,
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
                for region in region_list:
                    if region == galaxy:
                        for location in all_location_table.values():
                            if location.galaxy_name == galaxy:
                                er_hint_data.update({location.code: slot[0]})
            hint_data[self.player] = er_hint_data

    def fill_slot_data(self) -> dict:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        slot_data: dict = {}

        # This gets all the names of the options from both the world's option class and the inherited class,
        #   since this world's options inherit from PerGameCommonOptions, there will be duplicates.
        # HOWEVER, rather than just doing GameOptions.__annotations__ and getting it directly that way,
        #   you would automatically filter out death_link for example and... well im just lazy lol
        for f in sorted(fields(self.options), key=lambda f: f.name):
            if f.name in PER_GAME_OPTION_NAMES:
                continue

            # Skip options explicitly slot_req = False
            option = getattr(self.options, f.name)
            if getattr(option, "slot_req", True) is False:
                continue

            slot_data[f.name] = option.value

        slot_data["galaxy_counts"] = self.galaxy_counts
        slot_data["shuffled_levels"] = self.shuffled_levels
        return slot_data

