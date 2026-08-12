from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.rules import Rule

from.Constants.Names import region_names as regname
from .Constants.Names import location_names as locname


class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMGLocation, self).__init__(player, name, address=location_table[name].code, parent=parent)
        self.code = location_table[name].code

class SMGLocationData(NamedTuple):
    location_groups: list[str] # type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    default_access: Rule[Any] = True
    game_address: Optional[int] = 0  #


# good egg galaxy
locGE_table: dict[str, SMGLocationData] = {
    locname.GOODEGGSTAR1: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG, 17000000, game_address=0),
    locname.GOODEGGSTAR2: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG, 17000001, game_address=1),
    locname.GOODEGGSTAR3: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG, 17000002, game_address=2),
    locname.GOODEGGSTAR6: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG, 17000003, game_address=3),
    locname.GOODEGGSTAR4: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG, 17000004, game_address=4),
}

locHH_table: dict[str, SMGLocationData]  = {
    locname.HONEYHIVESTAR1: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000006, game_address=0),
    locname.HONEYHIVESTAR2: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000007, game_address=1),
    locname.HONEYHIVESTAR3: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000008, game_address=2),
    locname.HONEYHIVESTAR4: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000009, game_address=3),
    locname.HONEYHIVESTAR5: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 170000010, game_address=4)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    locname.LOOPDELOOPSTAR1: SMGLocationData(["Loopdeloop Galaxy", "Power Star Locations"], regname.LOOPDEELOOP, 170000012, game_address=0),
    locname.FLIPSWITCHSTAR1: SMGLocationData(["Flipswitch Galaxy", "Power Star Locations"], regname.FLIPSWITCH, 170000013, game_address=0),
    locname.ROLLINGGREENSTAR1: SMGLocationData(["Rolling Green Galaxy", "Power Star Locations"], regname.ROLLINGGREEN, 170000014, game_address=0),
    locname.HURRYSCURRYSTAR1: SMGLocationData(["Hurry-Scurry Galaxy", "Power Star Locations"], regname.HURRYSCUR, 170000015, game_address=0),
    locname.BUBBLEBREEZESTAR1: SMGLocationData(["Bubble Breeze Galaxy", "Power Star Locations"], regname.BUBBLEBREEZE, 170000016, game_address=0),
    locname.HONEYCLIMBSTAR1: SMGLocationData(["Honeyclimb Galaxy", "Power Star Locations"], regname.HONEYCLIMB, 170000118, game_address=0),
    locname.BUOYBASESTAR1: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY, 170000017, game_address=0),
    locname.BUOYBASESTAR2: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY, 170000018, game_address=0),
    #TODO: FIX duplicate abbreviation 
    locname.GATEWAYSTAR1: SMGLocationData([regname.SHIP, "Power Star Locations"], regname.GATEWAY, 170000019, game_address=0),
    locname.BONEFINSTAR1: SMGLocationData(["Bonefin Galaxy", "Power Star Locations"], regname.BONEFIN, 170000021, game_address=0),
    locname.MATTERSPLATTERSTAR1: SMGLocationData(["Matter Splatter Galaxy", "Power Star Locations"], regname.MATTER, 170000022, game_address=0),
    locname.ROLLINGGIZMOSTAR1: SMGLocationData(["Rolling Gizmo Galaxy", "Power Star Locations"], regname.ROLLINGGIZ, 170000023, game_address=0),
    locname.LOOPDEESWOOPSTAR1: SMGLocationData(["Loopdeeswoop Galaxy", "Power Star Locations"], regname.LOOPDEESWOOP, 170000024, game_address=0),
    locname.BUBBLEBLASTSTAR1: SMGLocationData(["Bubble Blast Galaxy", "Power Star Locations"], regname.BUBBLEBLAST, 170000025, game_address=0)
}

locbosses_table: dict[str, SMGLocationData]  = {
    locname.BOWSERJRGRANDSTAR1: SMGLocationData([regname.BOWJR1, "Power Star Locations", "Boss Star"], regname.BOWJR1, 170000026, game_address=0),
    locname.BOWSERGRANDSTAR1: SMGLocationData([regname.BOWSER1, "Power Star Locations", "Boss Star"], regname.BOWSER1, 170000027, game_address=0),
    locname.BOWSERJRGRANDSTAR2: SMGLocationData([regname.BOWJR2, "Power Star Locations", "Boss Star"], regname.BOWJR2, 170000028, game_address=0),
    locname.BOWSERJRGRANDSTAR3: SMGLocationData([regname.BOWJR3, "Power Star Locations", "Boss Star"], regname.BOWJR3, 170000029, game_address=0),
    locname.BOWSERGRANDSTAR2: SMGLocationData([regname.BOWSER2, "Power Star Locations", "Boss Star"], regname.BOWSER2, 170000030, game_address=0),
    locname.BOWSERGRANDSTAR3: SMGLocationData([regname.BOWSER3, "Power Star Locations", "Boss Star"], regname.BOWSER3, None, game_address=0)
}

locSJ_table: dict[str, SMGLocationData]  = {
    locname.SPACEJUNKSTAR1: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000031, game_address=0),
    locname.SPACEJUNKSTAR2: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000032, game_address=1),
    locname.SPACEJUNKSTAR3: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000033, game_address=2),
    locname.SPACEJUNKSTAR4: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000034, game_address=3),
    locname.SPACEJUNKSTAR5: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000035, game_address=4)
}

locBR_table: dict[str, SMGLocationData]  = {
    locname.BATTLEROCKSTAR1: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000037, game_address=0),
    locname.BATTLEROCKSTAR2: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000038, game_address=1),
    locname.BATTLEROCKSTAR3: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000119, game_address=2),
    locname.BATTLEROCKSTAR4: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000039, game_address=3),
    locname.BATTLEROCKSTAR5: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000040, game_address=4),
    locname.BATTLEROCKSTAR6: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000042, game_address=5)
}
#TODO: note change abbreviation same as buoy base
locBB_table: dict[str, SMGLocationData]  = {
    locname.BEACHBOWLSTAR1: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000043, game_address=0),
    locname.BEACHBOWLSTAR2: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000044, game_address=1),
    locname.BEACHBOWLSTAR3: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000045, game_address=2),
    locname.BEACHBOWLSTAR4: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000046, game_address=3),
    locname.BEACHBOWLSTAR5: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000048, game_address=4)
}

locG_table: dict[str, SMGLocationData]  = {
    locname.GHOSTLYSTAR1: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000049, game_address=0),
    locname.GHOSTLYSTAR2: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000050, game_address=1),
    locname.GHOSTLYSTAR3: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000051, game_address=2),
    locname.GHOSTLYSTAR4: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000052, game_address=3),
    locname.GHOSTLYSTAR5: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000054, game_address=4)
}

locGG_table: dict[str, SMGLocationData]  = {
    locname.GUSTYGARDENSTAR1: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000055, game_address=0),
    locname.GUSTYGARDENSTAR2: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000056, game_address=1),
    locname.GUSTYGARDENSTAR3: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000057, game_address=2),
    locname.GUSTYGARDENSTAR4: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000058, game_address=3),
    locname.GUSTYGARDENSTAR5: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000060, game_address=4)
}

locFF_table: dict[str, SMGLocationData]  = {
    locname.FREEZEFLAMESTAR1: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000061, game_address=0),
    locname.FREEZEFLAMESTAR2: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000062, game_address=1),
    locname.FREEZEFLAMESTAR3: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000063, game_address=2),
    locname.FREEZEFLAMESTAR4: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000064, game_address=3),
    locname.FREEZEFLAMESTAR5: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000065, game_address=4)
}

locDDune_table: dict[str, SMGLocationData]  = {
    locname.DUSTYDUNESTAR1: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000067, game_address=0),
    locname.DUSTYDUNESTAR2: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000068, game_address=1),
    locname.DUSTYDUNESTAR3: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000069, game_address=2),
    locname.DUSTYDUNESTAR4: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000071, game_address=3),
    locname.DUSTYDUNESTAR5: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000072, game_address=4),
    locname.DUSTYDUNESTAR6: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000073, game_address=5)
} 

locGL_table: dict[str, SMGLocationData]  = {
    "GL: Star Bunnies on the Hunt": SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000074, game_address=0),
    "GL: Cataquack to the skies": SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000075, game_address=1),
    "GL: When it Rains, it Pours": SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000076, game_address=2),
    "GL: Cosmic Mario Forest Race": SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000077, game_address=3),
    "GL: The Bell on the Big Trees": SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000079, game_address=4)
}
#TODO: Change abbrivation
locSS_table: dict[str, SMGLocationData]  = {
    "SS: Going After Guppy": SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000080, game_address=0),
    "SS: Faster Than a Speedrunning Penguin": SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000081, game_address=1),
    "SS: The Silver Stars of Sea Slide": SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000082, game_address=2),
    "SS: Underwater Cosmic Mario Race": SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000083, game_address=3),
    "SS: Hurry, He's Hungry": SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000085, game_address=4)
}

locTT_table: dict[str, SMGLocationData]  = {
    "TT: Heavy Metal Mecha Boswer": SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000086, game_address=0),
    "TT: Mario (or Luigi) Meets Mario": SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000087, game_address=1),
    "TT: Bouncing Down Cake Lane": SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000088, game_address=2),
    "TT: The Flipswitch Chain": SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000089, game_address=3),
    "TT: Fast Foes of Toy Time": SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000090, game_address=4)
}

locDD_table: dict[str, SMGLocationData]  = {
    "DD: The Underground Ghost Ship": SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000092, game_address=0),
    "DD: Bubble Blastoff": SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000093, game_address=1),
    "DD: Guppy and the Underground Lake": SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000094, game_address=2),
    "DD: Ghost Ship Daredevil Run": SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000095, game_address=3),
    "DD: Boo in Box": SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000097, game_address=4)
}

locDN_table: dict[str, SMGLocationData]  = {
    "DN: Inflitrating the Dreadnought": SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000098, game_address=0),
    "DN: Dreadnought's Colossal Cannons": SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000099, game_address=1),
    "DN: Revenge of the Topman Tribe": SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000100, game_address=2),
    "DN: Topman Tribe Speed Run": SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000101, game_address=3),
    "DN: Dreadnought's Garbage Dump": SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000103, game_address=4)
}

locMM_table: dict[str, SMGLocationData]  = {
    "MM: The Sinking Lava Spire": SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000104, game_address=0),
    "MM: Through the Meteor Storm": SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000105, game_address=1),
    "MM: Fiery Dino Piranha": SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000106, game_address=2),
    "MM: Lava Spire Daredevil Run": SMGLocationData(["Melty Molten Galaxy", "Power Star Location"], regname.MELTY, 170000107, game_address=3),
    "MM Burning Tide": SMGLocationData(["Melty Molten Galaxy", "Power Star Location"], regname.MELTY, 170000109, game_address=4)
}

locHL_table: dict[str, SMGLocationData]  = {
    "SS: Rocky Road": SMGLocationData(["Sweet Sweet Galaxy", "Power Star Location"], regname.SWEETSWEET, 170000110, game_address=0),
    "SP: A Very Sticky Situation": SMGLocationData(["Sling Pod Galaxy", "Power Star Location"], regname.SLINGPOD, 170000111, game_address=0),
    "DDR: Giant Eel Breakout": SMGLocationData(["Drip Drop Galaxy", "Power Star Location"], regname.DRIPDROP, 170000112, game_address=0),
    "BM: Bigmouth's Gold Bait": SMGLocationData(["Bigmouth Galaxy", "Power Star Location"], regname.BIGMOUTH, 170000113, game_address=0),
    "Sandy Spiral: Choosing a Favorite Snack": SMGLocationData(["Sand Spiral Galaxy", "Power Star Location"], regname.SANDSPIRAL, 170000114, game_address=0),
    "Bone's Boneyard: Racing the Spooky Speedster": SMGLocationData(["Boo's Boneyard Galaxy", "Power Star Location"], regname.BOOBONE, 170000115, game_address=0),
    "SC: Star Bunnies in the Snow": SMGLocationData(["Snow Cap Galaxy", "Power Star Location"], regname.SNOWCAP, 170000116, game_address=0)
}

locPC_table: dict[str, SMGLocationData]  = {
    "TT: Luigi's Purple Coins": SMGLocationData(["Toy Time Galaxy", "Power Star Location", "Purple Coins"], regname.TOYTIME, 170000091, game_address=5),
    "DN: Battlestation's Purple Coins": SMGLocationData(["Dreadnought Galaxy", "Power Star Location", "Purple Coins"], regname.DREADNOUGHT, 170000102, game_address=5),
    "MM: Red-Hot Purple Coins": SMGLocationData(["Melty Molten Galaxy", "Power Star Location", "Purple Coins"], regname.MELTY, 170000108, game_address=5),
    "DD: Plunder the Purple Coins": SMGLocationData(["Deep Dark Galaxy", "Power Star Location", "Purple Coins"], regname.DEEPDARK, 170000096, game_address=5),
    "SS: Purple Coins by the Seaside": SMGLocationData(["Sea Slide Galaxy", "Power Star Location", "Purple Coins"], regname.SEASLIDE, 170000084, game_address=5),
    locname.GOODEGGSTAR5: SMGLocationData(["Good Egg Galaxy", "Power Star Locations", "Purple Coins"], regname.GOODEGG, 170000005, game_address=5),
    locname.GATEWAYSTAR2: SMGLocationData([regname.GATEWAY, "Power Star Location", "Purple Coins"], regname.GATEWAY, 170000020, game_address=2),
    locname.BATTLEROCKSTAR7: SMGLocationData(["Battlerock Galaxy", "Power Star Location", "Purple Coins"], regname.BATTLEROCK, 17000121, game_address=5),
    locname.SPACEJUNKSTAR6: SMGLocationData(["Space Junk Galaxy", "Power Star Location", "Purple Coins"], regname.SPACEJUNK, 170000036, game_address=5),
    locname.GATEWAYSTAR2: SMGLocationData(["Gusty Garden Galaxy", "Power Star Location", "Purple Coins"], regname.GUSTY, 170000059, game_address=5),
    # TODO: change abbreviation for galaxy
    locname.BEACHBOWLSTAR6: SMGLocationData(["Bubble Breeze Galaxy", "Power Star Location", "Purple Coins"], regname.BUBBLEBREEZE, 170000047, game_address=5),
    locname.FREEZEFLAMESTAR6: SMGLocationData(["Freezeflame Galaxy", "Power Star Location", "Purple Coins"], regname.FREEZEFLAME, 170000066, game_address=5),
    locname.GHOSTLYSTAR6: SMGLocationData([regname.GHOSTLY, "Power Star Location", "Purple Coins"], regname.GHOSTLY, 170000053, game_address=5),
    "GL: Purple Coins in the Woods": SMGLocationData(["Gold Leaf Galaxy", "Power Star Location", "Purple Coins"], regname.GOLDLEAF, 170000078, game_address=5),
    locname.DUSTYDUNESTAR7: SMGLocationData(["Dusty Dune Galaxy", "Power Star Location", "Purple Coins"], regname.DUSTY, 170000070, game_address=5),
    locname.HONEYHIVESTAR6: SMGLocationData(["Honeyhive Galaxy", "Power Star Location", "Purple Coins"], regname.HONEYHIVE, 170000011, game_address=5)
}

base_stars_locations = {**locGE_table, **locHH_table,
                   **locSJ_table, **locBR_table, **locBB_table,
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table,
                   **locGL_table, **locSS_table, **locTT_table,
                   **locDD_table, **locDN_table, **locMM_table,
                   **locHL_table, **locspecialstages_table, **locbosses_table}

location_table = { **locGE_table, **locHH_table, 
                   **locSJ_table, **locBR_table, **locBB_table, 
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table, 
                   **locGL_table, **locSS_table, **locTT_table, 
                   **locDD_table, **locDN_table, **locMM_table, 
                   **locHL_table, **locspecialstages_table, **locbosses_table, 
                   **locPC_table,
}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in location_table.items() if data.code is not None}

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories