from typing import Dict, NamedTuple, Optional, Set
from BaseClasses import Location, Region

from.Constants.Names import region_names as regname

class SMGLocation(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMGLocation, self).__init__(player, name, address=location_table[name].code, parent=parent)
        self.code = location_table[name].code

class SMGLocationData(NamedTuple):
    location_groups: list[str] # type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    in_game_galaxy_name: str
    game_address: Optional[int] = 0  #
    default_access: Optional[dict[str, int]] = {}

# good egg galaxy
locGE_table: dict[str, SMGLocationData] = {
    "GE: Dino Piranha": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000000, "EggStarGalaxy", game_address=0),
    "GE: A Snack of Cosmic Proportions": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000001, "EggStarGalaxy", game_address=1),
    "GE: King Kaliente's Battle Fleet": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000002, "EggStarGalaxy", game_address=2),
    "GE: Luigi on the Roof": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000003, "EggStarGalaxy", game_address=3),
    "GE: Dino Piranha Speed Run": SMGLocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000004, "EggStarGalaxy", game_address=4),
}

locHH_table: dict[str, SMGLocationData]  = {
    "HH: Bee Mario Takes Flight": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000006, "HoneyBeeKingdomGalaxy", game_address=0),
    "HH: Trouble on the Tower": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000007, "HoneyBeeKingdomGalaxy", game_address=1),
    "HH: Big Bad Bugabooom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000008, "HoneyBeeKingdomGalaxy", game_address=2),
    "HH: Luigi in the Honeyhive Kingdom": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000009, "HoneyBeeKingdomGalaxy", game_address=3),
    "HH: Honeyhive Cosmic Mario Race": SMGLocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 170000010, "HoneyBeeKingdomGalaxy", game_address=4)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    "LDL: Surfing 101": SMGLocationData(["Loopdeloop Galaxy", "Power Star"], regname.LOOPDEELOOP, 170000012, "SurfingLv1Galaxy", game_address=0),
    "FS: Painting the Planet Yellow": SMGLocationData(["Flipswitch Galaxy", "Power Star"], regname.FLIPSWITCH, 170000013, "FlipPanelExGalaxy", game_address=0),
    "RG: Rolling in the Clouds": SMGLocationData(["Rolling Green Galaxy", "Power Star"], regname.ROLLINGGREEN, 170000014, "TamakoroExLv1Galaxy", game_address=0),
    "HS: Shrinking Satellite": SMGLocationData(["Hurry-Scurry Galaxy", "Power Star"], regname.HURRYSCUR, 170000015, "BreakDownPlanetGalaxy", game_address=0),
    "BUB: Through the Poison Swamp": SMGLocationData(["Bubble Breeze Galaxy", "Power Star"], regname.BUBBLEBREEZE, 170000016, "CubeBubbleExLv1Galaxy", game_address=0),
    "HC: Scaling the Sticky Wall": SMGLocationData(["Honeyclimb Galaxy", "Power Star"], regname.HONEYCLIMB, 170000118, "HoneyBeeExGalaxy", game_address=0),
    "BB: The Floating Fortress": SMGLocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000017, "OceanFloaterLandGalaxy", game_address=0),
    "BB: The Secret of Buoy Base": SMGLocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000018, "OceanFloaterLandGalaxy", game_address=0),
    #TODO: FIX duplicate abbreviation 
    "GG: Grand Star Rescue": SMGLocationData([regname.SHIP, "Power Star"], regname.GATEWAY, 170000019, "HeavensDoorGalaxy", game_address=0),
    "BF: Kingfin's Fearsome Waters": SMGLocationData(["Bonefin Galaxy", "Power Star"], regname.BONEFIN, 170000021, "SkullSharkGalaxy", game_address=0),
    "MS: Watch Your Step": SMGLocationData(["Matter Splatter Galaxy", "Power Star"], regname.MATTER, 170000022, "DarkRoomGalaxy", game_address=0),
    "RGT: Gizmos, Gears, and Gadgets": SMGLocationData(["Rolling Gizmo Galaxy", "Power Star"], regname.ROLLINGGIZ, 170000023, "TamakoroExLv2Galaxy", game_address=0),
    "LDT: The Galaxy's Greatest Wave": SMGLocationData(["Loopdeeswoop Galaxy", "Power Star"], regname.LOOPDEESWOOP, 170000024, "SurfingLv2Galaxy", game_address=0),
    "BBT: The Electric Labyrinth": SMGLocationData(["Bubble Blast Galaxy", "Power Star"], regname.BUBBLEBLAST, 170000025, "CubeBubbleExLv2Galaxy", game_address=0)
}

locbosses_table: dict[str, SMGLocationData]  = {
    "BJ: Megaleg's Moon": SMGLocationData([regname.BOWJR1, "Power Star", "Boss Star"], regname.BOWJR1, 170000026, "TriLegLv1Galaxy", game_address=0),
    "B: The Fiery Stronghold": SMGLocationData([regname.BOWSER1, "Power Star", "Boss Star"], regname.BOWSER1, 170000027, "KoopaBattleVs1Galaxy", game_address=0),
    "BJ: Sinking the Airships": SMGLocationData([regname.BOWJR2, "Power Star", "Boss Star"], regname.BOWJR2, 170000028, "KoopaJrShipLv1Galaxy", game_address=0),
    "BJ: King Kaliente's Spicy Return": SMGLocationData([regname.BOWJR3, "Power Star", "Boss Star"], regname.BOWJR3, 170000029, "FloaterOtaKingGalaxy", game_address=0),
    "B: Darkness on the Horizon": SMGLocationData([regname.BOWSER2, "Power Star", "Boss Star"], regname.BOWSER2, 170000030, "KoopaBattleVs2Galaxy", game_address=0),
    "B: The Fate of the Universe": SMGLocationData([regname.BOWSER3, "Power Star", "Boss Star"], regname.BOWSER3, None, "KoopaBattleVs3Galaxy", game_address=0)
}

locSJ_table: dict[str, SMGLocationData]  = {
    "SJ: Pull Star Path": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000031, "StarDustGalaxy", game_address=0),
    "SJ: Kamella's Airship Attack": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000032, "StarDustGalaxy", game_address=1),
    "SJ: Tarantox's Tangled Web": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000033, "StarDustGalaxy", game_address=2),
    "SJ: Yoshi's Unexpected Apparence": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000034, "StarDustGalaxy", game_address=3),
    "SJ: Pull Star Path Speed Run": SMGLocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000035, "StarDustGalaxy", game_address=4)
}

locBR_table: dict[str, SMGLocationData]  = {
    "BR: Battlerock Barrage": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000037, "BattleShipGalaxy", game_address=0),
    "BR: Breaking into the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000038, "BattleShipGalaxy", game_address=1),
    "BR: Topmaniac and Topman Tribe": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000119, "BattleShipGalaxy", game_address=2),
    "BR: Battlerock's Garbage dump": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000039, "BattleShipGalaxy", game_address=3),
    "BR: Topmanic's Dardevil Run": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000040, "BattleShipGalaxy", game_address=4),
    "BR: Luigi under the Saucer": SMGLocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000042, "BattleShipGalaxy", game_address=5)
}
#TODO: note change abbreviation same as buoy base
locBB_table: dict[str, SMGLocationData]  = {
    "BB: Sunken Treasure": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000043, "HeavenlyBeachGalaxy", game_address=0),
    "BB: Passing the Swim Test": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000044, "HeavenlyBeachGalaxy", game_address=1),
    "BB: The Secret Undersea Cavern": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000045, "HeavenlyBeachGalaxy", game_address=2),
    "BB: Fast Foes on the Cyclone Stone": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000046, "HeavenlyBeachGalaxy", game_address=3),
    "BB: Wall Jumping Up Waterfalls": SMGLocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000048, "HeavenlyBeachGalaxy", game_address=4)
}

locG_table: dict[str, SMGLocationData]  = {
    "G: Luigi and the Haunted Mansion": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000049, "PhantomGalaxy", game_address=0),
    "G: A Very Spooky Spirit": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000050, "PhantomGalaxy", game_address=1),
    "G: Beware of Bouldergeist": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000051, "PhantomGalaxy", game_address=2),
    "G: Bouldergeist's Daredevil Run": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000052, "PhantomGalaxy", game_address=3),
    "G: Matter Splatter Mansion": SMGLocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000054, "PhantomGalaxy", game_address=4)
}

locGG_table: dict[str, SMGLocationData]  = {
    "GG: Bunnies in the Wind": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000055, "CosmosGardenGalaxy", game_address=0),
    "GG: The Dirty Tricks of Major Burrows": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000056, "CosmosGardenGalaxy", game_address=1),
    "GG: Gusty Garden's Gravity Scramble": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000057, "CosmosGardenGalaxy", game_address=2),
    "GG: Major Burrows's Daredevil Run": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000058, "CosmosGardenGalaxy", game_address=3),
    "GG: The Golden Chomp": SMGLocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000060, "CosmosGardenGalaxy", game_address=4)
}

locFF_table: dict[str, SMGLocationData]  = {
    "FF: The Frozen Peak of Baron Brr": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000061, "IceVolcanoGalaxy", game_address=0),
    "FF: Freezeflame's Blistering Coore": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000062, "IceVolcanoGalaxy", game_address=1),
    "FF: Hot and Cold Collide": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000063, "IceVolcanoGalaxy", game_address=2),
    "FF: Conquring the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000064, "IceVolcanoGalaxy", game_address=3),
    "FF: Frosty Cosmic Mario race": SMGLocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000065, "IceVolcanoGalaxy", game_address=4)
}

locDDune_table: dict[str, SMGLocationData]  = {
    "DDune: Soaring on the Desert Winds": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000067, "SandClockGalaxy", game_address=0),
    "DDune: Blasting through the Sand": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000068, "SandClockGalaxy", game_address=1),
    "DDune: Sunbaked Sand Castle": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000069, "SandClockGalaxy", game_address=2),
    "DDune: Sandblast Speed Run": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000071, "SandClockGalaxy", game_address=3),
    "DDune: Bullet Bill on Your Back": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000072, "SandClockGalaxy", game_address=4),
    "DDune: Treasure of the Pyramid": SMGLocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000073, "SandClockGalaxy", game_address=5)
} 

locGL_table: dict[str, SMGLocationData]  = {
    "GL: Star Bunnies on the Hunt": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000074, "ReverseKingdomGalaxy", game_address=0),
    "GL: Cataquack to the skies": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000075, "ReverseKingdomGalaxy", game_address=1),
    "GL: When it Rains, it Pours": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000076, "ReverseKingdomGalaxy", game_address=2),
    "GL: Cosmic Mario Forest Race": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000077, "ReverseKingdomGalaxy", game_address=3),
    "GL: The Bell on the Big Trees": SMGLocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000079, "ReverseKingdomGalaxy", game_address=4)
}
#TODO: Change abbrivation
locSS_table: dict[str, SMGLocationData]  = {
    "SS: Going After Guppy": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000080, "OceanRingGalaxy", game_address=0),
    "SS: Faster Than a Speedrunning Penguin": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000081, "OceanRingGalaxy", game_address=1),
    "SS: The Silver Stars of Sea Slide": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000082, "OceanRingGalaxy", game_address=2),
    "SS: Underwater Cosmic Mario Race": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000083, "OceanRingGalaxy", game_address=3),
    "SS: Hurry, He's Hungry": SMGLocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000085, "OceanRingGalaxy", game_address=4)
}

locTT_table: dict[str, SMGLocationData]  = {
    "TT: Heavy Metal Mecha Boswer": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000086, "FactoryGalaxy", game_address=0),
    "TT: Mario (or Luigi) Meets Mario": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000087, "FactoryGalaxy", game_address=1),
    "TT: Bouncing Down Cake Lane": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000088, "FactoryGalaxy", game_address=2),
    "TT: The Flipswitch Chain": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000089, "FactoryGalaxy", game_address=3),
    "TT: Fast Foes of Toy Time": SMGLocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000090, "FactoryGalaxy", game_address=4)
}

locDD_table: dict[str, SMGLocationData]  = {
    "DD: The Underground Ghost Ship": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000092, "OceanPhantomCaveGalaxy", game_address=0),
    "DD: Bubble Blastoff": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000093,"OceanPhantomCaveGalaxy", game_address=1),
    "DD: Guppy and the Underground Lake": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000094,"OceanPhantomCaveGalaxy", game_address=2),
    "DD: Ghost Ship Daredevil Run": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000095,"OceanPhantomCaveGalaxy", game_address=3),
    "DD: Boo in Box": SMGLocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000097,"OceanPhantomCaveGalaxy", game_address=4)
}

locDN_table: dict[str, SMGLocationData]  = {
    "DN: Inflitrating the Dreadnought": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000098, "CannonFleetGalaxy", game_address=0),
    "DN: Dreadnought's Colossal Cannons": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000099, "CannonFleetGalaxy", game_address=1),
    "DN: Revenge of the Topman Tribe": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000100, "CannonFleetGalaxy", game_address=2),
    "DN: Topman Tribe Speed Run": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000101, "CannonFleetGalaxy", game_address=3),
    "DN: Dreadnought's Garbage Dump": SMGLocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000103, "CannonFleetGalaxy", game_address=4)
}

locMM_table: dict[str, SMGLocationData]  = {
    "MM: The Sinking Lava Spire": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000104, "HellProminenceGalaxy", game_address=0),
    "MM: Through the Meteor Storm": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000105, "HellProminenceGalaxy", game_address=1),
    "MM: Fiery Dino Piranha": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000106, "HellProminenceGalaxy", game_address=2),
    "MM: Lava Spire Daredevil Run": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000107, "HellProminenceGalaxy", game_address=3),
    "MM Burning Tide": SMGLocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000109, "HellProminenceGalaxy", game_address=4)
}

locHL_table: dict[str, SMGLocationData]  = {
    "SS: Rocky Road": SMGLocationData(["Sweet Sweet Galaxy", "Power Star"], regname.SWEETSWEET, 170000110, "BeltConveyerExGalaxy", game_address=0),
    "SP: A Very Sticky Situation": SMGLocationData(["Sling Pod Galaxy", "Power Star"], regname.SLINGPOD, 170000111, "CocoonExGalaxy", game_address=0),
    "DDR: Giant Eel Breakout": SMGLocationData(["Drip Drop Galaxy", "Power Star"], regname.DRIPDROP, 170000112, "TearDropGalaxy", game_address=0),
    "BM: Bigmouth's Gold Bait": SMGLocationData(["Bigmouth Galaxy", "Power Star"], regname.BIGMOUTH, 170000113, "FishTunnelGalaxy", game_address=0),
    "Sandy Spiral: Choosing a Favorite Snack": SMGLocationData(["Sand Spiral Galaxy", "Power Star"], regname.SANDSPIRAL, 170000114, "TransformationExGalaxy", game_address=0),
    "Bone's Boneyard: Racing the Spooky Speedster": SMGLocationData(["Boo's Boneyard Galaxy", "Power Star"], regname.BOOBONE, 170000115, "SnowCapsuleGalaxy", game_address=0),
    "SC: Star Bunnies in the Snow": SMGLocationData(["Snow Cap Galaxy", "Power Star"], regname.SNOWCAP, 170000116, "TeresaMario2DGalaxy", game_address=0)
}

locPC_table: dict[str, SMGLocationData]  = {
    "TT: Luigi's Purple Coins": SMGLocationData(["Toy Time Galaxy", "Power Star", "Purple Coins"], regname.TOYTIME, 170000091, "FactoryGalaxy", game_address=5),
    "DN: Battlestation's Purple Coins": SMGLocationData(["Dreadnought Galaxy", "Power Star", "Purple Coins"], regname.DREADNOUGHT, 170000102, "CannonFleetGalaxy", game_address=5),
    "MM: Red-Hot Purple Coins": SMGLocationData(["Melty Molten Galaxy", "Power Star", "Purple Coins"], regname.MELTY, 170000108, "HellProminenceGalaxy", game_address=5),
    "DD: Plunder the Purple Coins": SMGLocationData(["Deep Dark Galaxy", "Power Star", "Purple Coins"], regname.DEEPDARK, 170000096, "OceanPhantomCaveGalaxy", game_address=5),
    "SS: Purple Coins by the Seaside": SMGLocationData(["Sea Slide Galaxy", "Power Star", "Purple Coins"], regname.SEASLIDE, 170000084, "OceanRingGalaxy", game_address=5),
    "GE: Purple Coin Omelet": SMGLocationData(["Good Egg Galaxy", "Power Star", "Purple Coins"], regname.GOODEGG, 17000005, "EggStarGalaxy", game_address=5),
    "GG: Gateway's Purple coins": SMGLocationData([regname.GATEWAY, "Power Star", "Purple Coins"], regname.GATEWAY, 170000020, "HeavensDoorGalaxy", game_address=2),
    "BR: Purple Coins on the Battlerock": SMGLocationData(["Battlerock Galaxy", "Power Star", "Purple Coins"], regname.BATTLEROCK, 17000121, "BattleShipGalaxy", game_address=5),
    "SJ: Purple Coin Spacewalk": SMGLocationData(["Space Junk Galaxy", "Power Star", "Purple Coins"], regname.SPACEJUNK, 170000036, "StarDustGalaxy", game_address=5),
    "GG: Purple Coins on the Puzzle Cube": SMGLocationData(["Gusty Garden Galaxy", "Power Star", "Purple Coins"], regname.GUSTY, 170000059, "CosmosGardenGalaxy", game_address=5),
    # TODO: change abbreviation for galaxy
    "BB: Beachcombing for Purple Coins": SMGLocationData(["Bubble Breeze Galaxy", "Power Star", "Purple Coins"], regname.BUBBLEBREEZE, 170000047, "CubeBubbleExLv1Galaxy", game_address=5),
    "FF: Purple Coins on the Summit": SMGLocationData(["Freezeflame Galaxy", "Power Star", "Purple Coins"], regname.FREEZEFLAME, 170000066, "IceVolcanoGalaxy", game_address=5),
    "G: Purple Coins in the Bone Pen": SMGLocationData([regname.GHOSTLY, "Power Star", "Purple Coins"], regname.GHOSTLY, 170000053, "PhantomGalaxy", game_address=5),
    "GL: Purple Coins in the Woods": SMGLocationData(["Gold Leaf Galaxy", "Power Star", "Purple Coins"], regname.GOLDLEAF, 170000078, "ReverseKingdomGalaxy", game_address=5),
    "DDune: Purple Coin in the Desert": SMGLocationData(["Dusty Dune Galaxy", "Power Star", "Purple Coins"], regname.DUSTY, 170000070, "SandClockGalaxy", game_address=5),
    "HH: The Honeyhive's Purple Coins": SMGLocationData(["Honeyhive Galaxy", "Power Star", "Purple Coins"], regname.HONEYHIVE, 170000011, "HoneyBeeKingdomGalaxy", game_address=5)
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