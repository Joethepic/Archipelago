import copy
from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld
from entrance_rando import disconnect_entrance_for_randomization
import logging

from .Constants.Names import region_names as regname, galaxy_in_game_names as galaxyIG
from .SMGOptions import SMGOptions
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
    regname.GATEWAY: SMGRegionData("Special", 0x0, galaxyIG.GATEWAY),
    regname.SWEETSWEET: SMGRegionData("Special", 0x14, galaxyIG.SWEETSWEET),
    regname.SLINGPOD: SMGRegionData("Special", 0x2C, galaxyIG.SLINGPOD),
    regname.DRIPDROP: SMGRegionData("Special", 0x44, galaxyIG.DRIPDROP),
    regname.BIGMOUTH: SMGRegionData("Special", 0x90, galaxyIG.BIGMOUTH),
    regname.SANDSPIRAL: SMGRegionData("Special", 0x78, galaxyIG.SANDSPIRAL),
    regname.SNOWCAP: SMGRegionData("Special", 0x60, galaxyIG.SNOWCAP),
    regname.BOOBONE: SMGRegionData("Special", 0x48, galaxyIG.BOOBONE),
    regname.ROLLINGGIZ: SMGRegionData("Special", 0x98, galaxyIG.ROLLINGGIZ),
    regname.LOOPDEESWOOP: SMGRegionData("Special", 0x9C, galaxyIG.LOOPDEESWOOP),
    regname.BUBBLEBLAST: SMGRegionData("Special", 0xA0, galaxyIG.BUBBLEBLAST),
    #regname.FINALE: SMGRegionData("Special", 0xA4, galaxyIG.FINALE),
    regname.BOWJR1: SMGRegionData("Boss", 0x18, galaxyIG.BOWJR1),
    regname.BOWJR2: SMGRegionData("Boss", 0x4C, galaxyIG.BOWJR2),
    regname.BOWJR3: SMGRegionData("Boss", 0x7C, galaxyIG.BOWJR3), # Dome 5
    regname.BOWSER1: SMGRegionData("Boss", 0x30, galaxyIG.BOWSER1),
    regname.BOWSER2: SMGRegionData("Boss", 0x64, galaxyIG.BOWSER2),
    regname.BOWSER3: SMGRegionData("Goal", 0x94, galaxyIG.BOWSER3),
    regname.GOODEGG: SMGRegionData("Major", 0x4, galaxyIG.GOODEGG),
    regname.HONEYHIVE: SMGRegionData("Major", 0x8, galaxyIG.HONEYHIVE),
    regname.SPACEJUNK: SMGRegionData("Major", 0x1C, galaxyIG.SPACEJUNK),
    regname.BATTLEROCK: SMGRegionData("Major", 0x24, galaxyIG.BATTLEROCK),
    regname.BEACHBOWL: SMGRegionData("Major", 0x34, galaxyIG.BEACHBOWL),
    regname.GHOSTLY: SMGRegionData("Major", 0x3C, galaxyIG.GHOSTLY),
    regname.GUSTY: SMGRegionData("Major", 0x50, galaxyIG.GUSTY),
    regname.FREEZEFLAME: SMGRegionData("Major", 0x54, galaxyIG.FREEZEFLAME),
    regname.DUSTY: SMGRegionData("Major", 0x5C, galaxyIG.DUSTYDUNE),
    regname.GOLDLEAF: SMGRegionData("Major", 0x68, galaxyIG.GOLDLEAF),
    regname.SEASLIDE: SMGRegionData("Major", 0x6C, galaxyIG.SEASLIDE),
    regname.TOYTIME: SMGRegionData("Major", 0x74, galaxyIG.TOYTIME),
    regname.DEEPDARK: SMGRegionData("Major", 0x80, galaxyIG.DEEPDARK),
    regname.DREADNOUGHT: SMGRegionData("Major", 0x84, galaxyIG.DREADNOUGHT),
    regname.MELTY: SMGRegionData("Major", 0x8C, galaxyIG.MELTY),
    regname.LOOPDEELOOP: SMGRegionData("Minor", 0xC, galaxyIG.LOOPDEELOOP),
    regname.FLIPSWITCH: SMGRegionData("Minor", 0x10, galaxyIG.FLIPSWITCH),
    regname.ROLLINGGREEN: SMGRegionData("Minor", 0x20, galaxyIG.ROLLINGGREEN),
    regname.HURRYSCUR: SMGRegionData("Minor", 0x28, galaxyIG.HURRYSCURRY),
    regname.BUBBLEBREEZE: SMGRegionData("Minor", 0x38, galaxyIG.BUBBLEBREEZE),
    regname.BUOY: SMGRegionData("Minor", 0x40, galaxyIG.BUOY),
    regname.HONEYCLIMB: SMGRegionData("Minor", 0x58, galaxyIG.HONEYCLIMB),
    regname.BONEFIN: SMGRegionData("Minor", 0x70, galaxyIG.BONEFIN),
    regname.MATTER: SMGRegionData("Minor", 0x88, galaxyIG.MATTER),
    regname.TRIALS: SMGRegionData("Hub"),

    regname.GATEWAY1HOMEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),
    regname.GATEWAY1HOLEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),
    regname.GATEWAY1SMLTU: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),
    regname.GATEWAY1LRGTU: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),
    regname.GATEWAY1LRGTI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),
    regname.GATEWAY2HOMEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GATEWAY),

    regname.GOODEGG1HOTOW: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1HOTOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1TONOT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1DUMBB: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1SMLGR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1PANEL: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1GRASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG1DINOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3HOTOW: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3HOTOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3TONOT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3PALMT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3SANDY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3CHOMP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3CHOMI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3GRASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3SHIPS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG3KBOSS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4HOTOW: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4HOTOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4TONOT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4DUMBB: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4SMLGR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4PANEL: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4GRASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG4DINOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2HOTOW: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2HOTOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2TONOT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2PEARP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2ROCKY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2YOSHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2CAPSU: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2CAPSI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG2STARP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG5PEARP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG5ROCKY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG5YOSHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),
    regname.GOODEGG6LUIGI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOODEGG),

    regname.HONEYHI1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1SIDEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1BOULR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1WATRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1GARDN: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1HONYC: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1PONDT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI1TREET: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2SIDEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2WATRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2HATS2: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2DROPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2TOWRB: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2TOWRM: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI2TOWRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3SIDEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3BOULR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3WATRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3BUGLA: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI3BUGAB: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI4WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI4WATRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI4UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5SIDEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5WATRT: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI5CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.HONEYHI6LUIGI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYHIVE),
    regname.SWEETSW1SWEET: SMGRegionData("Planetoid", in_game_name=galaxyIG.SWEETSWEET),
    regname.LOOPDLO1ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEELOOP),
    regname.LOOPDLO1COURS: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEELOOP),
    regname.FLIPSWI1PANEL: SMGRegionData("Planetoid", in_game_name=galaxyIG.FLIPSWITCH),
    regname.ROBOTRE1CAGEB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR1),
    regname.ROBOTRE1MEGAL: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR1),
    regname.SLINGPO1WEBPU: SMGRegionData("Planetoid", in_game_name=galaxyIG.SLINGPOD),
    regname.DRIPDRO1WATER: SMGRegionData("Planetoid", in_game_name=galaxyIG.DRIPDROP),
    regname.BIGMOUT1ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.BIGMOUTH),
    regname.BIGMOUT1THROA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BIGMOUTH),
    regname.BIGMOUT1LOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BIGMOUTH),
    regname.BIGMOUT1UPPER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BIGMOUTH),
    regname.SANDSPI1SHIPB: SMGRegionData("Planetoid", in_game_name=galaxyIG.SANDSPIRAL),
    regname.SANDSPI1SANDT: SMGRegionData("Planetoid", in_game_name=galaxyIG.SANDSPIRAL),
    regname.SANDSPI1SPIRA: SMGRegionData("Planetoid", in_game_name=galaxyIG.SANDSPIRAL),
    regname.SNOWCAP1GLASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SNOWCAP),
    regname.SNOWCAP1SNOWY: SMGRegionData("Planetoid", in_game_name=galaxyIG.SNOWCAP),
    regname.BOOBONE1SKULL: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOOBONE),
    regname.BOOBONE1PIT: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOOBONE),
    regname.ROLLGIZ1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.ROLLINGGIZ),
    regname.ROLLGIZ1MAINA: SMGRegionData("Planetoid", in_game_name=galaxyIG.ROLLINGGIZ),
    regname.LOOPSWO1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEESWOOP),
    regname.LOOPSWO1TERR1: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEESWOOP),
    regname.LOOPSWO1TERR2: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEESWOOP),
    regname.LOOPSWO1SWOOP: SMGRegionData("Planetoid", in_game_name=galaxyIG.LOOPDEESWOOP),
    regname.BUBBLAS1LSTARP: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LNORTH: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LNORTW: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LNORTE: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LSOUTE: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LSOUTW: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.BUBBLAS1LLONGF: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBLAST),
    regname.GRANDFINALE: SMGRegionData("Planetoid"),
    regname.GALREAC1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1WALLS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1SMSUN: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1BLSUN: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1SANDY: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1GRAVI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1LAVAT: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1STAIR: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.GALREAC1BOSS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER3),
    regname.SPACJUN1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN1CRYCY: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN1SPHE3: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN1HSHIP: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN1TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN1SILVE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2AIRS1: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2AIRS2: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2AIRS3: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2AIRSI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN2BATTL: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3CRYCY: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3GLASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN6YOSHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3FLOAT: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3HSHIP: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN3TARAN: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4CRYCY: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4SPHE3: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4HSHIP: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN4SILVE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.SPACJUN5PURPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.SPACEJUNK),
    regname.ROLLGRESTART: SMGRegionData("Planetoid", in_game_name=galaxyIG.ROLLINGGREEN),
    regname.ROLLGREBATTL: SMGRegionData("Planetoid", in_game_name=galaxyIG.ROLLINGGREEN),
    regname.ROLLGREFINIS: SMGRegionData("Planetoid", in_game_name=galaxyIG.ROLLINGGREEN),
    regname.HURRSCULANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.HURRYSCURRY),
    regname.HURRSCUPLANE: SMGRegionData("Planetoid", in_game_name=galaxyIG.HURRYSCURRY),
    regname.STARREALPIPE: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER1),
    regname.STAREAGRAVIT: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER1),
    regname.STAREASTAIRS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER1),
    regname.STAREABOSSAR: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER1),
    regname.BATTLE1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE1SPINY: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE1AUTOS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE1FINAL: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE7LUIGI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE5AUTOS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2TETRA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2MINEF: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2CAGEO: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2CAGEI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE2PATCH: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE6BREAK: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3TRIPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3LUMAP: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3INSID: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3BCAGE: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3EXITG: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE3TOPMA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BATTLE4TOPMA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BATTLEROCK),
    regname.BEACH1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH1LAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH1CLIFB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH1CLIFT: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH2LAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH3LAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH3STCYC: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH4STCYC: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH5LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH5LAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH5CLIFB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH5CLIFT: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH6WATRB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH6ICELA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH3CAVES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH1BLOCK: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH2BLOCK: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.BEACH3BLOCK: SMGRegionData("Planetoid", in_game_name=galaxyIG.BEACHBOWL),
    regname.GHOSTLY1TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1FOYER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1BLACK: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1LIBRA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1BALCO: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1CORR1: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY1CORR2: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY2TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY2ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY2BOORA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY6MATTE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3FOYER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3SPIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3SLING: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3TRAMP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3BOSSA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY4BOSSA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY5PCOIN: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.GHOSTLY3ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GHOSTLY),
    regname.BUBBRE1SWAMP1: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBREEZE),
    regname.BUBBRE1SWAMP2: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUBBLEBREEZE),
    regname.BUOY1LAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUOY),
    regname.BUOY1TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUOY),
    regname.BUOY1WATER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUOY),
    regname.BUOY1UNDER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BUOY),
    regname.AIRARM1AIRS1: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.AIRARM1AIRS2: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.AIRARM1GOOMB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.AIRARM1AIRS3: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.AIRARM1AUTOS: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.AIRARM1BATTL: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR2),
    regname.HONEYCL1WALL1: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYCLIMB),
    regname.HONEYCL1WALL2: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYCLIMB),
    regname.HONEYCL1WALL3: SMGRegionData("Planetoid", in_game_name=galaxyIG.HONEYCLIMB),
    regname.DARKMAT1CASTB: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER2),
    regname.DARKMAT1GRAVI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER2),
    regname.DARKMAT1TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER2),
    regname.DARKMAT1BOSSA: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWSER2),
    regname.GUSTY1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY1PILLR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY1BAGMA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY1VINEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY1CMAZE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2PILLR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2QUESD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2QUEST: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2GRATE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2APPLE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2VINED: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY2BOSST: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY3GRASS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY3PEARL: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY3CYMBA: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY3BLOCK: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY4BOSST: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.GUSTY5CMAZE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GUSTY),
    regname.FREFLA1ICERI: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA1MOUNB: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA1SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA1MIDDL: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA1BARBR: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA2ICERI: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA2LAVA1: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA2LAVA2: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA2LAVA3: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA2LAVAC: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA3ICERI: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA3ICELA: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA3ICEFI: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA4ICEFI: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5MOUNB: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5MIDDL: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5BARBR: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5BACK1: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5BACK2: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA5BACK3: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA6BACK1: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA6BACK2: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.FREFLA6BACK3: SMGRegionData("Planetoid", in_game_name=galaxyIG.FREEZEFLAME),
    regname.DUSTY1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY1INPIP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY1PIPEO: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY1SANDT: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY1SANTO: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2WOODE: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2SAND1: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2SAND2: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2SAND3: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2NOTES: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY2MAZEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3POUN1: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3SANDT: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3ROCKY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3OASIS: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3GLASO: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY3GLASI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY6BBILL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4WOODE: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4SAND1: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4SAND2: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4SAND3: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4NOTES: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY4MAZEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY5MAZEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.DUSTY7SANDY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DUSTYDUNE),
    regname.BONEFINTOAD: SMGRegionData("Planetoid", in_game_name=galaxyIG.BONEFIN),
    regname.BONEFINWATR: SMGRegionData("Planetoid", in_game_name=galaxyIG.BONEFIN),
    regname.LAVREALANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR3),
    regname.LAVREALAVA1: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR3),
    regname.LAVREALAVA2: SMGRegionData("Planetoid", in_game_name=galaxyIG.BOWJR3),
    regname.GOLDLE1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE1WOODE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2HONYP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2QCUBE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2BIGMM: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2BELLS: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE2FLOWE: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3FLOAT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE3CANNO: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4FLOAT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE4CANNO: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5SMLHI: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5FOUNC: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5WATRP: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5POUND: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5BOULD: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5FLOAT: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5TOWER: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.GOLDLE5CANNO: SMGRegionData("Planetoid", in_game_name=galaxyIG.GOLDLEAF),
    regname.SEASLI1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI1SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI1TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI2SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI3SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI3BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI3TOADS: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI3CENTE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI4SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI5LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI5SLIDE: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI5BIGTR: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.SEASLI6HURRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.SEASLIDE),
    regname.TOYTIME1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1GRAVI: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1CONVE: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1CYLIN: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1PLATE: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1ROBOB: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1ROBOL: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1ROBOD: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1ROBOA: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME1ROBOH: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME2LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME2SCREW: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME6CHAIN: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME2MARIO: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3SWEET: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3CREAM: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3CAKES: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3PIPES: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME3CANNO: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME4CHAIN: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.TOYTIME5LUIGI: SMGRegionData("Planetoid", in_game_name=galaxyIG.TOYTIME),
    regname.DEEPDA1BEACH: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1BWATR: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1WOODE: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1FHOME: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1GATES: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1WATER: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1SHIPC: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA1SMAST: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2BEACH: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2BWATR: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2WATER: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2WOODE: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2FHOME: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2CLIFF: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2CLIFP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2CHEEP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA2MELON: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA3BEACH: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA3BWATR: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA3WATER: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA4SHIPC: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA4SHIPW: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA4SMAST: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA5SHIPC: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA5SHIPW: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA5SMAST: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DEEPDA6BOOBX: SMGRegionData("Planetoid", in_game_name=galaxyIG.DEEPDARK),
    regname.DREADN1HOURG: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN1ENTRY: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN1INSD1: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN1TOPMN: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN1METAL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN1PLATF: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN2CHIMP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN2AUTOS: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3TOPPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN6BREAK: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3METAL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3PULLP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3MINES: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN3BOSSA: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4TOPPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4METAL: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4PULLP: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4MINES: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4BOSSA: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN5AUTOS: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN5STARS: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.DREADN4LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.DREADNOUGHT),
    regname.MATTER1LANDI: SMGRegionData("Planetoid", in_game_name=galaxyIG.MATTER),
    regname.MATTER1WALLS: SMGRegionData("Planetoid", in_game_name=galaxyIG.MATTER),
    regname.MATTER1SPRIN: SMGRegionData("Planetoid", in_game_name=galaxyIG.MATTER),
    regname.MATTER1MAZES: SMGRegionData("Planetoid", in_game_name=galaxyIG.MATTER),
    regname.MELTY1VOLCA: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY1INVOL: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY1SPHER: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY6LAVAS: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY1UFOSS: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY1LAVAB: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY1SINKI: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY2VOLCA: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY2WHOMP: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY2METEO: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY2TUBEY: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY2CIRCL: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3VOLCA: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3UFOSS: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3LAVA1: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3LAVA2: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3SPINN: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3LAVPL: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY3FDINO: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4VOLCA: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4INVOL: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4SPHER: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4UFOSS: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4LAVAB: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY4SINKI: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY5VOLCA: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
    regname.MELTY5INVOL: SMGRegionData("Planetoid", in_game_name=galaxyIG.MELTY),
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
        logging.info(location.name)
        if data.default_access is not None:
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
