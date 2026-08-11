import copy
from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld
from entrance_rando import disconnect_entrance_for_randomization

from .Constants.Names import region_names as regname
from .Options import SMGOptions
from .locations import SMGLocation, locPC_table, base_stars_locations, SMGLocationData

if TYPE_CHECKING:
    from . import SMGWorld

class SMGRegionData(NamedTuple):
    type: str  # type of randomization for GER
    region_offset: Optional[int] = None
    in_game_name: Optional[str] = None

class SMGRegion(Region):
    game: str = "Super Mario Galaxy"
    region_data: SMGRegionData

    def __init__(self, region_name: str, region_data: SMGRegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

major_entr_list: list[str] = ["Dome 1 First Orbit Galaxy", "Dome 2 First Orbit Galaxy", "Dome 3 First Orbit Galaxy",
                              "Dome 4 First Orbit Galaxy", "Dome 5 First Orbit Galaxy", "Dome 6 First Orbit Galaxy",
                              "Dome 1 Second Orbit Galaxy", "Dome 2 Third Orbit Galaxy", "Dome 3 Third Orbit Galaxy",
                              "Dome 4 Second Orbit Galaxy", "Dome 5 Second Orbit Galaxy", "Dome 6 Second Orbit Galaxy",
                              "Dome 4 Third Orbit Galaxy", "Dome 5 Third Orbit Galaxy", "Dome 6 Fourth Orbit Galaxy"]

boss_entr_list: list[str] = ["Dome 1 Fifth Orbit Galaxy", "Dome 2 Fifth Orbit Galaxy", "Dome 3 Fifth Orbit Galaxy",
                             "Dome 4 Fifth Orbit Galaxy", "Dome 5 Fifth Orbit Galaxy"]

gal_minor_entr_list: list[str] = ["Dome 1 Third Orbit Galaxy", "Dome 2 Second Orbit Galaxy",
                                  "Dome 3 Second Orbit Galaxy", "Dome 4 Fourth Orbit Galaxy",
                                  "Dome 5 Fourth Orbit Galaxy", "Dome 6 Third Orbit Galaxy",
                                  "Dome 1 Fourth Orbit Galaxy", "Dome 2 Fourth Orbit Galaxy",
                                  "Dome 3 Fourth Orbit Galaxy"]

obs_entr_list: list[str] = ["Sweet Sweet Hungry Luma", "Sling Pod Hungry Luma", "Drip Drop Hungry Luma",
                            "Bigmouth Hungry Luma", "Sand Spiral Hungry Luma", "Snow Cap Hungry Luma", "Gateway Dome",
                            "Boo's Boneyard Hungry Luma", "Rolling Gizmo Launch Star", "Loopdeeswoop Launch Star",
                            "Bubble Blast Launch Star"]

all_galaxy_slots: list[str] = major_entr_list + gal_minor_entr_list + obs_entr_list + boss_entr_list

region_list: dict[str, SMGRegionData] = {
    regname.SHIP: SMGRegionData("Main"),
    regname.TERRACE: SMGRegionData("Dome"),
    regname.FOUNTAIN: SMGRegionData("Dome"),
    regname.ENGINE: SMGRegionData("Dome"),
    regname.KITCHEN: SMGRegionData("Dome"),
    regname.BEDROOM: SMGRegionData("Dome"),
    regname.GARDEN: SMGRegionData("Dome"),
    regname.LIBRARY: SMGRegionData("Dome"),
    regname.COTU: SMGRegionData("Dome"),
    regname.GATEWAY: SMGRegionData("Special", 0x0, "HeavensDoorGalaxy"),
    regname.SWEETSWEET: SMGRegionData("Special", 0x14, "BeltConveyerExGalaxy"),
    regname.SLINGPOD: SMGRegionData("Special", 0x2C, "CocoonExGalaxy"),
    regname.DRIPDROP: SMGRegionData("Special", 0x44, "TearDropGalaxy"),
    regname.BIGMOUTH: SMGRegionData("Special", 0x90, "FishTunnelGalaxy"),
    regname.SANDSPIRAL: SMGRegionData("Special", 0x78, "TransformationExGalaxy"),
    regname.SNOWCAP: SMGRegionData("Special", 0x60, "SnowCapsuleGalaxy"),
    regname.BOOBONE: SMGRegionData("Special", 0x48, "TeresaMario2DGalaxy"),
    regname.ROLLINGGIZ: SMGRegionData("Special", 0x98, "TamakoroExLv2Galaxy"),
    regname.LOOPDEESWOOP: SMGRegionData("Special", 0x9C, "SurfingLv2Galaxy"),
    regname.BUBBLEBLAST: SMGRegionData("Special", 0xA0, "CubeBubbleExLv2Galaxy"),
    #regname.FINALE: SMGRegionData("Special", 0xA4, "PeachCastleFinalGalaxy"),
    regname.BOWJR1: SMGRegionData("Boss", 0x18, "TriLegLv1Galaxy"),
    regname.BOWJR2: SMGRegionData("Boss", 0x4C, "KoopaJrShipLv1Galaxy"),
    regname.BOWJR3: SMGRegionData("Boss", 0x7C, "FloaterOtaKingGalaxy"), # Dome 5
    regname.BOWSER1: SMGRegionData("Boss", 0x30, "KoopaBattleVs1Galaxy"),
    regname.BOWSER2: SMGRegionData("Boss", 0x64, "KoopaBattleVs2Galaxy"),
    regname.BOWSER3: SMGRegionData("Goal", 0x94, "KoopaBattleVs3Galaxy"),
    regname.GOODEGG: SMGRegionData("Major", 0x4, "EggStarGalaxy"),
    regname.HONEYHIVE: SMGRegionData("Major", 0x8, "HoneyBeeKingdomGalaxy"),
    regname.SPACEJUNK: SMGRegionData("Major", 0x1C, "StarDustGalaxy"),
    regname.BATTLEROCK: SMGRegionData("Major", 0x24, "BattleShipGalaxy"),
    regname.BEACHBOWL: SMGRegionData("Major", 0x34, "HeavenlyBeachGalaxy"),
    regname.GHOSTLY: SMGRegionData("Major", 0x3C, "PhantomGalaxy"),
    regname.GUSTY: SMGRegionData("Major", 0x50, "CosmosGardenGalaxy"),
    regname.FREEZEFLAME: SMGRegionData("Major", 0x54, "IceVolcanoGalaxy"),
    regname.DUSTY: SMGRegionData("Major", 0x5C, "SandClockGalaxy"),
    regname.GOLDLEAF: SMGRegionData("Major", 0x68, "ReverseKingdomGalaxy"),
    regname.SEASLIDE: SMGRegionData("Major", 0x6C, "OceanRingGalaxy"),
    regname.TOYTIME: SMGRegionData("Major", 0x74, "FactoryGalaxy"),
    regname.DEEPDARK: SMGRegionData("Major", 0x80, "OceanPhantomCaveGalaxy"),
    regname.DREADNOUGHT: SMGRegionData("Major", 0x84, "CannonFleetGalaxy"),
    regname.MELTY: SMGRegionData("Major", 0x8C, "HellProminenceGalaxy"),
    regname.LOOPDEELOOP: SMGRegionData("Minor", 0xC, "SurfingLv1Galaxy"),
    regname.FLIPSWITCH: SMGRegionData("Minor", 0x10, "FlipPanelExGalaxy"),
    regname.ROLLINGGREEN: SMGRegionData("Minor", 0x20, "TamakoroExLv1Galaxy"),
    regname.HURRYSCUR: SMGRegionData("Minor", 0x28, "BreakDownPlanetGalaxy"),
    regname.BUBBLEBREEZE: SMGRegionData("Minor", 0x38, "CubeBubbleExLv1Galaxy"),
    regname.BUOY: SMGRegionData("Minor", 0x40, "OceanFloaterLandGalaxy"),
    regname.HONEYCLIMB: SMGRegionData("Minor", 0x58, "HoneyBeeExGalaxy"),
    regname.BONEFIN: SMGRegionData("Minor", 0x70, "SkullSharkGalaxy"),
    regname.MATTER: SMGRegionData("Minor", 0x88, "DarkRoomGalaxy"),
    regname.TRIALS: SMGRegionData("Hub"),

    regname.GATEWAY1HOMEP: SMGRegionData("Planetoid"),
    regname.GATEWAY1HOLEY: SMGRegionData("Planetoid"),
    regname.GATEWAY1SMLTU: SMGRegionData("Planetoid"),
    regname.GATEWAY1LRGTU: SMGRegionData("Planetoid"),
    regname.GATEWAY1LRGTI: SMGRegionData("Planetoid"),
    regname.GATEWAY2HOMEP: SMGRegionData("Planetoid"),

    regname.GOODEGG1HOTOW: SMGRegionData("Planetoid"),
    regname.GOODEGG1HOTOP: SMGRegionData("Planetoid"),
    regname.GOODEGG1TONOT: SMGRegionData("Planetoid"),
    regname.GOODEGG1DUMBB: SMGRegionData("Planetoid"),
    regname.GOODEGG1SMLGR: SMGRegionData("Planetoid"),
    regname.GOODEGG1BOULD: SMGRegionData("Planetoid"),
    regname.GOODEGG1PANEL: SMGRegionData("Planetoid"),
    regname.GOODEGG1GRASS: SMGRegionData("Planetoid"),
    regname.GOODEGG1DINOP: SMGRegionData("Planetoid"),
    regname.GOODEGG3HOTOW: SMGRegionData("Planetoid"),
    regname.GOODEGG3HOTOP: SMGRegionData("Planetoid"),
    regname.GOODEGG3TONOT: SMGRegionData("Planetoid"),
    regname.GOODEGG3PALMT: SMGRegionData("Planetoid"),
    regname.GOODEGG3SANDY: SMGRegionData("Planetoid"),
    regname.GOODEGG3CHOMP: SMGRegionData("Planetoid"),
    regname.GOODEGG3CHOMI: SMGRegionData("Planetoid"),
    regname.GOODEGG3GRASS: SMGRegionData("Planetoid"),
    regname.GOODEGG3SHIPS: SMGRegionData("Planetoid"),
    regname.GOODEGG3KBOSS: SMGRegionData("Planetoid"),
    regname.GOODEGG4HOTOW: SMGRegionData("Planetoid"),
    regname.GOODEGG4HOTOP: SMGRegionData("Planetoid"),
    regname.GOODEGG4TONOT: SMGRegionData("Planetoid"),
    regname.GOODEGG4DUMBB: SMGRegionData("Planetoid"),
    regname.GOODEGG4SMLGR: SMGRegionData("Planetoid"),
    regname.GOODEGG4BOULD: SMGRegionData("Planetoid"),
    regname.GOODEGG4PANEL: SMGRegionData("Planetoid"),
    regname.GOODEGG4GRASS: SMGRegionData("Planetoid"),
    regname.GOODEGG4DINOP: SMGRegionData("Planetoid"),
    regname.GOODEGG2HOTOW: SMGRegionData("Planetoid"),
    regname.GOODEGG2HOTOP: SMGRegionData("Planetoid"),
    regname.GOODEGG2TONOT: SMGRegionData("Planetoid"),
    regname.GOODEGG2PEARP: SMGRegionData("Planetoid"),
    regname.GOODEGG2ROCKY: SMGRegionData("Planetoid"),
    regname.GOODEGG2YOSHI: SMGRegionData("Planetoid"),
    regname.GOODEGG2TOWER: SMGRegionData("Planetoid"),
    regname.GOODEGG2CAPSU: SMGRegionData("Planetoid"),
    regname.GOODEGG2CAPSI: SMGRegionData("Planetoid"),
    regname.GOODEGG2STARP: SMGRegionData("Planetoid"),
    regname.GOODEGG5PEARP: SMGRegionData("Planetoid"),
    regname.GOODEGG5ROCKY: SMGRegionData("Planetoid"),
    regname.GOODEGG5YOSHI: SMGRegionData("Planetoid"),
    regname.GOODEGG6LUIGI: SMGRegionData("Planetoid"),

    regname.HONEYHI1LANDI: SMGRegionData("Planetoid"),
    regname.HONEYHI1SIDEP: SMGRegionData("Planetoid"),
    regname.HONEYHI1SMLHI: SMGRegionData("Planetoid"),
    regname.HONEYHI1BOULR: SMGRegionData("Planetoid"),
    regname.HONEYHI1FOUNC: SMGRegionData("Planetoid"),
    regname.HONEYHI1WATRP: SMGRegionData("Planetoid"),
    regname.HONEYHI1WATRT: SMGRegionData("Planetoid"),
    regname.HONEYHI1BIGTR: SMGRegionData("Planetoid"),
    regname.HONEYHI1POUND: SMGRegionData("Planetoid"),
    regname.HONEYHI1UNDER: SMGRegionData("Planetoid"),
    regname.HONEYHI1GARDN: SMGRegionData("Planetoid"),
    regname.HONEYHI1HONYC: SMGRegionData("Planetoid"),
    regname.HONEYHI1PONDT: SMGRegionData("Planetoid"),
    regname.HONEYHI1TREET: SMGRegionData("Planetoid"),
    regname.HONEYHI2LANDI: SMGRegionData("Planetoid"),
    regname.HONEYHI2SIDEP: SMGRegionData("Planetoid"),
    regname.HONEYHI2SMLHI: SMGRegionData("Planetoid"),
    regname.HONEYHI2FOUNC: SMGRegionData("Planetoid"),
    regname.HONEYHI2WATRP: SMGRegionData("Planetoid"),
    regname.HONEYHI2WATRT: SMGRegionData("Planetoid"),
    regname.HONEYHI2UNDER: SMGRegionData("Planetoid"),
    regname.HONEYHI2BIGTR: SMGRegionData("Planetoid"),
    regname.HONEYHI2POUND: SMGRegionData("Planetoid"),
    regname.HONEYHI2CLIFF: SMGRegionData("Planetoid"),
    regname.HONEYHI2HATS2: SMGRegionData("Planetoid"),
    regname.HONEYHI2DROPL: SMGRegionData("Planetoid"),
    regname.HONEYHI2TOWRB: SMGRegionData("Planetoid"),
    regname.HONEYHI2TOWRM: SMGRegionData("Planetoid"),
    regname.HONEYHI2TOWRT: SMGRegionData("Planetoid"),
    regname.HONEYHI3LANDI: SMGRegionData("Planetoid"),
    regname.HONEYHI3SIDEP: SMGRegionData("Planetoid"),
    regname.HONEYHI3SMLHI: SMGRegionData("Planetoid"),
    regname.HONEYHI3BOULR: SMGRegionData("Planetoid"),
    regname.HONEYHI3FOUNC: SMGRegionData("Planetoid"),
    regname.HONEYHI3WATRP: SMGRegionData("Planetoid"),
    regname.HONEYHI3WATRT: SMGRegionData("Planetoid"),
    regname.HONEYHI3BIGTR: SMGRegionData("Planetoid"),
    regname.HONEYHI3POUND: SMGRegionData("Planetoid"),
    regname.HONEYHI3UNDER: SMGRegionData("Planetoid"),
    regname.HONEYHI3BUGLA: SMGRegionData("Planetoid"),
    regname.HONEYHI3BUGAB: SMGRegionData("Planetoid"),
    regname.HONEYHI4LANDI: SMGRegionData("Planetoid"),
    regname.HONEYHI4WATRP: SMGRegionData("Planetoid"),
    regname.HONEYHI4WATRT: SMGRegionData("Planetoid"),
    regname.HONEYHI4UNDER: SMGRegionData("Planetoid"),
    regname.HONEYHI5LANDI: SMGRegionData("Planetoid"),
    regname.HONEYHI5SIDEP: SMGRegionData("Planetoid"),
    regname.HONEYHI5SMLHI: SMGRegionData("Planetoid"),
    regname.HONEYHI5FOUNC: SMGRegionData("Planetoid"),
    regname.HONEYHI5WATRP: SMGRegionData("Planetoid"),
    regname.HONEYHI5WATRT: SMGRegionData("Planetoid"),
    regname.HONEYHI5UNDER: SMGRegionData("Planetoid"),
    regname.HONEYHI5BIGTR: SMGRegionData("Planetoid"),
    regname.HONEYHI5POUND: SMGRegionData("Planetoid"),
    regname.HONEYHI5CLIFF: SMGRegionData("Planetoid"),
    regname.HONEYHI6LUIGI: SMGRegionData("Planetoid"),
    regname.SWEETSW1SWEET: SMGRegionData("Planetoid"),
    regname.LOOPDLO1ENTRY: SMGRegionData("Planetoid"),
    regname.LOOPDLO1COURS: SMGRegionData("Planetoid"),
    regname.FLIPSWI1PANEL: SMGRegionData("Planetoid"),
    regname.ROBOTRE1CAGEB: SMGRegionData("Planetoid"),
    regname.ROBOTRE1MEGAL: SMGRegionData("Planetoid"),
    regname.SLINGPO1WEBPU: SMGRegionData("Planetoid"),
    regname.DRIPDRO1WATER: SMGRegionData("Planetoid"),
    regname.BIGMOUT1ENTRY: SMGRegionData("Planetoid"),
    regname.BIGMOUT1THROA: SMGRegionData("Planetoid"),
    regname.BIGMOUT1LOWER: SMGRegionData("Planetoid"),
    regname.BIGMOUT1UPPER: SMGRegionData("Planetoid"),
    regname.SANDSPI1SHIPB: SMGRegionData("Planetoid"),
    regname.SANDSPI1SANDT: SMGRegionData("Planetoid"),
    regname.SANDSPI1SPIRA: SMGRegionData("Planetoid"),
    regname.SNOWCAP1GLASS: SMGRegionData("Planetoid"),
    regname.SNOWCAP1SNOWY: SMGRegionData("Planetoid"),
    regname.BOOBONE1SKULL: SMGRegionData("Planetoid"),
    regname.BOOBONE1PIT: SMGRegionData("Planetoid"),
    regname.ROLLGIZ1LANDI: SMGRegionData("Planetoid"),
    regname.ROLLGIZ1MAINA: SMGRegionData("Planetoid"),
    regname.LOOPSWO1LANDI: SMGRegionData("Planetoid"),
    regname.LOOPSWO1TERR1: SMGRegionData("Planetoid"),
    regname.LOOPSWO1TERR2: SMGRegionData("Planetoid"),
    regname.LOOPSWO1SWOOP: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LSTARP: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LNORTH: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LNORTW: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LNORTE: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LSOUTE: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LSOUTW: SMGRegionData("Planetoid"),
    regname.BUBBLAS1LLONGF: SMGRegionData("Planetoid"),
}

major_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Major"]

minor_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Minor"]

boss_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Boss"]

specials_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Special"]

def by_type_shuffle(world: "SMGWorld", entrances: list, galaxies: list[str]):
    for entrance in entrances:
        slot = world.get_entrance(entrance)
        galaxy = world.get_region(world.random.choice(sorted(galaxies)))
        galaxies.remove(galaxy.name)
        er_target: Entrance = {e.name: e for e in galaxy.entrances}[galaxy.name]
        galaxy.entrances.remove(er_target)
        slot.connect(galaxy)

def create_regions(world: "SMGWorld"):
    for region_name in region_list.keys():
        world.multiworld.regions.append(SMGRegion(region_name, region_list[region_name], world.player, world.multiworld))

    create_locations(base_stars_locations, world)

    if world.options.enable_purple_coin_stars.value == 1:
        create_locations(locPC_table, world)

    if world.options.stars_to_finish.value > 103 >= len(list(world.get_locations()))-1:
        world.options.stars_to_finish.value = len(list(world.get_locations()))-1

def connect_regions(world: "SMGWorld", player: int, source: str, target: str, name: str, rule=None):
    sourceRegion = world.get_region(source)
    targetRegion = world.get_region(target)

    sourceRegion.connect(targetRegion, name, rule)

def create_region(name: str, world: "SMGWorld") -> Region:
    return Region(name, world.player, world.multiworld, name)

def create_locations(locs: dict[str, SMGLocationData], world: "SMGWorld"):
    for name, data in locs.items():
        reg = world.get_region(data.region)
        location = SMGLocation(world.player, name, reg)
        if data.default_access:
            world.set_rule(location, data.default_access)

        reg.locations += [location]

def disconnect_from_option(world: "SMGWorld") -> str:
    Dome1Slot1 = "Good Egg Galaxy"
    if "Bosses" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Fifth Orbit Galaxy"), 0, regname.BOWJR1)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Fifth Orbit Galaxy"), 0, regname.BOWSER1)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Fifth Orbit Galaxy"), 0, regname.BOWJR2)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Fifth Orbit Galaxy"), 0, regname.BOWSER2)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Fifth Orbit Galaxy"), 0, regname.BOWJR3)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, boss_entr_list, copy.deepcopy(boss_galaxy_list))
    if "Dome Majors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 First Orbit Galaxy"), 0, regname.GOODEGG)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 First Orbit Galaxy"), 0, regname.SPACEJUNK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 First Orbit Galaxy"), 0, regname.BEACHBOWL)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 First Orbit Galaxy"), 0, regname.GUSTY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 First Orbit Galaxy"), 0, regname.GOLDLEAF)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 First Orbit Galaxy"), 0, regname.DEEPDARK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Second Orbit Galaxy"), 0, regname.HONEYHIVE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Third Orbit Galaxy"), 0, regname.BATTLEROCK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Third Orbit Galaxy"), 0, regname.GHOSTLY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Second Orbit Galaxy"), 0, regname.FREEZEFLAME)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Second Orbit Galaxy"), 0, regname.SEASLIDE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Second Orbit Galaxy"), 0, regname.DREADNOUGHT)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Third Orbit Galaxy"), 0, regname.DUSTY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Third Orbit Galaxy"), 0, regname.TOYTIME)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Fourth Orbit Galaxy"), 0, regname.MELTY)

        # Ensure the first galaxy is a major one
        Dome1Galaxy1Slot = world.get_entrance("Dome 1 First Orbit Galaxy")
        major_list_copy = copy.deepcopy(major_galaxy_list)
        starting_galaxy = world.get_region(world.random.choice(sorted(major_list_copy)))
        major_list_copy.remove(starting_galaxy.name)
        er_target: Entrance = {e.name: e for e in starting_galaxy.entrances}[starting_galaxy.name] # couldn't figure out how to index by the entrance name but this should only ever have one of these entrances anyway
        starting_galaxy.entrances.remove(er_target)
        Dome1Galaxy1Slot.connect(starting_galaxy)
        Dome1Slot1 = starting_galaxy.name
        major_entr_list_copy = copy.deepcopy(major_entr_list)
        major_entr_list_copy.remove("Dome 1 First Orbit Galaxy")
        if world.options.galaxy_shuffle_type.value != 2:
            by_type_shuffle(world, major_entr_list_copy, major_list_copy)

    if "Dome Minors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Third Orbit Galaxy"), 0, regname.LOOPDEELOOP)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Second Orbit Galaxy"), 0, regname.ROLLINGGREEN)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Second Orbit Galaxy"), 0, regname.BUBBLEBREEZE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Fourth Orbit Galaxy"), 0, regname.HONEYCLIMB)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Fourth Orbit Galaxy"), 0, regname.BONEFIN)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Third Orbit Galaxy"), 0, regname.MATTER)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Fourth Orbit Galaxy"), 0, regname.FLIPSWITCH)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Fourth Orbit Galaxy"), 0, regname.HURRYSCUR)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Fourth Orbit Galaxy"), 0, regname.BUOY)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, gal_minor_entr_list, copy.deepcopy(minor_galaxy_list))
    if "Observatory Specials" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Sweet Sweet Hungry Luma"), 0, regname.SWEETSWEET)
        disconnect_entrance_for_randomization(world.get_entrance("Sling Pod Hungry Luma"), 0, regname.SLINGPOD)
        disconnect_entrance_for_randomization(world.get_entrance("Drip Drop Hungry Luma"), 0, regname.DRIPDROP)
        disconnect_entrance_for_randomization(world.get_entrance("Bigmouth Hungry Luma"), 0, regname.BIGMOUTH)
        disconnect_entrance_for_randomization(world.get_entrance("Sand Spiral Hungry Luma"), 0, regname.SANDSPIRAL)
        disconnect_entrance_for_randomization(world.get_entrance("Snow Cap Hungry Luma"), 0, regname.SNOWCAP)
        disconnect_entrance_for_randomization(world.get_entrance("Gateway Dome"), 0, regname.GATEWAY)
        disconnect_entrance_for_randomization(world.get_entrance("Boo's Boneyard Hungry Luma"), 0, regname.BOOBONE)
        disconnect_entrance_for_randomization(world.get_entrance("Rolling Gizmo Launch Star"), 0, regname.ROLLINGGIZ)
        disconnect_entrance_for_randomization(world.get_entrance("Loopdeeswoop Launch Star"), 0, regname.LOOPDEESWOOP)
        disconnect_entrance_for_randomization(world.get_entrance("Bubble Blast Launch Star"), 0, regname.BUBBLEBLAST)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, obs_entr_list, copy.deepcopy(specials_galaxy_list))

    #if world.options.shuffle_option.value == 3:


    return Dome1Slot1