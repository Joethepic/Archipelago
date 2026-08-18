import copy
from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld
from entrance_rando import disconnect_entrance_for_randomization
import logging

from .Constants.Names import region_names as regname
from .Options import SMGOptions
from .locations import SMGLocation, locPC_table, base_stars_locations, SMGLocationData

if TYPE_CHECKING:
    from . import SMGWorld

class SMGRegionData(NamedTuple):
    type: str  # type of randomization for GER
    region_offset: Optional[int] = None
    in_game_name: Optional[str] = ""

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

    regname.GOODEGG1HOTOW: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1HOTOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1TONOT: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1DUMBB: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1SMLGR: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1BOULD: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1PANEL: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1GRASS: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG1DINOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3HOTOW: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3HOTOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3TONOT: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3PALMT: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3SANDY: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3CHOMP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3CHOMI: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3GRASS: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3SHIPS: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG3KBOSS: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4HOTOW: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4HOTOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4TONOT: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4DUMBB: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4SMLGR: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4BOULD: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4PANEL: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4GRASS: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG4DINOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2HOTOW: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2HOTOP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2TONOT: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2PEARP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2ROCKY: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2YOSHI: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2TOWER: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2CAPSU: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2CAPSI: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG2STARP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG5PEARP: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG5ROCKY: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG5YOSHI: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),
    regname.GOODEGG6LUIGI: SMGRegionData("Planetoid", in_game_name="EggStarGalaxy"),

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
    regname.GRANDFINALE: SMGRegionData("Planetoid"),
    regname.GALREAC1LANDI: SMGRegionData("Planetoid"),
    regname.GALREAC1WALLS: SMGRegionData("Planetoid"),
    regname.GALREAC1SMSUN: SMGRegionData("Planetoid"),
    regname.GALREAC1BLSUN: SMGRegionData("Planetoid"),
    regname.GALREAC1SANDY: SMGRegionData("Planetoid"),
    regname.GALREAC1GRAVI: SMGRegionData("Planetoid"),
    regname.GALREAC1LAVAT: SMGRegionData("Planetoid"),
    regname.GALREAC1STAIR: SMGRegionData("Planetoid"),
    regname.GALREAC1BOSS: SMGRegionData("Planetoid"),
    regname.SPACJUN1LANDI: SMGRegionData("Planetoid"),
    regname.SPACJUN1CRYCY: SMGRegionData("Planetoid"),
    regname.SPACJUN1SPHE3: SMGRegionData("Planetoid"),
    regname.SPACJUN1HSHIP: SMGRegionData("Planetoid"),
    regname.SPACJUN1TOADS: SMGRegionData("Planetoid"),
    regname.SPACJUN1SILVE: SMGRegionData("Planetoid"),
    regname.SPACJUN2TOADS: SMGRegionData("Planetoid"),
    regname.SPACJUN2AIRS1: SMGRegionData("Planetoid"),
    regname.SPACJUN2AIRS2: SMGRegionData("Planetoid"),
    regname.SPACJUN2AIRS3: SMGRegionData("Planetoid"),
    regname.SPACJUN2AIRSI: SMGRegionData("Planetoid"),
    regname.SPACJUN2BATTL: SMGRegionData("Planetoid"),
    regname.SPACJUN3TOADS: SMGRegionData("Planetoid"),
    regname.SPACJUN3CRYCY: SMGRegionData("Planetoid"),
    regname.SPACJUN3GLASS: SMGRegionData("Planetoid"),
    regname.SPACJUN6YOSHI: SMGRegionData("Planetoid"),
    regname.SPACJUN3FLOAT: SMGRegionData("Planetoid"),
    regname.SPACJUN3HSHIP: SMGRegionData("Planetoid"),
    regname.SPACJUN3TARAN: SMGRegionData("Planetoid"),
    regname.SPACJUN4LANDI: SMGRegionData("Planetoid"),
    regname.SPACJUN4CRYCY: SMGRegionData("Planetoid"),
    regname.SPACJUN4SPHE3: SMGRegionData("Planetoid"),
    regname.SPACJUN4HSHIP: SMGRegionData("Planetoid"),
    regname.SPACJUN4TOADS: SMGRegionData("Planetoid"),
    regname.SPACJUN4SILVE: SMGRegionData("Planetoid"),
    regname.SPACJUN5PURPL: SMGRegionData("Planetoid"),
    regname.ROLLGRESTART: SMGRegionData("Planetoid"),
    regname.ROLLGREBATTL: SMGRegionData("Planetoid"),
    regname.ROLLGREFINIS: SMGRegionData("Planetoid"),
    regname.HURRSCULANDI: SMGRegionData("Planetoid"),
    regname.HURRSCUPLANE: SMGRegionData("Planetoid"),
    regname.STARREALPIPE: SMGRegionData("Planetoid"),
    regname.STAREAGRAVIT: SMGRegionData("Planetoid"),
    regname.STAREASTAIRS: SMGRegionData("Planetoid"),
    regname.STAREABOSSAR: SMGRegionData("Planetoid"),
    regname.BATTLE1LANDI: SMGRegionData("Planetoid"),
    regname.BATTLE1SPINY: SMGRegionData("Planetoid"),
    regname.BATTLE1AUTOS: SMGRegionData("Planetoid"),
    regname.BATTLE1FINAL: SMGRegionData("Planetoid"),
    regname.BATTLE7LUIGI: SMGRegionData("Planetoid"),
    regname.BATTLE5AUTOS: SMGRegionData("Planetoid"),
    regname.BATTLE2LANDI: SMGRegionData("Planetoid"),
    regname.BATTLE2TETRA: SMGRegionData("Planetoid"),
    regname.BATTLE2MINEF: SMGRegionData("Planetoid"),
    regname.BATTLE2CAGEO: SMGRegionData("Planetoid"),
    regname.BATTLE2CAGEI: SMGRegionData("Planetoid"),
    regname.BATTLE2PATCH: SMGRegionData("Planetoid"),
    regname.BATTLE6BREAK: SMGRegionData("Planetoid"),
    regname.BATTLE3LANDI: SMGRegionData("Planetoid"),
    regname.BATTLE3TRIPL: SMGRegionData("Planetoid"),
    regname.BATTLE3LUMAP: SMGRegionData("Planetoid"),
    regname.BATTLE3CLIFF: SMGRegionData("Planetoid"),
    regname.BATTLE3INSID: SMGRegionData("Planetoid"),
    regname.BATTLE3BCAGE: SMGRegionData("Planetoid"),
    regname.BATTLE3EXITG: SMGRegionData("Planetoid"),
    regname.BATTLE3TOPMA: SMGRegionData("Planetoid"),
    regname.BATTLE4TOPMA: SMGRegionData("Planetoid"),
    regname.BEACH1LANDI: SMGRegionData("Planetoid"),
    regname.BEACH1LAKES: SMGRegionData("Planetoid"),
    regname.BEACH1CLIFB: SMGRegionData("Planetoid"),
    regname.BEACH1CLIFT: SMGRegionData("Planetoid"),
    regname.BEACH2LANDI: SMGRegionData("Planetoid"),
    regname.BEACH2LAKES: SMGRegionData("Planetoid"),
    regname.BEACH3LANDI: SMGRegionData("Planetoid"),
    regname.BEACH3LAKES: SMGRegionData("Planetoid"),
    regname.BEACH3STCYC: SMGRegionData("Planetoid"),
    regname.BEACH4STCYC: SMGRegionData("Planetoid"),
    regname.BEACH5LANDI: SMGRegionData("Planetoid"),
    regname.BEACH5LAKES: SMGRegionData("Planetoid"),
    regname.BEACH5CLIFB: SMGRegionData("Planetoid"),
    regname.BEACH5CLIFT: SMGRegionData("Planetoid"),
    regname.BEACH6WATRB: SMGRegionData("Planetoid"),
    regname.BEACH6ICELA: SMGRegionData("Planetoid"),
    regname.BEACH3CAVES: SMGRegionData("Planetoid"),
    regname.BEACH1BLOCK: SMGRegionData("Planetoid"),
    regname.BEACH2BLOCK: SMGRegionData("Planetoid"),
    regname.BEACH3BLOCK: SMGRegionData("Planetoid"),
    regname.GHOSTLY1TOADS: SMGRegionData("Planetoid"),
    regname.GHOSTLY1ENTRY: SMGRegionData("Planetoid"),
    regname.GHOSTLY1FOYER: SMGRegionData("Planetoid"),
    regname.GHOSTLY1BLACK: SMGRegionData("Planetoid"),
    regname.GHOSTLY1LIBRA: SMGRegionData("Planetoid"),
    regname.GHOSTLY1BALCO: SMGRegionData("Planetoid"),
    regname.GHOSTLY1CORR1: SMGRegionData("Planetoid"),
    regname.GHOSTLY1CORR2: SMGRegionData("Planetoid"),
    regname.GHOSTLY2TOADS: SMGRegionData("Planetoid"),
    regname.GHOSTLY2ENTRY: SMGRegionData("Planetoid"),
    regname.GHOSTLY2BOORA: SMGRegionData("Planetoid"),
    regname.GHOSTLY6MATTE: SMGRegionData("Planetoid"),
    regname.GHOSTLY3TOADS: SMGRegionData("Planetoid"),
    regname.GHOSTLY3FOYER: SMGRegionData("Planetoid"),
    regname.GHOSTLY3SPIDE: SMGRegionData("Planetoid"),
    regname.GHOSTLY3SLING: SMGRegionData("Planetoid"),
    regname.GHOSTLY3TRAMP: SMGRegionData("Planetoid"),
    regname.GHOSTLY3BOSSA: SMGRegionData("Planetoid"),
    regname.GHOSTLY4BOSSA: SMGRegionData("Planetoid"),
    regname.GHOSTLY5PCOIN: SMGRegionData("Planetoid"),
    regname.GHOSTLY3ENTRY: SMGRegionData("Planetoid"),
    regname.BUBBRE1SWAMP1: SMGRegionData("Planetoid"),
    regname.BUBBRE1SWAMP2: SMGRegionData("Planetoid"),
    regname.BUOY1LAKES: SMGRegionData("Planetoid"),
    regname.BUOY1TOWER: SMGRegionData("Planetoid"),
    regname.BUOY1WATER: SMGRegionData("Planetoid"),
    regname.BUOY1UNDER: SMGRegionData("Planetoid"),
    regname.AIRARM1AIRS1: SMGRegionData("Planetoid"),
    regname.AIRARM1AIRS2: SMGRegionData("Planetoid"),
    regname.AIRARM1GOOMB: SMGRegionData("Planetoid"),
    regname.AIRARM1AIRS3: SMGRegionData("Planetoid"),
    regname.AIRARM1AUTOS: SMGRegionData("Planetoid"),
    regname.AIRARM1BATTL: SMGRegionData("Planetoid"),
    regname.HONEYCL1WALL1: SMGRegionData("Planetoid"),
    regname.HONEYCL1WALL2: SMGRegionData("Planetoid"),
    regname.HONEYCL1WALL3: SMGRegionData("Planetoid"),
    regname.DARKMAT1CASTB: SMGRegionData("Planetoid"),
    regname.DARKMAT1GRAVI: SMGRegionData("Planetoid"),
    regname.DARKMAT1TOWER: SMGRegionData("Planetoid"),
    regname.DARKMAT1BOSSA: SMGRegionData("Planetoid"),
    regname.GUSTY1LANDI: SMGRegionData("Planetoid"),
    regname.GUSTY1PILLR: SMGRegionData("Planetoid"),
    regname.GUSTY1BAGMA: SMGRegionData("Planetoid"),
    regname.GUSTY1VINEY: SMGRegionData("Planetoid"),
    regname.GUSTY1CMAZE: SMGRegionData("Planetoid"),
    regname.GUSTY2LANDI: SMGRegionData("Planetoid"),
    regname.GUSTY2PILLR: SMGRegionData("Planetoid"),
    regname.GUSTY2QUESD: SMGRegionData("Planetoid"),
    regname.GUSTY2QUEST: SMGRegionData("Planetoid"),
    regname.GUSTY2GRATE: SMGRegionData("Planetoid"),
    regname.GUSTY2APPLE: SMGRegionData("Planetoid"),
    regname.GUSTY2VINED: SMGRegionData("Planetoid"),
    regname.GUSTY2BOSST: SMGRegionData("Planetoid"),
    regname.GUSTY3LANDI: SMGRegionData("Planetoid"),
    regname.GUSTY3GRASS: SMGRegionData("Planetoid"),
    regname.GUSTY3PEARL: SMGRegionData("Planetoid"),
    regname.GUSTY3CYMBA: SMGRegionData("Planetoid"),
    regname.GUSTY3BLOCK: SMGRegionData("Planetoid"),
    regname.GUSTY4BOSST: SMGRegionData("Planetoid"),
    regname.GUSTY5CMAZE: SMGRegionData("Planetoid"),
    regname.FREFLA1ICERI: SMGRegionData("Planetoid"),
    regname.FREFLA1MOUNB: SMGRegionData("Planetoid"),
    regname.FREFLA1SLIDE: SMGRegionData("Planetoid"),
    regname.FREFLA1MIDDL: SMGRegionData("Planetoid"),
    regname.FREFLA1BARBR: SMGRegionData("Planetoid"),
    regname.FREFLA2ICERI: SMGRegionData("Planetoid"),
    regname.FREFLA2LAVA1: SMGRegionData("Planetoid"),
    regname.FREFLA2LAVA2: SMGRegionData("Planetoid"),
    regname.FREFLA2LAVA3: SMGRegionData("Planetoid"),
    regname.FREFLA2LAVAC: SMGRegionData("Planetoid"),
    regname.FREFLA3ICERI: SMGRegionData("Planetoid"),
    regname.FREFLA3ICELA: SMGRegionData("Planetoid"),
    regname.FREFLA3ICEFI: SMGRegionData("Planetoid"),
    regname.FREFLA4ICEFI: SMGRegionData("Planetoid"),
    regname.FREFLA5MOUNB: SMGRegionData("Planetoid"),
    regname.FREFLA5SLIDE: SMGRegionData("Planetoid"),
    regname.FREFLA5MIDDL: SMGRegionData("Planetoid"),
    regname.FREFLA5BARBR: SMGRegionData("Planetoid"),
    regname.FREFLA5BACK1: SMGRegionData("Planetoid"),
    regname.FREFLA5BACK2: SMGRegionData("Planetoid"),
    regname.FREFLA5BACK3: SMGRegionData("Planetoid"),
    regname.FREFLA6BACK1: SMGRegionData("Planetoid"),
    regname.FREFLA6BACK2: SMGRegionData("Planetoid"),
    regname.FREFLA6BACK3: SMGRegionData("Planetoid"),
    regname.DUSTY1LANDI: SMGRegionData("Planetoid"),
    regname.DUSTY1INPIP: SMGRegionData("Planetoid"),
    regname.DUSTY1PIPEO: SMGRegionData("Planetoid"),
    regname.DUSTY1SANDT: SMGRegionData("Planetoid"),
    regname.DUSTY1SANTO: SMGRegionData("Planetoid"),
    regname.DUSTY2LANDI: SMGRegionData("Planetoid"),
    regname.DUSTY2WOODE: SMGRegionData("Planetoid"),
    regname.DUSTY2SAND1: SMGRegionData("Planetoid"),
    regname.DUSTY2SAND2: SMGRegionData("Planetoid"),
    regname.DUSTY2SAND3: SMGRegionData("Planetoid"),
    regname.DUSTY2NOTES: SMGRegionData("Planetoid"),
    regname.DUSTY2MAZEY: SMGRegionData("Planetoid"),
    regname.DUSTY3LANDI: SMGRegionData("Planetoid"),
    regname.DUSTY3POUN1: SMGRegionData("Planetoid"),
    regname.DUSTY3SANDT: SMGRegionData("Planetoid"),
    regname.DUSTY3ROCKY: SMGRegionData("Planetoid"),
    regname.DUSTY3OASIS: SMGRegionData("Planetoid"),
    regname.DUSTY3GLASO: SMGRegionData("Planetoid"),
    regname.DUSTY3GLASI: SMGRegionData("Planetoid"),
    regname.DUSTY6BBILL: SMGRegionData("Planetoid"),
    regname.DUSTY4LANDI: SMGRegionData("Planetoid"),
    regname.DUSTY4WOODE: SMGRegionData("Planetoid"),
    regname.DUSTY4SAND1: SMGRegionData("Planetoid"),
    regname.DUSTY4SAND2: SMGRegionData("Planetoid"),
    regname.DUSTY4SAND3: SMGRegionData("Planetoid"),
    regname.DUSTY4NOTES: SMGRegionData("Planetoid"),
    regname.DUSTY4MAZEY: SMGRegionData("Planetoid"),
    regname.DUSTY5MAZEY: SMGRegionData("Planetoid"),
    regname.DUSTY7SANDY: SMGRegionData("Planetoid"),
    regname.BONEFINTOAD: SMGRegionData("Planetoid"),
    regname.BONEFINWATR: SMGRegionData("Planetoid"),
    regname.LAVREALANDI: SMGRegionData("Planetoid"),
    regname.LAVREALAVA1: SMGRegionData("Planetoid"),
    regname.LAVREALAVA2: SMGRegionData("Planetoid"),
    regname.GOLDLE1LANDI: SMGRegionData("Planetoid"),
    regname.GOLDLE1SMLHI: SMGRegionData("Planetoid"),
    regname.GOLDLE1FOUNC: SMGRegionData("Planetoid"),
    regname.GOLDLE1WATRP: SMGRegionData("Planetoid"),
    regname.GOLDLE1BIGTR: SMGRegionData("Planetoid"),
    regname.GOLDLE1POUND: SMGRegionData("Planetoid"),
    regname.GOLDLE1CLIFF: SMGRegionData("Planetoid"),
    regname.GOLDLE1BOULD: SMGRegionData("Planetoid"),
    regname.GOLDLE1WOODE: SMGRegionData("Planetoid"),
    regname.GOLDLE2LANDI: SMGRegionData("Planetoid"),
    regname.GOLDLE2SMLHI: SMGRegionData("Planetoid"),
    regname.GOLDLE2FOUNC: SMGRegionData("Planetoid"),
    regname.GOLDLE2WATRP: SMGRegionData("Planetoid"),
    regname.GOLDLE2BIGTR: SMGRegionData("Planetoid"),
    regname.GOLDLE2POUND: SMGRegionData("Planetoid"),
    regname.GOLDLE2CLIFF: SMGRegionData("Planetoid"),
    regname.GOLDLE2BOULD: SMGRegionData("Planetoid"),
    regname.GOLDLE2HONYP: SMGRegionData("Planetoid"),
    regname.GOLDLE2QCUBE: SMGRegionData("Planetoid"),
    regname.GOLDLE2BIGMM: SMGRegionData("Planetoid"),
    regname.GOLDLE2BELLS: SMGRegionData("Planetoid"),
    regname.GOLDLE2FLOWE: SMGRegionData("Planetoid"),
    regname.GOLDLE3LANDI: SMGRegionData("Planetoid"),
    regname.GOLDLE3SMLHI: SMGRegionData("Planetoid"),
    regname.GOLDLE3FOUNC: SMGRegionData("Planetoid"),
    regname.GOLDLE3WATRP: SMGRegionData("Planetoid"),
    regname.GOLDLE3BIGTR: SMGRegionData("Planetoid"),
    regname.GOLDLE3POUND: SMGRegionData("Planetoid"),
    regname.GOLDLE3CLIFF: SMGRegionData("Planetoid"),
    regname.GOLDLE3BOULD: SMGRegionData("Planetoid"),
    regname.GOLDLE3FLOAT: SMGRegionData("Planetoid"),
    regname.GOLDLE3TOWER: SMGRegionData("Planetoid"),
    regname.GOLDLE3CANNO: SMGRegionData("Planetoid"),
    regname.GOLDLE4LANDI: SMGRegionData("Planetoid"),
    regname.GOLDLE4SMLHI: SMGRegionData("Planetoid"),
    regname.GOLDLE4FOUNC: SMGRegionData("Planetoid"),
    regname.GOLDLE4WATRP: SMGRegionData("Planetoid"),
    regname.GOLDLE4BIGTR: SMGRegionData("Planetoid"),
    regname.GOLDLE4POUND: SMGRegionData("Planetoid"),
    regname.GOLDLE4CLIFF: SMGRegionData("Planetoid"),
    regname.GOLDLE4BOULD: SMGRegionData("Planetoid"),
    regname.GOLDLE4FLOAT: SMGRegionData("Planetoid"),
    regname.GOLDLE4TOWER: SMGRegionData("Planetoid"),
    regname.GOLDLE4CANNO: SMGRegionData("Planetoid"),
    regname.GOLDLE5LANDI: SMGRegionData("Planetoid"),
    regname.GOLDLE5SMLHI: SMGRegionData("Planetoid"),
    regname.GOLDLE5FOUNC: SMGRegionData("Planetoid"),
    regname.GOLDLE5WATRP: SMGRegionData("Planetoid"),
    regname.GOLDLE5BIGTR: SMGRegionData("Planetoid"),
    regname.GOLDLE5POUND: SMGRegionData("Planetoid"),
    regname.GOLDLE5CLIFF: SMGRegionData("Planetoid"),
    regname.GOLDLE5BOULD: SMGRegionData("Planetoid"),
    regname.GOLDLE5FLOAT: SMGRegionData("Planetoid"),
    regname.GOLDLE5TOWER: SMGRegionData("Planetoid"),
    regname.GOLDLE5CANNO: SMGRegionData("Planetoid"),
    regname.SEASLI1LANDI: SMGRegionData("Planetoid"),
    regname.SEASLI1SLIDE: SMGRegionData("Planetoid"),
    regname.SEASLI1TOADS: SMGRegionData("Planetoid"),
    regname.SEASLI2LANDI: SMGRegionData("Planetoid"),
    regname.SEASLI2SLIDE: SMGRegionData("Planetoid"),
    regname.SEASLI3LANDI: SMGRegionData("Planetoid"),
    regname.SEASLI3SLIDE: SMGRegionData("Planetoid"),
    regname.SEASLI3BIGTR: SMGRegionData("Planetoid"),
    regname.SEASLI3TOADS: SMGRegionData("Planetoid"),
    regname.SEASLI3CENTE: SMGRegionData("Planetoid"),
    regname.SEASLI4LANDI: SMGRegionData("Planetoid"),
    regname.SEASLI4SLIDE: SMGRegionData("Planetoid"),
    regname.SEASLI5LANDI: SMGRegionData("Planetoid"),
    regname.SEASLI5SLIDE: SMGRegionData("Planetoid"),
    regname.SEASLI5BIGTR: SMGRegionData("Planetoid"),
    regname.SEASLI6HURRY: SMGRegionData("Planetoid"),
    regname.TOYTIME1LANDI: SMGRegionData("Planetoid"),
    regname.TOYTIME1GRAVI: SMGRegionData("Planetoid"),
    regname.TOYTIME1CONVE: SMGRegionData("Planetoid"),
    regname.TOYTIME1CYLIN: SMGRegionData("Planetoid"),
    regname.TOYTIME1PLATE: SMGRegionData("Planetoid"),
    regname.TOYTIME1ROBOB: SMGRegionData("Planetoid"),
    regname.TOYTIME1ROBOL: SMGRegionData("Planetoid"),
    regname.TOYTIME1ROBOD: SMGRegionData("Planetoid"),
    regname.TOYTIME1ROBOA: SMGRegionData("Planetoid"),
    regname.TOYTIME1ROBOH: SMGRegionData("Planetoid"),
    regname.TOYTIME2LANDI: SMGRegionData("Planetoid"),
    regname.TOYTIME2SCREW: SMGRegionData("Planetoid"),
    regname.TOYTIME6CHAIN: SMGRegionData("Planetoid"),
    regname.TOYTIME2MARIO: SMGRegionData("Planetoid"),
    regname.TOYTIME3LANDI: SMGRegionData("Planetoid"),
    regname.TOYTIME3SWEET: SMGRegionData("Planetoid"),
    regname.TOYTIME3CREAM: SMGRegionData("Planetoid"),
    regname.TOYTIME3CAKES: SMGRegionData("Planetoid"),
    regname.TOYTIME3PIPES: SMGRegionData("Planetoid"),
    regname.TOYTIME3CANNO: SMGRegionData("Planetoid"),
    regname.TOYTIME4CHAIN: SMGRegionData("Planetoid"),
    regname.TOYTIME5LUIGI: SMGRegionData("Planetoid"),
    regname.DEEPDA1BEACH: SMGRegionData("Planetoid"),
    regname.DEEPDA1BWATR: SMGRegionData("Planetoid"),
    regname.DEEPDA1WOODE: SMGRegionData("Planetoid"),
    regname.DEEPDA1FHOME: SMGRegionData("Planetoid"),
    regname.DEEPDA1GATES: SMGRegionData("Planetoid"),
    regname.DEEPDA1WATER: SMGRegionData("Planetoid"),
    regname.DEEPDA1SHIPC: SMGRegionData("Planetoid"),
    regname.DEEPDA1SMAST: SMGRegionData("Planetoid"),
    regname.DEEPDA2BEACH: SMGRegionData("Planetoid"),
    regname.DEEPDA2BWATR: SMGRegionData("Planetoid"),
    regname.DEEPDA2WATER: SMGRegionData("Planetoid"),
    regname.DEEPDA2WOODE: SMGRegionData("Planetoid"),
    regname.DEEPDA2FHOME: SMGRegionData("Planetoid"),
    regname.DEEPDA2CLIFF: SMGRegionData("Planetoid"),
    regname.DEEPDA2CLIFP: SMGRegionData("Planetoid"),
    regname.DEEPDA2CHEEP: SMGRegionData("Planetoid"),
    regname.DEEPDA2MELON: SMGRegionData("Planetoid"),
    regname.DEEPDA3BEACH: SMGRegionData("Planetoid"),
    regname.DEEPDA3BWATR: SMGRegionData("Planetoid"),
    regname.DEEPDA3WATER: SMGRegionData("Planetoid"),
    regname.DEEPDA4SHIPC: SMGRegionData("Planetoid"),
    regname.DEEPDA4SHIPW: SMGRegionData("Planetoid"),
    regname.DEEPDA4SMAST: SMGRegionData("Planetoid"),
    regname.DEEPDA5SHIPC: SMGRegionData("Planetoid"),
    regname.DEEPDA5SHIPW: SMGRegionData("Planetoid"),
    regname.DEEPDA5SMAST: SMGRegionData("Planetoid"),
    regname.DEEPDA6BOOBX: SMGRegionData("Planetoid"),
    regname.DREADN1HOURG: SMGRegionData("Planetoid"),
    regname.DREADN1ENTRY: SMGRegionData("Planetoid"),
    regname.DREADN1INSD1: SMGRegionData("Planetoid"),
    regname.DREADN1TOPMN: SMGRegionData("Planetoid"),
    regname.DREADN1METAL: SMGRegionData("Planetoid"),
    regname.DREADN1PLATF: SMGRegionData("Planetoid"),
    regname.DREADN2CHIMP: SMGRegionData("Planetoid"),
    regname.DREADN2AUTOS: SMGRegionData("Planetoid"),
    regname.DREADN3LANDI: SMGRegionData("Planetoid"),
    regname.DREADN3TOPPL: SMGRegionData("Planetoid"),
    regname.DREADN6BREAK: SMGRegionData("Planetoid"),
    regname.DREADN3METAL: SMGRegionData("Planetoid"),
    regname.DREADN3PULLP: SMGRegionData("Planetoid"),
    regname.DREADN3MINES: SMGRegionData("Planetoid"),
    regname.DREADN3BOSSA: SMGRegionData("Planetoid"),
    regname.DREADN4TOPPL: SMGRegionData("Planetoid"),
    regname.DREADN4METAL: SMGRegionData("Planetoid"),
    regname.DREADN4PULLP: SMGRegionData("Planetoid"),
    regname.DREADN4MINES: SMGRegionData("Planetoid"),
    regname.DREADN4BOSSA: SMGRegionData("Planetoid"),
    regname.DREADN5AUTOS: SMGRegionData("Planetoid"),
    regname.DREADN5STARS: SMGRegionData("Planetoid"),
    regname.DREADN4LANDI: SMGRegionData("Planetoid"),
    regname.MATTER1LANDI: SMGRegionData("Planetoid"),
    regname.MATTER1WALLS: SMGRegionData("Planetoid"),
    regname.MATTER1SPRIN: SMGRegionData("Planetoid"),
    regname.MATTER1MAZES: SMGRegionData("Planetoid"),
    regname.MELTY1VOLCA: SMGRegionData("Planetoid"),
    regname.MELTY1INVOL: SMGRegionData("Planetoid"),
    regname.MELTY1SPHER: SMGRegionData("Planetoid"),
    regname.MELTY6LAVAS: SMGRegionData("Planetoid"),
    regname.MELTY1UFOSS: SMGRegionData("Planetoid"),
    regname.MELTY1LAVAB: SMGRegionData("Planetoid"),
    regname.MELTY1SINKI: SMGRegionData("Planetoid"),
    regname.MELTY2VOLCA: SMGRegionData("Planetoid"),
    regname.MELTY2WHOMP: SMGRegionData("Planetoid"),
    regname.MELTY2METEO: SMGRegionData("Planetoid"),
    regname.MELTY2TUBEY: SMGRegionData("Planetoid"),
    regname.MELTY2CIRCL: SMGRegionData("Planetoid"),
    regname.MELTY3VOLCA: SMGRegionData("Planetoid"),
    regname.MELTY3UFOSS: SMGRegionData("Planetoid"),
    regname.MELTY3LAVA1: SMGRegionData("Planetoid"),
    regname.MELTY3LAVA2: SMGRegionData("Planetoid"),
    regname.MELTY3SPINN: SMGRegionData("Planetoid"),
    regname.MELTY3LAVPL: SMGRegionData("Planetoid"),
    regname.MELTY3FDINO: SMGRegionData("Planetoid"),
    regname.MELTY4VOLCA: SMGRegionData("Planetoid"),
    regname.MELTY4INVOL: SMGRegionData("Planetoid"),
    regname.MELTY4SPHER: SMGRegionData("Planetoid"),
    regname.MELTY4UFOSS: SMGRegionData("Planetoid"),
    regname.MELTY4LAVAB: SMGRegionData("Planetoid"),
    regname.MELTY4SINKI: SMGRegionData("Planetoid"),
    regname.MELTY5VOLCA: SMGRegionData("Planetoid"),
    regname.MELTY5INVOL: SMGRegionData("Planetoid"),
}

major_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Major"]

minor_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Minor"]

boss_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Boss"]

specials_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Special"]

galaxies_list: list[str] = []
galaxies_list.extend(major_galaxy_list)
galaxies_list.extend(minor_galaxy_list)
galaxies_list.extend(boss_galaxy_list)
galaxies_list.extend(specials_galaxy_list)
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
        reg.locations += [location]
        logging.info(location.name)
        if data.default_access is not None:
            world.set_rule(location, data.default_access)

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
