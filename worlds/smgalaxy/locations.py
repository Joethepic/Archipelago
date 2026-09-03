from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.rules import Rule, CanReachLocation, True_

from.Constants.Names import region_names as regname
from .Constants.Names import galaxy_in_game_names as galaxyIG
from .Constants.Names import location_names as locname
from .Constants.Names import galaxy_in_game_names as galaxyignname

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
                                          galaxyignname.GOODEGG,game_address=0),
    locname.GOODEGGSTAR2: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG2STARP, 17000001,
                                          galaxyignname.GOODEGG,game_address=1),
    locname.GOODEGGSTAR3: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG3KBOSS, 17000002,
                                          galaxyignname.GOODEGG,game_address=2),
    locname.GOODEGGSTAR6: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG6LUIGI, 17000003,
                                          galaxyignname.GOODEGG,
                                          CanReachLocation(locname.GHOSTLYSTAR1,parent_region_name=regname.GHOSTLY1CORR2),game_address=3),
    locname.GOODEGGSTAR4: SMGLocationData(["Good Egg Galaxy", "Power Star Locations"], regname.GOODEGG4DINOP, 17000004,
                                          galaxyignname.GOODEGG,game_address=4),
}

locHH_table: dict[str, SMGLocationData]  = {
    locname.HONEYHIVESTAR1: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHI1TREET, 17000006,
                                            galaxyignname.HONEYHIVE, game_address=0),
    locname.HONEYHIVESTAR2: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHI2TOWRT, 17000007,
                                            galaxyignname.HONEYHIVE, game_address=1),
    locname.HONEYHIVESTAR3: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHI3BUGAB, 17000008,
                                            galaxyignname.HONEYHIVE, game_address=2),
    locname.HONEYHIVESTAR6: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHI6LUIGI, 17000009,
                                            galaxyignname.HONEYHIVE,
                                          CanReachLocation(locname.GHOSTLYSTAR1,parent_region_name=regname.GHOSTLY1CORR2), game_address=3),
    locname.HONEYHIVESTAR4: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations"], regname.HONEYHI4UNDER, 170000010,
                                            galaxyignname.HONEYHIVE, game_address=4)
}

locspecialstages_table: dict[str, SMGLocationData]  = {
    locname.LOOPDEELOOPSTAR: SMGLocationData(["Loopdeloop Galaxy", "Power Star Locations"], regname.LOOPDLO1COURS,
                                             170000012, galaxyignname.LOOPDEELOOP, game_address=0),
    locname.FLIPSWITCHSTAR: SMGLocationData(["Flipswitch Galaxy", "Power Star Locations"], regname.FLIPSWI1PANEL,
                                            170000013, galaxyignname.FLIPSWITCH, game_address=0),
    locname.ROLLINGGREENSTAR: SMGLocationData(["Rolling Green Galaxy", "Power Star Locations"], regname.ROLLGREFINIS,
                                              170000014, galaxyignname.ROLLINGGREEN, game_address=0),
    locname.HURRYSCURRYSTAR: SMGLocationData(["Hurry-Scurry Galaxy", "Power Star Locations"], regname.HURRSCUPLANE,
                                             170000015, galaxyignname.HURRYSCURRY, game_address=0),
    locname.BUBBLEBREEZESTAR: SMGLocationData(["Bubble Breeze Galaxy", "Power Star Locations"], regname.BUBBRE1SWAMP2,
                                              170000016, galaxyignname.BUBBLEBREEZE, game_address=0),
    locname.HONEYCLIMBSTAR: SMGLocationData(["Honeyclimb Galaxy", "Power Star Locations"], regname.HONEYCL1WALL3,
                                            170000118, galaxyignname.HONEYCLIMB, game_address=0),
    locname.BUOYBASESTAR1: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY1WATER,
                                           170000017, galaxyignname.BUOY, game_address=0),
    locname.BUOYBASESTAR2: SMGLocationData(["Buoy Base Galaxy", "Power Star Locations"], regname.BUOY1UNDER,
                                           170000018, galaxyignname.BUOY, game_address=0),
    locname.GATEWAYSTAR1: SMGLocationData([regname.SHIP, "Power Star Locations"], regname.GATEWAY1LRGTI, 170000019,
                                           galaxyignname.GATEWAY, game_address=0),
    locname.BONEFINSTAR: SMGLocationData(["Bonefin Galaxy", "Power Star Locations"], regname.BONEFINWATR, 170000021,
                                          galaxyignname.BONEFIN, game_address=0),
    locname.MATTERSPLATTERSTAR: SMGLocationData(["Matter Splatter Galaxy", "Power Star Locations"], regname.MATTER1MAZES, 170000022,
                                                galaxyignname.MATTER, game_address=0),
    locname.ROLLINGGIZMOSTAR: SMGLocationData(["Rolling Gizmo Galaxy", "Power Star Locations"], regname.ROLLGIZ1MAINA, 170000023,
                                              galaxyignname.ROLLINGGIZ, game_address=0),
    locname.LOOPDEESWOOPSTAR: SMGLocationData(["Loopdeeswoop Galaxy", "Power Star Locations"], regname.LOOPSWO1SWOOP, 170000024,
                                              galaxyignname.LOOPDEESWOOP, game_address=0),
    locname.BUBBLEBLASTSTAR: SMGLocationData(["Bubble Blast Galaxy", "Power Star Locations"], regname.BUBBLAS1LLONGF, 170000025,
                                             galaxyignname.BUBBLEBLAST, game_address=0)
}

locbosses_table: dict[str, SMGLocationData]  = {
    locname.ROBOTREACTORSTAR1: SMGLocationData([regname.ROBOTRE1MEGAL, "Power Star Locations", "Boss Star"], regname.ROBOTRE1MEGAL,
                                               170000026, galaxyignname.BOWJR1, game_address=0),
    locname.STARREACTORSTAR1: SMGLocationData([regname.BOWSER1, "Power Star Locations", "Boss Star"], regname.STAREABOSSAR,
                                              170000027, galaxyignname.BOWSER1, game_address=0),
    locname.AIRSHIPARMADASTAR1: SMGLocationData([regname.AIRARM1BATTL, "Power Star Locations", "Boss Star"], regname.AIRARM1BATTL,
                                                170000028, galaxyignname.BOWJR2, game_address=0),
    locname.LAVAREACTORSTAR1: SMGLocationData([regname.BOWJR3, "Power Star Locations", "Boss Star"], regname.LAVREALAVA2,
                                              170000029, galaxyignname.BOWSER2, game_address=0),
    locname.DARKMATTERPLANTSTAR1: SMGLocationData([regname.BOWSER2, "Power Star Locations", "Boss Star"], regname.DARKMAT1BOSSA,
                                                  170000030, galaxyignname.BOWJR3, game_address=0),
    locname.GALAXYREACTORSTAR1: SMGLocationData([regname.BOWSER3, "Power Star Locations", "Boss Star"], regname.GALREAC1BOSS,
                                                None, galaxyignname.BOWSER3, game_address=0)
}

locSJ_table: dict[str, SMGLocationData]  = {
    locname.SPACEJUNKSTAR1: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACJUN1SILVE,
                                            170000031, galaxyignname.SPACEJUNK, game_address=0),
    locname.SPACEJUNKSTAR2: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACJUN2BATTL,
                                            170000032, galaxyignname.SPACEJUNK, game_address=1),
    locname.SPACEJUNKSTAR3: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACJUN3TARAN,
                                            170000033, galaxyignname.SPACEJUNK, game_address=2),
    locname.SPACEJUNKSTAR6: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACJUN6YOSHI,
                                            170000034, galaxyignname.SPACEJUNK, game_address=3),
    locname.SPACEJUNKSTAR4: SMGLocationData(["Space Junk Galaxy", "Power Star Locations"], regname.SPACJUN4SILVE,
                                            170000035, galaxyignname.SPACEJUNK, game_address=4)
}

locBR_table: dict[str, SMGLocationData]  = {
    locname.BATTLEROCKSTAR1: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE1FINAL,
                                             170000037, galaxyignname.BATTLEROCK, game_address=0),
    locname.BATTLEROCKSTAR2: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE2PATCH,
                                             170000038, galaxyignname.BATTLEROCK, game_address=1),
    locname.BATTLEROCKSTAR3: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE3TOPMA,
                                             170000119, galaxyignname.BATTLEROCK, game_address=2),
    locname.BATTLEROCKSTAR6: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE6BREAK,
                                             170000039, galaxyignname.BATTLEROCK, game_address=3),
    locname.BATTLEROCKSTAR4: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE4TOPMA,
                                             170000040, galaxyignname.BATTLEROCK, game_address=4),
    locname.BATTLEROCKSTAR7: SMGLocationData(["Battlerock Galaxy", "Power Star Locations"], regname.BATTLE7LUIGI,
                                             170000042,
                                                  galaxyignname.BATTLEROCK, CanReachLocation(locname.GHOSTLYSTAR1,parent_region_name=regname.GHOSTLY1CORR2), game_address=6)
}
#TODO: note change abbreviation same as buoy base
locBB_table: dict[str, SMGLocationData]  = {
    locname.BEACHBOWLSTAR1: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACH1CLIFT,
                                            170000043, galaxyignname.BEACHBOWL, game_address=0),
    locname.BEACHBOWLSTAR2: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACH2LANDI,
                                            170000044, galaxyignname.BEACHBOWL, game_address=1),
    locname.BEACHBOWLSTAR3: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACH3STCYC,
                                            170000045, galaxyignname.BEACHBOWL, game_address=2),
    locname.BEACHBOWLSTAR4: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACH4STCYC,
                                            170000046, galaxyignname.BEACHBOWL, game_address=3),
    locname.BEACHBOWLSTAR6: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations"], regname.BEACH6ICELA,
                                            170000048, galaxyignname.BEACHBOWL, game_address=4)
}

locG_table: dict[str, SMGLocationData]  = {
    locname.GHOSTLYSTAR1: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY1CORR2,
                                          170000049, galaxyignname.GHOSTLY, game_address=0),
    locname.GHOSTLYSTAR2: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY2BOORA,
                                          170000050, galaxyignname.GHOSTLY, game_address=1),
    locname.GHOSTLYSTAR3: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY3BOSSA,
                                          170000051, galaxyignname.GHOSTLY, game_address=2),
    locname.GHOSTLYSTAR4: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY4BOSSA,
                                          170000052, galaxyignname.GHOSTLY, game_address=3),
    locname.GHOSTLYSTAR6: SMGLocationData([regname.GHOSTLY, "Power Star Locations"], regname.GHOSTLY6MATTE,
                                          170000054, galaxyignname.GHOSTLY, game_address=4)
}

locGG_table: dict[str, SMGLocationData]  = {
    locname.GUSTYGARDENSTAR1: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY1CMAZE,
                                              170000055, galaxyignname.GUSTY, game_address=0),
    locname.GUSTYGARDENSTAR2: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY2BOSST,
                                              170000056, galaxyignname.GUSTY, game_address=1),
    locname.GUSTYGARDENSTAR3: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY3BLOCK,
                                              170000057, galaxyignname.GUSTY, game_address=2),
    locname.GUSTYGARDENSTAR4: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY4BOSST,
                                              170000058, galaxyignname.GUSTY, game_address=3),
    locname.GUSTYGARDENSTAR6: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations"], regname.GUSTY3GRASS,
                                              170000060, galaxyignname.GUSTY, game_address=4)
}

locFF_table: dict[str, SMGLocationData]  = {
    locname.FREEZEFLAMESTAR1: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREFLA1BARBR,
                                              170000061, galaxyignname.FREEZEFLAME, game_address=0),
    locname.FREEZEFLAMESTAR2: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREFLA2LAVAC,
                                              170000062, galaxyignname.FREEZEFLAME, game_address=1),
    locname.FREEZEFLAMESTAR3: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREFLA3ICEFI,
                                              170000063, galaxyignname.FREEZEFLAME, game_address=2),
    locname.FREEZEFLAMESTAR6: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREFLA6BACK3,
                                              170000064, galaxyignname.FREEZEFLAME, game_address=3),
    locname.FREEZEFLAMESTAR4: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations"], regname.FREFLA4ICEFI,
                                              170000065, galaxyignname.FREEZEFLAME, game_address=4)
}

locDDune_table: dict[str, SMGLocationData]  = {
    locname.DUSTYDUNESTAR1: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY1SANTO,
                                            170000067, galaxyignname.DUSTYDUNE, game_address=0),
    locname.DUSTYDUNESTAR2: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY2MAZEY,
                                            170000068, galaxyignname.DUSTYDUNE, game_address=1),
    locname.DUSTYDUNESTAR3: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY3GLASI,
                                            170000069, galaxyignname.DUSTYDUNE, game_address=2),
    locname.DUSTYDUNESTAR4: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY4MAZEY,
                                            170000071, galaxyignname.DUSTYDUNE, game_address=3),
    locname.DUSTYDUNESTAR6: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY6BBILL,
                                            170000072, galaxyignname.DUSTYDUNE, game_address=4),
    locname.DUSTYDUNESTAR7: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations"], regname.DUSTY7SANDY,
                                            170000073, galaxyignname.DUSTYDUNE, game_address=6)
} 

locGL_table: dict[str, SMGLocationData]  = {
    locname.GOLDLEAFSTAR1: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLE1WOODE,
                                           170000074, galaxyignname.GOLDLEAF, game_address=0),
    locname.GOLDLEAFSTAR2: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLE2FLOWE,
                                           170000075, galaxyignname.GOLDLEAF, game_address=1),
    locname.GOLDLEAFSTAR3: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLE3CANNO,
                                           170000076, galaxyignname.GOLDLEAF, game_address=2),
    locname.GOLDLEAFSTAR4: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLE4CANNO,
                                           170000077, galaxyignname.GOLDLEAF, game_address=3),
    locname.GOLDLEAFSTAR6: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations"], regname.GOLDLE2BIGTR,
                                           170000079, galaxyignname.GOLDLEAF, game_address=4)
}
#TODO: Change abbrivation
locSS_table: dict[str, SMGLocationData]  = {
    locname.SEASLIDESTAR1: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLI1SLIDE,
                                           170000080, galaxyignname.SEAGLIDE, game_address=0),
    locname.SEASLIDESTAR2: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLI2SLIDE,
                                           170000081, galaxyignname.SEAGLIDE, game_address=1),
    locname.SEASLIDESTAR3: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLI3LANDI,
                                           170000082, galaxyignname.SEAGLIDE, game_address=2),
    locname.SEASLIDESTAR4: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLI4SLIDE,
                                           170000083, galaxyignname.SEAGLIDE, game_address=3),
    locname.SEASLIDESTAR6: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations"], regname.SEASLI6HURRY,
                                           170000085, galaxyignname.SEAGLIDE, game_address=4)
}

locTT_table: dict[str, SMGLocationData]  = {
    locname.TOYTIMESTAR1: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME1ROBOH,
                                          170000086, galaxyignname.TOYTIME, game_address=0),
    locname.TOYTIMESTAR2: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME2MARIO,
                                          170000087, galaxyignname.TOYTIME, game_address=1),
    locname.TOYTIMESTAR3: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME3CANNO,
                                          170000088, galaxyignname.TOYTIME, game_address=2),
    locname.TOYTIMESTAR6: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME6CHAIN,
                                          170000089, galaxyignname.TOYTIME, game_address=3),
    locname.TOYTIMESTAR4: SMGLocationData(["Toy Time Galaxy", "Power Star Locations"], regname.TOYTIME4CHAIN,
                                          170000090, galaxyignname.TOYTIME, game_address=4)
}

locDD_table: dict[str, SMGLocationData]  = {
    locname.DEEPDARKSTAR1: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDA1SMAST,
                                           170000092, galaxyignname.DEEPDARK, game_address=0),
    locname.DEEPDARKSTAR2: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDA2MELON,
                                           170000093,galaxyignname.DEEPDARK, game_address=1),
    locname.DEEPDARKSTAR3: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDA3WATER,
                                           170000094,galaxyignname.DEEPDARK, game_address=2),
    locname.DEEPDARKSTAR4: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDA4SMAST,
                                           170000095,galaxyignname.DEEPDARK, game_address=3),
    locname.DEEPDARKSTAR6: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations"], regname.DEEPDA6BOOBX,
                                           170000097,galaxyignname.DEEPDARK, game_address=4)
}

locDN_table: dict[str, SMGLocationData]  = {
    locname.DREADNOUGHTSTAR1: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADN1PLATF,
                                              170000098, galaxyignname.DREADNOUGHT, game_address=0),
    locname.DREADNOUGHTSTAR2: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADN2AUTOS,
                                              170000099, galaxyignname.DREADNOUGHT, game_address=1),
    locname.DREADNOUGHTSTAR3: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADN3BOSSA,
                                              170000100, galaxyignname.DREADNOUGHT, game_address=2),
    locname.DREADNOUGHTSTAR4: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADN4BOSSA,
                                              170000101, galaxyignname.DREADNOUGHT, game_address=3),
    locname.DREADNOUGHTSTAR6: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations"], regname.DREADN6BREAK,
                                              170000103, galaxyignname.DREADNOUGHT, game_address=4)
}

locMM_table: dict[str, SMGLocationData]  = {
    locname.MELTYMOLTENSTAR1: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY1SINKI,
                                              170000104, galaxyignname.MELTYMOLTEN, game_address=0),
    locname.MELTYMOLTENSTAR2: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY2CIRCL,
                                              170000105, galaxyignname.MELTYMOLTEN, game_address=1),
    locname.MELTYMOLTENSTAR3: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY3FDINO,
                                              170000106, galaxyignname.MELTYMOLTEN, game_address=2),
    locname.MELTYMOLTENSTAR4: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY4SINKI,
                                              170000107, galaxyignname.MELTYMOLTEN, game_address=3),
    locname.MELTYMOLTENSTAR6: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations"], regname.MELTY6LAVAS,
                                              170000109, galaxyignname.MELTYMOLTEN, game_address=4)
}

locHL_table: dict[str, SMGLocationData]  = {
    locname.SWEETSWEETSTAR: SMGLocationData(["Sweet Sweet Galaxy", "Power Star Locations"], regname.SWEETSW1SWEET,
                                            170000110, galaxyignname.SWEETSWEET, game_address=0),
    locname.SLINGPODSTAR: SMGLocationData(["Sling Pod Galaxy", "Power Star Locations"], regname.SLINGPO1WEBPU,
                                          170000111, galaxyignname.SLINGPOD, game_address=0),
    locname.DRIPDROPSTAR: SMGLocationData(["Drip Drop Galaxy", "Power Star Locations"], regname.DRIPDRO1WATER,
                                          170000112, galaxyignname.DRIPDROP, game_address=0),
    locname.BIGMOUTHSTAR: SMGLocationData(["Bigmouth Galaxy", "Power Star Locations"], regname.BIGMOUT1UPPER,
                                          170000113, galaxyignname.BIGMOUTH, game_address=0),
    locname.SANDSPIRALSTAR: SMGLocationData(["Sand Spiral Galaxy", "Power Star Locations"], regname.SANDSPI1SPIRA,
                                            170000114, galaxyignname.SANDSPIRAL, game_address=0),
    locname.BOOSBONEYARDSTAR: SMGLocationData(["Boo's Boneyard Galaxy", "Power Star Locations"], regname.BOOBONE1PIT,
                                              170000115, galaxyignname.BOOBONE, game_address=0),
    locname.SNOWCAPSTAR: SMGLocationData(["Snow Cap Galaxy", "Power Star Locations"], regname.SNOWCAP1SNOWY,
                                         170000116, galaxyignname.SNOWCAP, game_address=0)
}

locPC_table: dict[str, SMGLocationData]  = {
    locname.TOYTIMESTAR5: SMGLocationData(["Toy Time Galaxy", "Power Star Locations", "Purple Coins"], regname.TOYTIME5LUIGI,
                                          170000091, galaxyignname.TOYTIME, game_address=5),
    locname.DREADNOUGHTSTAR5: SMGLocationData(["Dreadnought Galaxy", "Power Star Locations", "Purple Coins"], regname.DREADN5STARS,
                                              170000102, galaxyignname.DREADNOUGHT, game_address=5),
    locname.MELTYMOLTENSTAR5: SMGLocationData(["Melty Molten Galaxy", "Power Star Locations", "Purple Coins"], regname.MELTY5VOLCA,
                                              170000108, galaxyignname.MELTYMOLTEN, game_address=5),
    locname.DEEPDARKSTAR5: SMGLocationData(["Deep Dark Galaxy", "Power Star Locations", "Purple Coins"], regname.DEEPDA5SHIPC,
                                           170000096, galaxyignname.DEEPDARK, game_address=5),
    locname.SEASLIDESTAR5: SMGLocationData(["Sea Slide Galaxy", "Power Star Locations", "Purple Coins"], regname.SEASLI5SLIDE,
                                           170000084, galaxyignname.SEAGLIDE, game_address=5),
    locname.GOODEGGSTAR5: SMGLocationData(["Good Egg Galaxy", "Power Star Locations", "Purple Coins"], regname.GOODEGG5PEARP,
                                          170000005, galaxyignname.GOODEGG, game_address=5),
    locname.GATEWAYSTAR2: SMGLocationData([regname.GATEWAY, "Power Star Locations", "Purple Coins"], regname.GATEWAY2HOMEP,
                                          170000020, "HeavensDoorGalaxy", game_address=2),
    locname.BATTLEROCKSTAR5: SMGLocationData(["Battlerock Galaxy", "Power Star Locations", "Purple Coins"], regname.BATTLE5AUTOS,
                                             17000121, galaxyignname.BATTLEROCK, game_address=5),
    locname.SPACEJUNKSTAR5: SMGLocationData(["Space Junk Galaxy", "Power Star Locations", "Purple Coins"], regname.SPACJUN5PURPL,
                                            170000036, galaxyignname.SPACEJUNK, game_address=5),
    locname.GUSTYGARDENSTAR5: SMGLocationData(["Gusty Garden Galaxy", "Power Star Locations", "Purple Coins"], regname.GUSTY5CMAZE,
                                              170000059, galaxyignname.GUSTY, game_address=5),
    locname.BEACHBOWLSTAR5: SMGLocationData(["Beach Bowl Galaxy", "Power Star Locations", "Purple Coins"], regname.BEACH5LANDI,
                                            170000047, galaxyignname.BEACHBOWL, game_address=5),
    locname.FREEZEFLAMESTAR5: SMGLocationData(["Freezeflame Galaxy", "Power Star Locations", "Purple Coins"], regname.FREFLA5MOUNB,
                                              170000066, galaxyignname.FREEZEFLAME, game_address=5),
    locname.GHOSTLYSTAR5: SMGLocationData([regname.GHOSTLY, "Power Star Locations", "Purple Coins"], regname.GHOSTLY5PCOIN,
                                          170000053, galaxyignname.GHOSTLY, game_address=5),
    locname.GOLDLEAFSTAR5: SMGLocationData(["Gold Leaf Galaxy", "Power Star Locations", "Purple Coins"], regname.GOLDLE5CANNO,
                                           170000078, galaxyignname.GOLDLEAF, game_address=5),
    locname.DUSTYDUNESTAR5: SMGLocationData(["Dusty Dune Galaxy", "Power Star Locations", "Purple Coins"], regname.DUSTY5MAZEY,
                                            170000070, galaxyignname.DUSTYDUNE, game_address=5),
    locname.HONEYHIVESTAR5: SMGLocationData(["Honeyhive Galaxy", "Power Star Locations", "Purple Coins"], regname.HONEYHI5LANDI,
                                            170000011, galaxyignname.HONEYHIVE, game_address=5)
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
