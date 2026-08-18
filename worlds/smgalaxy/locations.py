from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.rules import Rule, CanReachLocation, True_

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
    in_game_galaxy_name: str
    default_access: Rule[Any] = None
    game_address: Optional[int] = 0  #


# good egg galaxy
locGE_table: dict[str, SMGLocationData] = {
    locname.GOODEGGSTAR1: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG1DINOP, 17000000,
                                          "EggStarGalaxy",game_address=0),
    locname.GOODEGGSTAR2: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG2STARP, 17000001,
                                          "EggStarGalaxy",game_address=1),
    locname.GOODEGGSTAR3: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG3KBOSS, 17000002,
                                          "EggStarGalaxy",game_address=2),
    locname.GOODEGGSTAR6: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG6LUIGI, 17000003,
                                          "EggStarGalaxy",
                                          CanReachLocation(locname.GHOSTLYSTAR1),game_address=3),
    locname.GOODEGGSTAR4: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG4DINOP, 17000004,
                                          "EggStarGalaxy",game_address=4),
}

locHH_table: dict[str, SMGLocationData]  = {
    locname.HONEYHIVESTAR1: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000006,
                                            "HoneyBeeKingdomGalaxy", game_address=0),
    locname.HONEYHIVESTAR2: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000007,
                                            "HoneyBeeKingdomGalaxy", game_address=1),
    locname.HONEYHIVESTAR3: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000008,
                                            "HoneyBeeKingdomGalaxy", game_address=2),
    locname.HONEYHIVESTAR6: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 17000009,
                                            "HoneyBeeKingdomGalaxy",
                                          CanReachLocation(locname.GHOSTLYSTAR1), game_address=3),
    locname.HONEYHIVESTAR4: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHIVE, 170000010,
                                            "HoneyBeeKingdomGalaxy", game_address=4)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    locname.LOOPDEELOOPSTAR: SMGLocationData(["Loopdeloop Galaxy", "Power Star Locations"], regname.LOOPDEELOOP,
                                             170000012, "SurfingLv1Galaxy", game_address=0),
    locname.FLIPSWITCHSTAR: SMGLocationData(["Flipswitch Galaxy", "Power Star Locations"], regname.FLIPSWITCH,
                                            170000013, "FlipPanelExGalaxy", game_address=0),
    locname.ROLLINGGREENSTAR: SMGLocationData(["Rolling Green Galaxy", "Power Star Locations"], regname.ROLLINGGREEN,
                                              170000014, "TamakoroExLv1Galaxy", game_address=0),
    locname.HURRYSCURRYSTAR: SMGLocationData(["Hurry-Scurry Galaxy", "Power Star Locations"], regname.HURRYSCUR,
                                             170000015, "BreakDownPlanetGalaxy", game_address=0),
    locname.BUBBLEBREEZESTAR: SMGLocationData(["Bubble Breeze Galaxy", "Power Star Locations"], regname.BUBBLEBREEZE,
                                              170000016, "CubeBubbleExLv1Galaxy", game_address=0),
    locname.HONEYCLIMBSTAR: SMGLocationData(["Honeyclimb Galaxy", "Power Star Locations"], regname.HONEYCLIMB,
                                            170000118, "HoneyBeeExGalaxy", game_address=0),
    locname.BUOYBASESTAR1: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY,
                                           170000017, "OceanFloaterLandGalaxy", game_address=0),
    locname.BUOYBASESTAR2: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY,
                                           170000018, "OceanFloaterLandGalaxy", game_address=0),
    #TODO: FIX duplicate abbreviation 
    locname.GATEWAYSTAR1: SMGLocationData([regname.SHIP, "Power Star Locations"], regname.GATEWAY, 170000019, "HeavensDoorGalaxy", game_address=0),
    locname.BONEFINSTAR: SMGLocationData(["Bonefin Galaxy", "Power Star Locations"], regname.BONEFIN, 170000021, "SkullSharkGalaxy", game_address=0),
    locname.MATTERSPLATTERSTAR: SMGLocationData(["Matter Splatter Galaxy", "Power Star Locations"], regname.MATTER, 170000022, "DarkRoomGalaxy", game_address=0),
    locname.ROLLINGGIZMOSTAR: SMGLocationData(["Rolling Gizmo Galaxy", "Power Star Locations"], regname.ROLLINGGIZ, 170000023, "TamakoroExLv2Galaxy", game_address=0),
    locname.LOOPDEESWOOPSTAR: SMGLocationData(["Loopdeeswoop Galaxy", "Power Star Locations"], regname.LOOPDEESWOOP, 170000024, "SurfingLv2Galaxy", game_address=0),
    locname.BUBBLEBLASTSTAR: SMGLocationData(["Bubble Blast Galaxy", "Power Star Locations"], regname.BUBBLEBLAST, 170000025, "CubeBubbleExLv2Galaxy", game_address=0)
}

locbosses_table: dict[str, SMGLocationData]  = {
    locname.ROBOTREACTORSTAR1: SMGLocationData([regname.BOWJR1, "Power Star Locations", "Boss Star"], regname.BOWJR1, 170000026, "TriLegLv1Galaxy", game_address=0),
    locname.STARREACTORSTAR1: SMGLocationData([regname.BOWSER1, "Power Star Locations", "Boss Star"], regname.BOWSER1, 170000027, "KoopaBattleVs1Galaxy", game_address=0),
    locname.AIRSHIPARMADASTAR1: SMGLocationData([regname.BOWJR2, "Power Star Locations", "Boss Star"], regname.BOWJR2, 170000028, "KoopaJrShipLv1Galaxy", game_address=0),
    locname.LAVAREACTORSTAR1: SMGLocationData([regname.BOWJR3, "Power Star Locations", "Boss Star"], regname.BOWJR3, 170000029, "FloaterOtaKingGalaxy", game_address=0),
    locname.DARKMATTERPLANTSTAR1: SMGLocationData([regname.BOWSER2, "Power Star Locations", "Boss Star"], regname.BOWSER2, 170000030, "KoopaBattleVs2Galaxy", game_address=0),
    locname.GALAXYREACTORSTAR1: SMGLocationData([regname.BOWSER3, "Power Star Locations", "Boss Star"], regname.BOWSER3, None, "KoopaBattleVs3Galaxy", game_address=0)
}

locSJ_table: dict[str, SMGLocationData]  = {
    locname.SPACEJUNKSTAR1: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000031, "StarDustGalaxy", game_address=0),
    locname.SPACEJUNKSTAR2: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000032, "StarDustGalaxy", game_address=1),
    locname.SPACEJUNKSTAR3: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000033, "StarDustGalaxy", game_address=2),
    locname.SPACEJUNKSTAR6: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000034, "StarDustGalaxy", game_address=3),
    locname.SPACEJUNKSTAR4: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACEJUNK, 170000035, "StarDustGalaxy", game_address=4)
}

locBR_table: dict[str, SMGLocationData]  = {
    locname.BATTLEROCKSTAR1: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000037, "BattleShipGalaxy", game_address=0),
    locname.BATTLEROCKSTAR2: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000038, "BattleShipGalaxy", game_address=1),
    locname.BATTLEROCKSTAR3: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000119, "BattleShipGalaxy", game_address=2),
    locname.BATTLEROCKSTAR6: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000039, "BattleShipGalaxy", game_address=3),
    locname.BATTLEROCKSTAR4: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000040, "BattleShipGalaxy", game_address=4),
    locname.BATTLEROCKSTAR7: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLEROCK, 170000042,
                                                  "BattleShipGalaxy", CanReachLocation(locname.GHOSTLYSTAR1), game_address=5)
}
#TODO: note change abbreviation same as buoy base
locBB_table: dict[str, SMGLocationData]  = {
    locname.BEACHBOWLSTAR1: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000043, "HeavenlyBeachGalaxy", game_address=0),
    locname.BEACHBOWLSTAR2: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000044, "HeavenlyBeachGalaxy", game_address=1),
    locname.BEACHBOWLSTAR3: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000045, "HeavenlyBeachGalaxy", game_address=2),
    locname.BEACHBOWLSTAR4: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000046, "HeavenlyBeachGalaxy", game_address=3),
    locname.BEACHBOWLSTAR6: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACHBOWL, 170000048, "HeavenlyBeachGalaxy", game_address=4)
}

locG_table: dict[str, SMGLocationData]  = {
    locname.GHOSTLYSTAR1: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000049, "PhantomGalaxy", game_address=0),
    locname.GHOSTLYSTAR2: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000050, "PhantomGalaxy", game_address=1),
    locname.GHOSTLYSTAR3: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000051, "PhantomGalaxy", game_address=2),
    locname.GHOSTLYSTAR4: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000052, "PhantomGalaxy", game_address=3),
    locname.GHOSTLYSTAR6: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY, 170000054, "PhantomGalaxy", game_address=4)
}

locGG_table: dict[str, SMGLocationData]  = {
    locname.GUSTYGARDENSTAR1: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000055, "CosmosGardenGalaxy", game_address=0),
    locname.GUSTYGARDENSTAR2: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000056, "CosmosGardenGalaxy", game_address=1),
    locname.GUSTYGARDENSTAR3: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000057, "CosmosGardenGalaxy", game_address=2),
    locname.GUSTYGARDENSTAR4: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000058, "CosmosGardenGalaxy", game_address=3),
    locname.GUSTYGARDENSTAR6: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY, 170000060, "CosmosGardenGalaxy", game_address=4)
}

locFF_table: dict[str, SMGLocationData]  = {
    locname.FREEZEFLAMESTAR1: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000061, "IceVolcanoGalaxy", game_address=0),
    locname.FREEZEFLAMESTAR2: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000062, "IceVolcanoGalaxy", game_address=1),
    locname.FREEZEFLAMESTAR3: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000063, "IceVolcanoGalaxy", game_address=2),
    locname.FREEZEFLAMESTAR6: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000064, "IceVolcanoGalaxy", game_address=3),
    locname.FREEZEFLAMESTAR4: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREEZEFLAME, 170000065, "IceVolcanoGalaxy", game_address=4)
}

locDDune_table: dict[str, SMGLocationData]  = {
    locname.DUSTYDUNESTAR1: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000067, "SandClockGalaxy", game_address=0),
    locname.DUSTYDUNESTAR2: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000068, "SandClockGalaxy", game_address=1),
    locname.DUSTYDUNESTAR3: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000069, "SandClockGalaxy", game_address=2),
    locname.DUSTYDUNESTAR4: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000071, "SandClockGalaxy", game_address=3),
    locname.DUSTYDUNESTAR6: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000072, "SandClockGalaxy", game_address=4),
    locname.DUSTYDUNESTAR7: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY, 170000073, "SandClockGalaxy", game_address=5)
} 

locGL_table: dict[str, SMGLocationData]  = {
    locname.GOLDLEAFSTAR1: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000074, "ReverseKingdomGalaxy", game_address=0),
    locname.GOLDLEAFSTAR2: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000075, "ReverseKingdomGalaxy", game_address=1),
    locname.GOLDLEAFSTAR3: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000076, "ReverseKingdomGalaxy", game_address=2),
    locname.GOLDLEAFSTAR4: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000077, "ReverseKingdomGalaxy", game_address=3),
    locname.GOLDLEAFSTAR6: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLEAF, 170000079, "ReverseKingdomGalaxy", game_address=4)
}
#TODO: Change abbrivation
locSS_table: dict[str, SMGLocationData]  = {
    locname.SEASLIDESTAR1: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000080, "OceanRingGalaxy", game_address=0),
    locname.SEASLIDESTAR2: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000081, "OceanRingGalaxy", game_address=1),
    locname.SEASLIDESTAR3: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000082, "OceanRingGalaxy", game_address=2),
    locname.SEASLIDESTAR4: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000083, "OceanRingGalaxy", game_address=3),
    locname.SEASLIDESTAR6: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLIDE, 170000085, "OceanRingGalaxy", game_address=4)
}

locTT_table: dict[str, SMGLocationData]  = {
    locname.TOYTIMESTAR1: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000086, "FactoryGalaxy", game_address=0),
    locname.TOYTIMESTAR2: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000087, "FactoryGalaxy", game_address=1),
    locname.TOYTIMESTAR3: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000088, "FactoryGalaxy", game_address=2),
    locname.TOYTIMESTAR6: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000089, "FactoryGalaxy", game_address=3),
    locname.TOYTIMESTAR4: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME, 170000090, "FactoryGalaxy", game_address=4)
}

locDD_table: dict[str, SMGLocationData]  = {
    locname.DEEPDARKSTAR1: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000092, "OceanPhantomCaveGalaxy", game_address=0),
    locname.DEEPDARKSTAR2: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000093,"OceanPhantomCaveGalaxy", game_address=1),
    locname.DEEPDARKSTAR3: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000094,"OceanPhantomCaveGalaxy", game_address=2),
    locname.DEEPDARKSTAR4: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000095,"OceanPhantomCaveGalaxy", game_address=3),
    locname.DEEPDARKSTAR6: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDARK, 170000097,"OceanPhantomCaveGalaxy", game_address=4)
}

locDN_table: dict[str, SMGLocationData]  = {
    locname.DREADNOUGHTSTAR1: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000098, "CannonFleetGalaxy", game_address=0),
    locname.DREADNOUGHTSTAR2: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000099, "CannonFleetGalaxy", game_address=1),
    locname.DREADNOUGHTSTAR3: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000100, "CannonFleetGalaxy", game_address=2),
    locname.DREADNOUGHTSTAR4: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000101, "CannonFleetGalaxy", game_address=3),
    locname.DREADNOUGHTSTAR6: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADNOUGHT, 170000103, "CannonFleetGalaxy", game_address=4)
}

locMM_table: dict[str, SMGLocationData]  = {
    locname.MELTYMOLTENSTAR1: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000104, "HellProminenceGalaxy", game_address=0),
    locname.MELTYMOLTENSTAR2: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000105, "HellProminenceGalaxy", game_address=1),
    locname.MELTYMOLTENSTAR3: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000106, "HellProminenceGalaxy", game_address=2),
    locname.MELTYMOLTENSTAR4: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000107, "HellProminenceGalaxy", game_address=3),
    locname.MELTYMOLTENSTAR6: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY, 170000109, "HellProminenceGalaxy", game_address=4)
}

locHL_table: dict[str, SMGLocationData]  = {
    locname.SWEETSWEETSTAR: SMGLocationData(["Sweet Sweet Galaxy", "Power Star Locations"], regname.SWEETSWEET, 170000110, "BeltConveyerExGalaxy", game_address=0),
    locname.SLINGPODSTAR: SMGLocationData(["Sling Pod Galaxy", "Power Star Locations"], regname.SLINGPOD, 170000111, "CocoonExGalaxy", game_address=0),
    locname.DRIPDROPSTAR: SMGLocationData(["Drip Drop Galaxy", "Power Star Locations"], regname.DRIPDROP, 170000112, "TearDropGalaxy", game_address=0),
    locname.BIGMOUTHSTAR: SMGLocationData(["Bigmouth Galaxy", "Power Star Locations"], regname.BIGMOUTH, 170000113, "FishTunnelGalaxy", game_address=0),
    locname.SANDSPIRALSTAR: SMGLocationData(["Sand Spiral Galaxy", "Power Star Locations"], regname.SANDSPIRAL, 170000114, "TransformationExGalaxy", game_address=0),
    locname.BOOSBONEYARDSTAR: SMGLocationData(["Boo's Boneyard Galaxy", "Power Star Locations"], regname.BOOBONE, 170000115, "SnowCapsuleGalaxy", game_address=0),
    locname.SNOWCAPSTAR: SMGLocationData(["Snow Cap Galaxy", "Power Star Locations"], regname.SNOWCAP, 170000116, "TeresaMario2DGalaxy", game_address=0)
}

locPC_table: dict[str, SMGLocationData]  = {
    locname.TOYTIMESTAR5: SMGLocationData(["Toy Time Galaxy", "Power Star Locations", "Purple Coins"], regname.TOYTIME, 170000091, "FactoryGalaxy", game_address=5),
    locname.DREADNOUGHTSTAR5: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations", "Purple Coins"], regname.DREADNOUGHT, 170000102, "CannonFleetGalaxy", game_address=5),
    locname.MELTYMOLTENSTAR5: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations", "Purple Coins"], regname.MELTY, 170000108, "HellProminenceGalaxy", game_address=5),
    locname.DEEPDARKSTAR5: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations", "Purple Coins"], regname.DEEPDARK, 170000096, "OceanPhantomCaveGalaxy", game_address=5),
    locname.SEASLIDESTAR5: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations", "Purple Coins"], regname.SEASLIDE, 170000084, "OceanRingGalaxy", game_address=5),
    locname.GOODEGGSTAR5: SMGLocationData(["Good Egg Galaxy", "Power Star Locations", "Purple Coins"], regname.GOODEGG5PEARP, 170000005, "EggStarGalaxy", game_address=5),
    locname.GATEWAYSTAR2: SMGLocationData([regname.GATEWAY, "Power Star Locations", "Purple Coins"], regname.GATEWAY, 170000020, "HeavensDoorGalaxy", game_address=2),
    locname.BATTLEROCKSTAR5: SMGLocationData(["Battlerock Galaxy", "Power Star Locations", "Purple Coins"], regname.BATTLEROCK, 17000121, "BattleShipGalaxy", game_address=5),
    locname.SPACEJUNKSTAR5: SMGLocationData(["Space Junk Galaxy", "Power Star Locations", "Purple Coins"], regname.SPACEJUNK, 170000036, "StarDustGalaxy", game_address=5),
    locname.GUSTYGARDENSTAR5: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations", "Purple Coins"], regname.GUSTY, 170000059, "CosmosGardenGalaxy", game_address=5),
    locname.BEACHBOWLSTAR5: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations", "Purple Coins"], regname.BEACHBOWL, 170000047, "HeavenlyBeachGalaxy", game_address=5),
    locname.FREEZEFLAMESTAR5: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations", "Purple Coins"], regname.FREEZEFLAME, 170000066, "IceVolcanoGalaxy", game_address=5),
    locname.GHOSTLYSTAR5: SMGLocationData([regname.GHOSTLY, "Power Star Locations", "Purple Coins"], regname.GHOSTLY, 170000053, "PhantomGalaxy", game_address=5),
    locname.GOLDLEAFSTAR5: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations", "Purple Coins"], regname.GOLDLEAF, 170000078, "ReverseKingdomGalaxy", game_address=5),
    locname.DUSTYDUNESTAR5: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations", "Purple Coins"], regname.DUSTY, 170000070, "SandClockGalaxy", game_address=5),
    locname.HONEYHIVESTAR5: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations", "Purple Coins"], regname.HONEYHIVE, 170000011, "HoneyBeeKingdomGalaxy", game_address=5)
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
