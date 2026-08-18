from typing import TYPE_CHECKING

from BaseClasses import Entrance
from rule_builder.rules import HasGroup, Has
from .regions import connect_regions, region_list, all_galaxy_slots
from.Constants.Names import region_names as regname

if TYPE_CHECKING:
    from . import SMGWorld

# Cap the incoming offsets to the maximum of that area.

# main stage logic
def set_rules(world: "SMGWorld", player: int):
    # Dome 1
    world.get_region(regname.SHIP).connect(world.get_region(regname.TERRACE), "Dome 1 Entry")
    world.get_region(regname.TERRACE).connect(world.get_region(regname.GOODEGG), "Dome 1 First Orbit Galaxy")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG1HOTOW), "Good Egg 1: Dino Piranha")
    world.get_region(regname.GOODEGG1HOTOW).connect(world.get_region(regname.GOODEGG1HOTOP))
    world.get_region(regname.GOODEGG1HOTOP).connect(world.get_region(regname.GOODEGG6LUIGI))
    world.get_region(regname.GOODEGG1HOTOW).connect(world.get_region(regname.GOODEGG1TONOT),
                                                    "Good Egg 1: Tower Orange Pipe")
    world.get_region(regname.GOODEGG1TONOT).connect(world.get_region(regname.GOODEGG1HOTOP),
                                                    "Good Egg 1: Note Room Orange Pipe")
    world.get_region(regname.GOODEGG1HOTOW).connect(world.get_region(regname.GOODEGG1DUMBB),
                                                    "Good Egg 1: Towertop Sling & Launch Star")
    world.get_region(regname.GOODEGG1DUMBB).connect(world.get_region(regname.GOODEGG1SMLGR),
                                                    "Good Egg 1: Dumbbell Boulder Launch Star")
    world.get_region(regname.GOODEGG1SMLGR).connect(world.get_region(regname.GOODEGG1BOULD),
                                                    "Good Egg 1: Small Grass Planet Vine")
    world.get_region(regname.GOODEGG1BOULD).connect(world.get_region(regname.GOODEGG1PANEL),
                                                    "Good Egg 1: Boulder Black Hole Green Pipe")
    world.get_region(regname.GOODEGG1BOULD).connect(world.get_region(regname.GOODEGG1GRASS),
                                                    "Good Egg 1: Boulder Black Hole Vine")
    world.get_region(regname.GOODEGG1PANEL).connect(world.get_region(regname.GOODEGG1GRASS),
                                                    "Good Egg 1: Flipswitch Launch Star")
    world.get_region(regname.GOODEGG1GRASS).connect(world.get_region(regname.GOODEGG1DINOP),
                                                    "Good Egg 1: Grass Climb Launch Star")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG2HOTOW),
                                              "Good Egg 2: A Snack of Cosmic Proportions")
    world.get_region(regname.GOODEGG2HOTOW).connect(world.get_region(regname.GOODEGG2HOTOP))
    world.get_region(regname.GOODEGG2HOTOP).connect(world.get_region(regname.GOODEGG6LUIGI))
    world.get_region(regname.GOODEGG2HOTOW).connect(world.get_region(regname.GOODEGG2TONOT),
                                                    "Good Egg 2: Tower Orange Pipe")
    world.get_region(regname.GOODEGG2TONOT).connect(world.get_region(regname.GOODEGG2HOTOP),
                                                    "Good Egg 2: Note Room Orange Pipe")
    world.get_region(regname.GOODEGG2HOTOW).connect(world.get_region(regname.GOODEGG2PEARP),
                                                    "Good Egg 2: Tower Pull to Launch Star")
    world.get_region(regname.GOODEGG2PEARP).connect(world.get_region(regname.GOODEGG2ROCKY),
                                                    "Good Egg 2: Pear Launch Star")
    world.get_region(regname.GOODEGG2PEARP).connect(world.get_region(regname.GOODEGG2YOSHI),
                                                    "Good Egg 2: Pear Mid-Flight Launch Star")
    world.get_region(regname.GOODEGG2ROCKY).connect(world.get_region(regname.GOODEGG2YOSHI),
                                                    "Good Egg 2: Rocky Launch Star")
    world.get_region(regname.GOODEGG2ROCKY).connect(world.get_region(regname.GOODEGG2PEARP),
                                                    "Good Egg 2: Rocky Mid-Flight Launch Star")
    world.get_region(regname.GOODEGG2YOSHI).connect(world.get_region(regname.GOODEGG2PEARP),
                                                    "Good Egg 2: Yoshi Egg Launch Star")
    world.get_region(regname.GOODEGG2YOSHI).connect(world.get_region(regname.GOODEGG2ROCKY),
                                                    "Good Egg 2: Yoshi Egg Mid-Flight Launch Star")
    world.get_region(regname.GOODEGG2YOSHI).connect(world.get_region(regname.GOODEGG2TOWER),
                                                    "Good Egg 2: Yoshi Egg Hungry Luma Launch Star")
    world.get_region(regname.GOODEGG2TOWER).connect(world.get_region(regname.GOODEGG2CAPSU),
                                                    "Good Egg 2: Tower Climb Launch Star")
    world.get_region(regname.GOODEGG2CAPSU).connect(world.get_region(regname.GOODEGG2CAPSI))
    world.get_region(regname.GOODEGG2CAPSI).connect(world.get_region(regname.GOODEGG2STARP),
                                                    "Good Egg 2: Inside Capsule Launch Star")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG3HOTOW),
                                              "Good Egg 3: King Kaliente's Battle Fleet")
    world.get_region(regname.GOODEGG3HOTOW).connect(world.get_region(regname.GOODEGG3HOTOP))
    world.get_region(regname.GOODEGG3HOTOP).connect(world.get_region(regname.GOODEGG6LUIGI))
    world.get_region(regname.GOODEGG3HOTOW).connect(world.get_region(regname.GOODEGG3TONOT),
                                                    "Good Egg 3: Tower Orange Pipe")
    world.get_region(regname.GOODEGG3TONOT).connect(world.get_region(regname.GOODEGG3HOTOP),
                                                    "Good Egg 3: Note Room Orange Pipe")
    world.get_region(regname.GOODEGG3HOTOP).connect(world.get_region(regname.GOODEGG3PALMT),
                                                    "Good Egg 3: Housetop Launch Star")
    world.get_region(regname.GOODEGG3PALMT).connect(world.get_region(regname.GOODEGG3SANDY),
                                                    "Good Egg 3: Palm Tree Sling Star")
    world.get_region(regname.GOODEGG3SANDY).connect(world.get_region(regname.GOODEGG3CHOMP),
                                                    "Good Egg 3: Sandy Launch Star")
    world.get_region(regname.GOODEGG3CHOMP).connect(world.get_region(regname.GOODEGG3CHOMI),
                                                    "Good Egg 3: Meteor Pipe")
    world.get_region(regname.GOODEGG3CHOMP).connect(world.get_region(regname.GOODEGG3GRASS),
                                                    "Good Egg 3: Meteor Sling Star")
    world.get_region(regname.GOODEGG3GRASS).connect(world.get_region(regname.GOODEGG3SHIPS),
                                                    "Good Egg 3: UFO Grass Launch Star")
    world.get_region(regname.GOODEGG3SHIPS).connect(world.get_region(regname.GOODEGG3KBOSS),
                                                    "Good Egg 3: Ship Launch Star")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG4HOTOW),
                                              "Good Egg Comet: Dino Piranha Speed Run")
    world.get_region(regname.GOODEGG4HOTOW).connect(world.get_region(regname.GOODEGG4HOTOP))
    world.get_region(regname.GOODEGG4HOTOW).connect(world.get_region(regname.GOODEGG4TONOT),
                                                    "Good Egg Comet: Tower Orange Pipe")
    world.get_region(regname.GOODEGG4TONOT).connect(world.get_region(regname.GOODEGG4HOTOP),
                                                    "Good Egg Comet: Note Room Orange Pipe")
    world.get_region(regname.GOODEGG4HOTOW).connect(world.get_region(regname.GOODEGG4DUMBB),
                                                    "Good Egg Comet: Towertop Sling & Launch Star")
    world.get_region(regname.GOODEGG4DUMBB).connect(world.get_region(regname.GOODEGG4SMLGR),
                                                    "Good Egg Comet: Dumbbell Boulder Launch Star")
    world.get_region(regname.GOODEGG4SMLGR).connect(world.get_region(regname.GOODEGG4BOULD),
                                                    "Good Egg Comet: Small Grass Planet Vine")
    world.get_region(regname.GOODEGG4BOULD).connect(world.get_region(regname.GOODEGG4PANEL),
                                                    "Good Egg Comet: Boulder Black Hole Green Pipe")
    world.get_region(regname.GOODEGG4BOULD).connect(world.get_region(regname.GOODEGG4GRASS),
                                                    "Good Egg Comet: Boulder Black Hole Vine")
    world.get_region(regname.GOODEGG4PANEL).connect(world.get_region(regname.GOODEGG4GRASS),
                                                    "Good Egg Comet: Flipswitch Launch Star")
    world.get_region(regname.GOODEGG4GRASS).connect(world.get_region(regname.GOODEGG4DINOP),
                                                    "Good Egg Comet: Grass Climb Launch Star")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG5PEARP),
                                              "Good Egg Purple Coin: Purple Coin Omelet")
    world.get_region(regname.GOODEGG5PEARP).connect(world.get_region(regname.GOODEGG5ROCKY),
                                                    "Good Egg Purple Coin: Pear Launch Star")
    world.get_region(regname.GOODEGG5PEARP).connect(world.get_region(regname.GOODEGG5YOSHI),
                                                    "Good Egg Purple Coin: Pear Mid-Flight Launch Star")
    world.get_region(regname.GOODEGG5ROCKY).connect(world.get_region(regname.GOODEGG5YOSHI),
                                                    "Good Egg Purple Coin: Rocky Launch Star")
    world.get_region(regname.GOODEGG5ROCKY).connect(world.get_region(regname.GOODEGG5PEARP),
                                                    "Good Egg Purple Coin: Rocky Mid-Flight Launch Star")
    world.get_region(regname.GOODEGG5YOSHI).connect(world.get_region(regname.GOODEGG5PEARP),
                                                    "Good Egg Purple Coin: Yoshi Egg Launch Star")
    world.get_region(regname.GOODEGG5YOSHI).connect(world.get_region(regname.GOODEGG5ROCKY),
                                                    "Good Egg Purple Coin: Yoshi Egg Mid-Flight Launch Star")

    world.get_region(regname.TERRACE).connect(world.get_region(regname.HONEYHIVE), "Dome 1 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_one_counts["Second Orbit"], 4)))
    world.get_region(regname.HONEYHIVE).connect(world.get_region(regname.HONEYHI1LANDI),
                                                    "Honeyhive 1: Bee Mario Takes Flight")
    world.get_region(regname.HONEYHI1LANDI).connect(world.get_region(regname.HONEYHI1SIDEP))
    world.get_region(regname.HONEYHI1LANDI).connect(world.get_region(regname.HONEYHI1WATRP))
    world.get_region(regname.HONEYHI1POUND).connect(world.get_region(regname.HONEYHI1FOUNC))
    world.get_region(regname.HONEYHI1WATRP).connect(world.get_region(regname.HONEYHI1WATRT))
    world.get_region(regname.HONEYHI1WATRT).connect(world.get_region(regname.HONEYHI1POUND))
    world.get_region(regname.HONEYHI1POUND).connect(world.get_region(regname.HONEYHI6LUIGI))
    world.get_region(regname.HONEYHI1POUND).connect(world.get_region(regname.HONEYHI1BIGTR))
    world.get_region(regname.HONEYHI1WATRT).connect(world.get_region(regname.HONEYHI1UNDER))
    world.get_region(regname.HONEYHI1UNDER).connect(world.get_region(regname.HONEYHI1GARDN),
                                                    "Honeyhive 1: Undercliff Launch Star")
    world.get_region(regname.HONEYHI1GARDN).connect(world.get_region(regname.HONEYHI1HONYC),
                                                    "Honeyhive 1: Garden Launch Star")
    world.get_region(regname.HONEYHI1HONYC).connect(world.get_region(regname.HONEYHI1PONDT))
    world.get_region(regname.HONEYHI1PONDT).connect(world.get_region(regname.HONEYHI1TREET),
                                                    "Honeyhive 1: Queen Bee Launch Star")
    world.get_region(regname.HONEYHIVE).connect(world.get_region(regname.HONEYHI2LANDI),
                                                    "Honeyhive 2: Trouble on the Tower")
    world.get_region(regname.HONEYHI2LANDI).connect(world.get_region(regname.HONEYHI2SIDEP))
    world.get_region(regname.HONEYHI2LANDI).connect(world.get_region(regname.HONEYHI2WATRP))
    world.get_region(regname.HONEYHI2LANDI).connect(world.get_region(regname.HONEYHI2BIGTR),
                                                    "Honeyhive 2: Landing Ground Pound Vine")
    world.get_region(regname.HONEYHI2BIGTR).connect(world.get_region(regname.HONEYHI2POUND),
                                                    "Honeyhive 2: Big Tree Sling Star")
    world.get_region(regname.HONEYHI2POUND).connect(world.get_region(regname.HONEYHI6LUIGI))
    world.get_region(regname.HONEYHI2POUND).connect(world.get_region(regname.HONEYHI2CLIFF))
    world.get_region(regname.HONEYHI2CLIFF).connect(world.get_region(regname.HONEYHI2FOUNC))
    world.get_region(regname.HONEYHI2CLIFF).connect(world.get_region(regname.HONEYHI2WATRT))
    world.get_region(regname.HONEYHI2CLIFF).connect(world.get_region(regname.HONEYHI2HATS2),
                                                    "Honeyhive 2: Clifftop Launch Star")
    world.get_region(regname.HONEYHI2HATS2).connect(world.get_region(regname.HONEYHI2DROPL),
                                                    "Honeyhive 2: Hat Planets Sling Star")
    world.get_region(regname.HONEYHI2DROPL).connect(world.get_region(regname.HONEYHI2TOWRB))
    world.get_region(regname.HONEYHI2TOWRB).connect(world.get_region(regname.HONEYHI2TOWRM))
    world.get_region(regname.HONEYHI2TOWRM).connect(world.get_region(regname.HONEYHI2TOWRT))
    world.get_region(regname.HONEYHI2WATRT).connect(world.get_region(regname.HONEYHI2UNDER))
    world.get_region(regname.HONEYHI2UNDER).connect(world.get_region(regname.HONEYHI2SMLHI),
                                                    "Honeyhive 2: Undercliff Return Pipe")
    world.get_region(regname.HONEYHIVE).connect(world.get_region(regname.HONEYHI3LANDI),
                                                    "Honeyhive 3: Big Bad Bugaboom")
    world.get_region(regname.HONEYHI3LANDI).connect(world.get_region(regname.HONEYHI3SIDEP))
    world.get_region(regname.HONEYHI3LANDI).connect(world.get_region(regname.HONEYHI3WATRP))
    world.get_region(regname.HONEYHI3LANDI).connect(world.get_region(regname.HONEYHI3POUND))
    world.get_region(regname.HONEYHI3POUND).connect(world.get_region(regname.HONEYHI3FOUNC))
    world.get_region(regname.HONEYHI3WATRP).connect(world.get_region(regname.HONEYHI3WATRT))
    world.get_region(regname.HONEYHI3POUND).connect(world.get_region(regname.HONEYHI6LUIGI))
    world.get_region(regname.HONEYHI3POUND).connect(world.get_region(regname.HONEYHI3BIGTR))
    world.get_region(regname.HONEYHI3WATRT).connect(world.get_region(regname.HONEYHI3UNDER))
    world.get_region(regname.HONEYHI3UNDER).connect(world.get_region(regname.HONEYHI3SMLHI),
                                                    "Hineyhive 3: Undercliff Return Pipe")
    world.get_region(regname.HONEYHI3WATRT).connect(world.get_region(regname.HONEYHI3BUGLA),
                                                    "Honeyhive 3: Waterfall Tunnel Launch Star")
    world.get_region(regname.HONEYHI3BIGTR).connect(world.get_region(regname.HONEYHI3LANDI),
                                                    "Honeyhive 3: Big Tree Return Pipe")
    world.get_region(regname.HONEYHI3BUGLA).connect(world.get_region(regname.HONEYHI3BUGAB))
    world.get_region(regname.HONEYHIVE).connect(world.get_region(regname.HONEYHI4LANDI),
                                                    "Honeyhive Comet: Honeyhive Cosmic Mario Race")
    world.get_region(regname.HONEYHI4LANDI).connect(world.get_region(regname.HONEYHI4WATRP))
    world.get_region(regname.HONEYHI4WATRP).connect(world.get_region(regname.HONEYHI4WATRT))
    world.get_region(regname.HONEYHI4WATRT).connect(world.get_region(regname.HONEYHI4UNDER))
    world.get_region(regname.HONEYHIVE).connect(world.get_region(regname.HONEYHI5LANDI),
                                                    "Honeyhive Purple Coins: The Honeyhive's Purple Coins")
    world.get_region(regname.HONEYHI5LANDI).connect(world.get_region(regname.HONEYHI5SIDEP))
    world.get_region(regname.HONEYHI5LANDI).connect(world.get_region(regname.HONEYHI5WATRP))
    world.get_region(regname.HONEYHI5LANDI).connect(world.get_region(regname.HONEYHI5BIGTR),
                                                    "Honeyhive Purple Coin: Landing Ground Pound Vine")
    world.get_region(regname.HONEYHI5SIDEP).connect(world.get_region(regname.HONEYHI5SMLHI))
    world.get_region(regname.HONEYHI5BIGTR).connect(world.get_region(regname.HONEYHI5POUND),
                                                    "Honeyhive Purple Coin: Big Tree Sling Star")
    world.get_region(regname.HONEYHI5POUND).connect(world.get_region(regname.HONEYHI5CLIFF))
    world.get_region(regname.HONEYHI5POUND).connect(world.get_region(regname.HONEYHI5FOUNC))
    world.get_region(regname.HONEYHI5CLIFF).connect(world.get_region(regname.HONEYHI5FOUNC))
    world.get_region(regname.HONEYHI5CLIFF).connect(world.get_region(regname.HONEYHI5WATRT))
    world.get_region(regname.HONEYHI5WATRT).connect(world.get_region(regname.HONEYHI5UNDER))
    world.get_region(regname.HONEYHI5UNDER).connect(world.get_region(regname.HONEYHI5SMLHI),
                                                    "Honeyhive Purple Coin: Undercliff Return Pipe")
    world.get_region(regname.TERRACE).connect(world.get_region(regname.LOOPDEELOOP), "Dome 1 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_one_counts["Third Orbit"], 5)))
    world.get_region(regname.LOOPDEELOOP).connect(world.get_region(regname.LOOPDLO1ENTRY),
                                                  "Loopdeeloop: Surfing 101")
    world.get_region(regname.LOOPDLO1ENTRY).connect(world.get_region(regname.LOOPDLO1COURS))
    world.get_region(regname.TERRACE).connect(world.get_region(regname.FLIPSWITCH), "Dome 1 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_one_counts["Fourth Orbit"], 6)))
    world.get_region(regname.FLIPSWITCH).connect(world.get_region(regname.FLIPSWI1PANEL),
                                                 "Flipswitch: Painting the Planet Yellow")
    world.get_region(regname.TERRACE).connect(world.get_region(regname.BOWJR1), "Dome 1 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_one_counts["Fifth Orbit"], 7)))
    world.get_region(regname.BOWJR1).connect(world.get_region(regname.ROBOTRE1CAGEB),
                                             "Robot Reactor: Megaleg's Moon")
    world.get_region(regname.ROBOTRE1CAGEB).connect(world.get_region(regname.ROBOTRE1MEGAL),
                                                    "Robot Reactor: Cage Break Launch Star")
    # Dome 2
    world.get_region(regname.SHIP).connect(world.get_region(regname.FOUNTAIN), "Dome 2 Entry",
                    Has("Grand Star"))
    world.get_region(regname.FOUNTAIN).connect(world.get_region(regname.SPACEJUNK), "Dome 2 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_two_counts["First Orbit"], 8)))
    world.get_region(regname.SPACEJUNK).connect(world.get_region(regname.SPACJUN1LANDI),
                                                    "Space Junk 1: Pull Star Path")
    world.get_region(regname.SPACJUN1LANDI).connect(world.get_region(regname.SPACJUN1CRYCY))
    world.get_region(regname.SPACJUN1CRYCY).connect(world.get_region(regname.SPACJUN1SPHE3))
    world.get_region(regname.SPACJUN1SPHE3).connect(world.get_region(regname.SPACJUN1HSHIP),
                                                    "Space Junk 1: Three Spheres Launch Star")
    world.get_region(regname.SPACJUN1HSHIP).connect(world.get_region(regname.SPACJUN1TOADS))
    world.get_region(regname.SPACJUN1TOADS).connect(world.get_region(regname.SPACJUN1SILVE),
                                                    "Space Junk 1: Toadship Sling Star")
    world.get_region(regname.SPACEJUNK).connect(world.get_region(regname.SPACJUN2TOADS),
                                                    "Space Junk 2: Kamella's Airship Attack")
    world.get_region(regname.SPACJUN2TOADS).connect(world.get_region(regname.SPACJUN2AIRS1),
                                                    "Space Junk 2: Toadship Launch Star")
    world.get_region(regname.SPACJUN2AIRS1).connect(world.get_region(regname.SPACJUN2AIRS2),
                                                    "Space Junk 2: Meteor Platform Sling Star")
    world.get_region(regname.SPACJUN2AIRS2).connect(world.get_region(regname.SPACJUN2AIRS3),
                                                    "Space Junk 2: Airship Launch Star")
    world.get_region(regname.SPACJUN2AIRS3).connect(world.get_region(regname.SPACJUN2AIRSI),
                                                    "Space Junk 2: Third Airship Chimney")
    world.get_region(regname.SPACJUN2AIRS3).connect(world.get_region(regname.SPACJUN2BATTL),
                                                    "Space Junk 2: Bridge Sling Star")
    world.get_region(regname.SPACEJUNK).connect(world.get_region(regname.SPACJUN3TOADS),
                                                    "Space Junk 2: Tarantox's Tangled Web")
    world.get_region(regname.SPACJUN3TOADS).connect(world.get_region(regname.SPACJUN3CRYCY))
    world.get_region(regname.SPACJUN3CRYCY).connect(world.get_region(regname.SPACJUN3GLASS))
    world.get_region(regname.SPACJUN3GLASS).connect(world.get_region(regname.SPACJUN6YOSHI),
                                                    "Space Junk Secret: Hungry Luma Launch Star")
    world.get_region(regname.SPACJUN3GLASS).connect(world.get_region(regname.SPACJUN3FLOAT),
                                                    "Space Junk 2: Under Glass Launch Star")
    world.get_region(regname.SPACJUN3FLOAT).connect(world.get_region(regname.SPACJUN3HSHIP))
    world.get_region(regname.SPACJUN3HSHIP).connect(world.get_region(regname.SPACJUN3TARAN))
    world.get_region(regname.SPACEJUNK).connect(world.get_region(regname.SPACJUN4LANDI),
                                                    "Space Junk Comet: Pull Star Path Speed Run")
    world.get_region(regname.SPACJUN4LANDI).connect(world.get_region(regname.SPACJUN4CRYCY))
    world.get_region(regname.SPACJUN4CRYCY).connect(world.get_region(regname.SPACJUN4SPHE3))
    world.get_region(regname.SPACJUN4SPHE3).connect(world.get_region(regname.SPACJUN4HSHIP),
                                                    "Space Junk Comet: Three Spheres Launch Star")
    world.get_region(regname.SPACJUN4HSHIP).connect(world.get_region(regname.SPACJUN4TOADS))
    world.get_region(regname.SPACJUN4TOADS).connect(world.get_region(regname.SPACJUN4SILVE),
                                                    "Space Junk Comet: Toadship Sling Star")
    world.get_region(regname.SPACEJUNK).connect(world.get_region(regname.SPACJUN5PURPL),
                                                    "Space Junk Purple Coins: Purple Coin Spacewalk")
    world.get_region(regname.FOUNTAIN).connect(world.get_region(regname.ROLLINGGREEN), "Dome 2 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_two_counts["Second Orbit"], 9)))
    world.get_region(regname.ROLLINGGREEN).connect(world.get_region(regname.ROLLGRESTART),
                                                    "Rolling Green: Rolling in the Clouds")
    world.get_region(regname.ROLLGRESTART).connect(world.get_region(regname.ROLLGREBATTL))
    world.get_region(regname.ROLLGREBATTL).connect(world.get_region(regname.ROLLGREFINIS))
    world.get_region(regname.FOUNTAIN).connect(world.get_region(regname.BATTLEROCK), "Dome 2 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_two_counts["Third Orbit"], 10)))
    world.get_region(regname.BATTLEROCK).connect(world.get_region(regname.BATTLE1LANDI),
                                                    "Battlerock 1: Battlerock Barrage")
    world.get_region(regname.BATTLE1LANDI).connect(world.get_region(regname.BATTLE1SPINY),
                                                    "Battlerock 1: Landing Launch Star")
    world.get_region(regname.BATTLE1SPINY).connect(world.get_region(regname.BATTLE1AUTOS))
    world.get_region(regname.BATTLE1AUTOS).connect(world.get_region(regname.BATTLE1FINAL))
    world.get_region(regname.BATTLE1FINAL).connect(world.get_region(regname.BATTLE7LUIGI))
    world.get_region(regname.BATTLEROCK).connect(world.get_region(regname.BATTLE2LANDI),
                                                    "Battlerock 2: Breaking into the Battlerock")
    world.get_region(regname.BATTLE2LANDI).connect(world.get_region(regname.BATTLE2TETRA),
                                                    "Battlerock 2: Landing Launch Star")
    world.get_region(regname.BATTLE2TETRA).connect(world.get_region(regname.BATTLE6BREAK),
                                                    "Battlerock Secret: Hungry Luma Launch Star")
    world.get_region(regname.BATTLE2TETRA).connect(world.get_region(regname.BATTLE2MINEF),
                                                    "Battlerock 2: Color Orbs  Launch Star")
    world.get_region(regname.BATTLE2MINEF).connect(world.get_region(regname.BATTLE2CAGEO),
                                                    "Battlerock 2: Minefield Launch Star")
    world.get_region(regname.BATTLE2CAGEO).connect(world.get_region(regname.BATTLE2CAGEI),
                                                    "Battlerock 2: Container Green Pipe")
    world.get_region(regname.BATTLE2CAGEI).connect(world.get_region(regname.BATTLE2PATCH),
                                                    "Battlerock 2: Caged Launch Star")
    world.get_region(regname.BATTLEROCK).connect(world.get_region(regname.BATTLE3LANDI),
                                                    "Battlerock 3: Topmaniac and the Topman Tribe")
    world.get_region(regname.BATTLE3LANDI).connect(world.get_region(regname.BATTLE3TRIPL),
                                                    "Battlerock 3: Landing Sling Star")
    world.get_region(regname.BATTLE3TRIPL).connect(world.get_region(regname.BATTLE3LUMAP),
                                                    "Battlerock 3: Triple Platform Launch Star")
    world.get_region(regname.BATTLE3LUMAP).connect(world.get_region(regname.BATTLE3CLIFF),
                                                    "Battlerock 3: Luma Launch Star")
    world.get_region(regname.BATTLE3CLIFF).connect(world.get_region(regname.BATTLE3INSID),
                                                    "Battlerock 3: Cliffside Green Pipe")
    world.get_region(regname.BATTLE3INSID).connect(world.get_region(regname.BATTLE3BCAGE),
                                                    "Battlerock 3: Near Crusher Green pipe")
    world.get_region(regname.BATTLE3BCAGE).connect(world.get_region(regname.BATTLE3EXITG),
                                                    "Battlerock 3: Circle Room Sling Star")
    world.get_region(regname.BATTLE3EXITG).connect(world.get_region(regname.BATTLE3TOPMA),
                                                    "Battlerock 3: Electric Gate Launch Star")
    world.get_region(regname.BATTLEROCK).connect(world.get_region(regname.BATTLE4TOPMA),
                                                 "Battlerock Comet: Topmaniac's Daredevil Run")
    world.get_region(regname.BATTLEROCK).connect(world.get_region(regname.BATTLE5AUTOS),
                                                    "Battlerock Purple Coins: Purple Coins on the Battlerock")
    world.get_region(regname.FOUNTAIN).connect(world.get_region(regname.HURRYSCUR), "Dome 2 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_two_counts["Fourth Orbit"], 11)))
    world.get_region(regname.HURRYSCUR).connect(world.get_region(regname.HURRSCULANDI),
                                                    "Hurry-Scurry: Shrinking Satellite")
    world.get_region(regname.HURRSCULANDI).connect(world.get_region(regname.HURRSCUPLANE),
                                                    "Hurry-Scurry: Falling Launch Star")
    world.get_region(regname.FOUNTAIN).connect(world.get_region(regname.BOWSER1), "Dome 2 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_two_counts["Fifth Orbit"], 12)))
    world.get_region(regname.BOWSER1).connect(world.get_region(regname.STARREALPIPE),
                                                    "Star Reactor: The Fiery Stronghold")
    world.get_region(regname.STARREALPIPE).connect(world.get_region(regname.STAREAGRAVIT))
    world.get_region(regname.STAREAGRAVIT).connect(world.get_region(regname.STAREASTAIRS))
    world.get_region(regname.STAREASTAIRS).connect(world.get_region(regname.STAREABOSSAR))
    # Dome 3
    world.get_region(regname.SHIP).connect(world.get_region(regname.KITCHEN), "Dome 3 Entry",
                    Has("Grand Star", 2))
    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BEACHBOWL), "Dome 3 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["First Orbit"], 13)))
    world.get_region(regname.BEACHBOWL).connect(world.get_region(regname.BEACH1LANDI),
                                                    "Beach Bowl 1: Sunken Treasure")
    world.get_region(regname.BEACH1LANDI).connect(world.get_region(regname.BEACH1BLOCK))
    world.get_region(regname.BEACH1LANDI).connect(world.get_region(regname.BEACH1LAKES))
    world.get_region(regname.BEACH1LANDI).connect(world.get_region(regname.BEACH1CLIFB))
    world.get_region(regname.BEACH1LAKES).connect(world.get_region(regname.BEACH1CLIFB),
                                                    "Beach Bowl 1: Lake Bottom Launch Star")
    world.get_region(regname.BEACH1CLIFB).connect(world.get_region(regname.BEACH1CLIFT))
    world.get_region(regname.BEACHBOWL).connect(world.get_region(regname.BEACH2LANDI),
                                                    "Beach Bowl 2: Passing the Swim Test")
    world.get_region(regname.BEACH2LANDI).connect(world.get_region(regname.BEACH2BLOCK))
    world.get_region(regname.BEACH2LANDI).connect(world.get_region(regname.BEACH2LAKES))
    world.get_region(regname.BEACH2LANDI).connect(world.get_region(regname.BEACH6WATRB),
                                                    "Beach Bowl 2: Hidden Treasure Launch Star")
    world.get_region(regname.BEACH6WATRB).connect(world.get_region(regname.BEACH6ICELA))
    world.get_region(regname.BEACHBOWL).connect(world.get_region(regname.BEACH3LANDI),
                                                    "Beach Bowl 3: The Secret Undersea Cavern")
    world.get_region(regname.BEACH3LANDI).connect(world.get_region(regname.BEACH3BLOCK))
    world.get_region(regname.BEACH3LANDI).connect(world.get_region(regname.BEACH3LAKES))
    world.get_region(regname.BEACH3LAKES).connect(world.get_region(regname.BEACH3CAVES))
    world.get_region(regname.BEACH3CAVES).connect(world.get_region(regname.BEACH3STCYC),
                                                  "Beach Bowl 3: Cavern Launch Star")
    world.get_region(regname.BEACH3LANDI).connect(world.get_region(regname.BEACH6WATRB),
                                                    "Beach Bowl 3: Hidden Treasure Launch Star")
    world.get_region(regname.BEACHBOWL).connect(world.get_region(regname.BEACH4STCYC),
                                                    "Beach Bowl Comet: Fast Foes on the Cyclone Stone")
    world.get_region(regname.BEACHBOWL).connect(world.get_region(regname.BEACH5LANDI),
                                                    "Beach Bowl Purple Coins: Beachcombing for Purple Coins")
    world.get_region(regname.BEACH5LANDI).connect(world.get_region(regname.BEACH5LAKES))
    world.get_region(regname.BEACH5LANDI).connect(world.get_region(regname.BEACH5CLIFB))
    world.get_region(regname.BEACH5CLIFB).connect(world.get_region(regname.BEACH5CLIFT))

    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BUBBLEBREEZE), "Dome 3 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Second Orbit"], 14)))
    world.get_region(regname.BUBBLEBREEZE).connect(world.get_region(regname.BUBBRE1SWAMP1),
                                                    "Bubble Breeze: Through the Poison Swamp")
    world.get_region(regname.BUBBRE1SWAMP1).connect(world.get_region(regname.BUBBRE1SWAMP2),
                                                    "Bubble Breeze: Swamp Launch Star")

    world.get_region(regname.KITCHEN).connect(world.get_region(regname.GHOSTLY), "Dome 3 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Third Orbit"], 15)))
    world.get_region(regname.GHOSTLY).connect(world.get_region(regname.GHOSTLY1TOADS),
                                                    "Ghostly 1: Luigi and the Haunted Mansion")
    world.get_region(regname.GHOSTLY1TOADS).connect(world.get_region(regname.GHOSTLY1ENTRY),
                                                    "Ghostly 1: Toadship Launch Star")
    world.get_region(regname.GHOSTLY1ENTRY).connect(world.get_region(regname.GHOSTLY1FOYER))
    world.get_region(regname.GHOSTLY1FOYER).connect(world.get_region(regname.GHOSTLY1BLACK),
                                                    "Ghostly 1: Foyer Locked Door")
    world.get_region(regname.GHOSTLY1BLACK).connect(world.get_region(regname.GHOSTLY1LIBRA))
    world.get_region(regname.GHOSTLY1BLACK).connect(world.get_region(regname.GHOSTLY1BALCO),
                                                    "Ghostly 1: Black Hole Launch Star")
    world.get_region(regname.GHOSTLY1BALCO).connect(world.get_region(regname.GHOSTLY1CORR1),
                                                    "Ghostly 1: Balcony Locked Door")
    world.get_region(regname.GHOSTLY1CORR1).connect(world.get_region(regname.GHOSTLY1CORR2))
    world.get_region(regname.GHOSTLY).connect(world.get_region(regname.GHOSTLY2TOADS),
                                                    "Ghostly 2: A Very Spooky Spirit")
    world.get_region(regname.GHOSTLY2TOADS).connect(world.get_region(regname.GHOSTLY2ENTRY),
                                                    "Ghostly 2: Toadship Launch Star")
    world.get_region(regname.GHOSTLY2ENTRY).connect(world.get_region(regname.GHOSTLY2BOORA),
                                                    "Ghostly 2: Pull Star Launch Star")
    world.get_region(regname.GHOSTLY).connect(world.get_region(regname.GHOSTLY3TOADS),
                                                    "Ghostly 3: Beware of Bouldergeist")
    world.get_region(regname.GHOSTLY3TOADS).connect(world.get_region(regname.GHOSTLY3ENTRY),
                                                    "Ghostly 3: Toadship Launch Star")
    world.get_region(regname.GHOSTLY3ENTRY).connect(world.get_region(regname.GHOSTLY3FOYER))
    world.get_region(regname.GHOSTLY3FOYER).connect(world.get_region(regname.GHOSTLY3SPIDE),
                                                    "Ghostly 3: Foyer Launch Star")
    world.get_region(regname.GHOSTLY3SPIDE).connect(world.get_region(regname.GHOSTLY3SLING),
                                                    "Ghostly 3: Spider Wall Launch Star")
    world.get_region(regname.GHOSTLY3SLING).connect(world.get_region(regname.GHOSTLY3TRAMP),
                                                    "Ghostly 3: Sling Pod Launch Star")
    world.get_region(regname.GHOSTLY3TRAMP).connect(world.get_region(regname.GHOSTLY3BOSSA),
                                                    "Ghostly 3: Trampoline Launch Star")
    world.get_region(regname.GHOSTLY).connect(world.get_region(regname.GHOSTLY4BOSSA),
                                                    "Ghostly Comet: Bouldergeist's Daredevil Run")
    world.get_region(regname.GHOSTLY).connect(world.get_region(regname.GHOSTLY5PCOIN),
                                                    "Ghostly Purple Coins: Purple Coins in the Bone Pen")

    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BUOY), "Dome 3 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Fourth Orbit"], 16)))
    world.get_region(regname.BUOY).connect(world.get_region(regname.BUOY1LAKES),
                                                    "Buoy Base: The Floating Fortress")
    world.get_region(regname.BUOY1LAKES).connect(world.get_region(regname.BUOY1UNDER),
                                                    "Buoy Base Secret: Underwater Green Pipe")
    world.get_region(regname.BUOY1LAKES).connect(world.get_region(regname.BUOY1TOWER))
    world.get_region(regname.BUOY1TOWER).connect(world.get_region(regname.BUOY1WATER))

    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BOWJR2), "Dome 3 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Fifth Orbit"], 17)))
    world.get_region(regname.BOWJR2).connect(world.get_region(regname.AIRARM1AIRS1),
                                                    "Airship Armada: Sinking the Airships")
    world.get_region(regname.AIRARM1AIRS1).connect(world.get_region(regname.AIRARM1AIRS2))
    world.get_region(regname.AIRARM1AIRS1).connect(world.get_region(regname.AIRARM1GOOMB))
    world.get_region(regname.AIRARM1GOOMB).connect(world.get_region(regname.AIRARM1AIRS2))
    world.get_region(regname.AIRARM1AIRS2).connect(world.get_region(regname.AIRARM1AIRS3))
    world.get_region(regname.AIRARM1AIRS2).connect(world.get_region(regname.AIRARM1GOOMB))
    world.get_region(regname.AIRARM1AIRS3).connect(world.get_region(regname.AIRARM1AUTOS))
    world.get_region(regname.AIRARM1AUTOS).connect(world.get_region(regname.AIRARM1BATTL))

    # Dome 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.BEDROOM), "Dome 4 Entry",
                    Has("Grand Star", 3))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.GUSTY), "Dome 4 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["First Orbit"], 18)))
    world.get_region(regname.GUSTY).connect(world.get_region(regname.GUSTY1LANDI),
                                                    "Gusty Garden 1: Bunnies in the Wind")
    world.get_region(regname.GUSTY1LANDI).connect(world.get_region(regname.GUSTY1PILLR))
    world.get_region(regname.GUSTY1PILLR).connect(world.get_region(regname.GUSTY1BAGMA))
    world.get_region(regname.GUSTY1BAGMA).connect(world.get_region(regname.GUSTY1VINEY))
    world.get_region(regname.GUSTY1VINEY).connect(world.get_region(regname.GUSTY1CMAZE),
                                                  "Gusty Garden 1: Footprints Launch Star")
    world.get_region(regname.GUSTY).connect(world.get_region(regname.GUSTY2LANDI),
                                                    "Gusty Garden 2: The Dirty Tricks of Major Burrows")
    world.get_region(regname.GUSTY2LANDI).connect(world.get_region(regname.GUSTY2PILLR))
    world.get_region(regname.GUSTY2PILLR).connect(world.get_region(regname.GUSTY2QUESD))
    world.get_region(regname.GUSTY2QUESD).connect(world.get_region(regname.GUSTY2QUEST),
                                                  "Gusty Garden 2: Dot Sling Star")
    world.get_region(regname.GUSTY2QUEST).connect(world.get_region(regname.GUSTY2APPLE),
                                                  "Gusty Garden 2: Question Hook Launch Star")
    world.get_region(regname.GUSTY2QUEST).connect(world.get_region(regname.GUSTY2GRATE),
                                                  "Gusty Garden 2: Hook Pull to Launch Star")
    world.get_region(regname.GUSTY2GRATE).connect(world.get_region(regname.GUSTY2APPLE),
                                                  "Gusty Garden 2: Grate Launch Star")
    world.get_region(regname.GUSTY2APPLE).connect(world.get_region(regname.GUSTY2VINED),
                                                  "Gusty Garden 2: Apples Launch Star")
    world.get_region(regname.GUSTY2VINED).connect(world.get_region(regname.GUSTY2BOSST),
                                                  "Gusty Garden 2: Vined Launch Star")
    world.get_region(regname.GUSTY).connect(world.get_region(regname.GUSTY3LANDI),
                                                    "Gusty Garden 3: Gusty Garden's Gravity Scramble")
    world.get_region(regname.GUSTY3LANDI).connect(world.get_region(regname.GUSTY3GRASS))
    world.get_region(regname.GUSTY3GRASS).connect(world.get_region(regname.GUSTY3PEARL),
                                                  "Gusty Garden 3: Footprint Launch Star")
    world.get_region(regname.GUSTY3PEARL).connect(world.get_region(regname.GUSTY3CYMBA),
                                                  "Gusty Garden 3: Grass Pearls Launch Star")
    world.get_region(regname.GUSTY3CYMBA).connect(world.get_region(regname.GUSTY3BLOCK),
                                                  "Gusty Garden 3: Cymbal Launch Star")
    world.get_region(regname.GUSTY).connect(world.get_region(regname.GUSTY4BOSST),
                                                    "Gusty Garden Comet: Major Burrows's Daredevil Run")
    world.get_region(regname.GUSTY).connect(world.get_region(regname.GUSTY5CMAZE),
                                                    "Gusty Garden Purple Coins: Purple Coins on the Puzzle Cube")

    world.get_region(regname.BEDROOM).connect(world.get_region(regname.FREEZEFLAME), "Dome 4 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Second Orbit"], 19)))
    world.get_region(regname.FREEZEFLAME).connect(world.get_region(regname.FREFLA1ICERI),
                                                    "Freezeflame 1: The Frozen Peak of Baron Brrr")
    world.get_region(regname.FREFLA1ICERI).connect(world.get_region(regname.FREFLA1MOUNB),
                                                   "Freezeflame 1: Ice Ring Launch Star")
    world.get_region(regname.FREFLA1MOUNB).connect(world.get_region(regname.FREFLA1SLIDE),
                                                   "Freezeflame 1: Sling Star to Slide")
    world.get_region(regname.FREFLA1MOUNB).connect(world.get_region(regname.FREFLA1MIDDL),
                                                   "Freezeflame 1: Mountain Base Sling Star")
    world.get_region(regname.FREFLA1MOUNB).connect(world.get_region(regname.FREFLA6BACK1),
                                                   "Freezeflame Secret: Ice Jump Sling Star")
    world.get_region(regname.FREFLA1MIDDL).connect(world.get_region(regname.FREFLA1BARBR),
                                                   "Freezeflame 1: Middle Ponds Sling Star")
    world.get_region(regname.FREFLA6BACK1).connect(world.get_region(regname.FREFLA6BACK2),
                                                   "Freezeflame Secret: First Snowman Sling Star")
    world.get_region(regname.FREFLA6BACK2).connect(world.get_region(regname.FREFLA6BACK3),
                                                   "Freezeflame Secret: Second Snowman Sling Star")
    world.get_region(regname.FREEZEFLAME).connect(world.get_region(regname.FREFLA2ICERI),
                                                    "Freezeflame 2: Freezeflame's Blistering Core")
    world.get_region(regname.FREFLA2ICERI).connect(world.get_region(regname.FREFLA2LAVA1),
                                                   "Freezeflame 2: Ice Ring Launch Star")
    world.get_region(regname.FREFLA2LAVA1).connect(world.get_region(regname.FREFLA2LAVA2))
    world.get_region(regname.FREFLA2LAVA2).connect(world.get_region(regname.FREFLA2LAVA3))
    world.get_region(regname.FREFLA2LAVA3).connect(world.get_region(regname.FREFLA2LAVAC))
    world.get_region(regname.FREEZEFLAME).connect(world.get_region(regname.FREFLA3ICERI),
                                                    "Freezeflame 3: Hot and Cold Collide")
    world.get_region(regname.FREFLA3ICERI).connect(world.get_region(regname.FREFLA3ICELA),
                                                   "Freezeflame 3: Ice Ring Launch Star")
    world.get_region(regname.FREFLA3ICELA).connect(world.get_region(regname.FREFLA3ICEFI),
                                                   "Freezeflame 3: Ice Lake Launch Star")
    world.get_region(regname.FREEZEFLAME).connect(world.get_region(regname.FREFLA4ICEFI),
                                                    "Freezeflame Comet: Frosty Cosmic Mario Race")
    world.get_region(regname.FREEZEFLAME).connect(world.get_region(regname.FREFLA5MOUNB),
                                                    "Freezeflame Purple Coins: Purple Coins on the Summit")
    world.get_region(regname.FREFLA5MOUNB).connect(world.get_region(regname.FREFLA5SLIDE),
                                                   "Freezeflame Purple Coins: Sling Star to Slide")
    world.get_region(regname.FREFLA5MOUNB).connect(world.get_region(regname.FREFLA5MIDDL),
                                                   "Freezeflame Purple Coins: Mountain Base Sling Star")
    world.get_region(regname.FREFLA5MOUNB).connect(world.get_region(regname.FREFLA5BACK1),
                                                   "Freezeflame Purple Coins: Ice Jump Sling Star")
    world.get_region(regname.FREFLA5MIDDL).connect(world.get_region(regname.FREFLA5BARBR),
                                                   "Freezeflame Purple Coins: Middle Ponds Sling Star")
    world.get_region(regname.FREFLA5BACK1).connect(world.get_region(regname.FREFLA5BACK2),
                                                   "Freezeflame Purple Coins: First Snowman Sling Star")
    world.get_region(regname.FREFLA5BACK2).connect(world.get_region(regname.FREFLA5BACK3),
                                                   "Freezeflame Purple Coins: Second Snowman Sling Star")

    world.get_region(regname.BEDROOM).connect(world.get_region(regname.DUSTY), "Dome 4 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Third Orbit"], 20)))
    world.get_region(regname.DUSTY).connect(world.get_region(regname.DUSTY1LANDI),
                                                    "Dusty Dune 1: Soaring through the Desert Winds")
    world.get_region(regname.DUSTY1LANDI).connect(world.get_region(regname.DUSTY1INPIP),
                                                    "Dusty Dune 1: Past Tornadoes Pipe")
    world.get_region(regname.DUSTY1INPIP).connect(world.get_region(regname.DUSTY1PIPEO),
                                                    "Dusty Dune 1: Sling to Pipe")
    world.get_region(regname.DUSTY1PIPEO).connect(world.get_region(regname.DUSTY1SANDT),
                                                    "Dusty Dune 1: Near Pipe Launch Star")
    world.get_region(regname.DUSTY1SANDT).connect(world.get_region(regname.DUSTY1SANTO),
                                                    "Dusty Dune 1: Sand Climb Halfway Sling Stars")
    world.get_region(regname.DUSTY).connect(world.get_region(regname.DUSTY2LANDI),
                                                    "Dusty Dune 2: Blasting through the Sand")
    world.get_region(regname.DUSTY2LANDI).connect(world.get_region(regname.DUSTY2WOODE),
                                                    "Dusty Dune 2: Landing Launch Star")
    world.get_region(regname.DUSTY2WOODE).connect(world.get_region(regname.DUSTY2SAND1),
                                                    "Dusty Dune 2: Wooden Ring Sling Stars")
    world.get_region(regname.DUSTY2WOODE).connect(world.get_region(regname.DUSTY7SANDY),
                                                    "Dusty Dune Green: Hungry Luma Launch Star")
    world.get_region(regname.DUSTY2SAND1).connect(world.get_region(regname.DUSTY2SAND2),
                                                    "Dusty Dune 2: Small Stream Sling Star")
    world.get_region(regname.DUSTY2SAND2).connect(world.get_region(regname.DUSTY2SAND3),
                                                    "Dusty Dune 2: Sand Ring Pull Stars")
    world.get_region(regname.DUSTY2SAND3).connect(world.get_region(regname.DUSTY2NOTES),
                                                    "Dusty Dune 2: Sand Sphere Green pipe")
    world.get_region(regname.DUSTY2NOTES).connect(world.get_region(regname.DUSTY2MAZEY),
                                                    "Dusty Dune 2: Note Room Green Pipe")
    world.get_region(regname.DUSTY2SAND3).connect(world.get_region(regname.DUSTY2MAZEY),
                                                    "Dusty Dune 2: Sand Sphere Launch Star")
    world.get_region(regname.DUSTY).connect(world.get_region(regname.DUSTY3LANDI),
                                                    "Dusty Dune 3: Sunbaked Sand Castle")
    world.get_region(regname.DUSTY3LANDI).connect(world.get_region(regname.DUSTY3POUN1),
                                                    "Dusty Dune 3: Landing Launch Star")
    world.get_region(regname.DUSTY3POUN1).connect(world.get_region(regname.DUSTY3SANDT),
                                                    "Dusty Dune 3: Landing Launch Star")
    world.get_region(regname.DUSTY3SANDT).connect(world.get_region(regname.DUSTY6BBILL),
                                                    "Dusty Dune Secret: Sand Tide Stump Launch Star")
    world.get_region(regname.DUSTY3SANDT).connect(world.get_region(regname.DUSTY3ROCKY),
                                                    "Dusty Dune 3: Sand Tide Thorns Launch Star")
    world.get_region(regname.DUSTY3ROCKY).connect(world.get_region(regname.DUSTY3OASIS),
                                                    "Dusty Dune 3: Rocky Sling Star")
    world.get_region(regname.DUSTY3OASIS).connect(world.get_region(regname.DUSTY3OASIS),
                                                    "Dusty Dune 3: Oasis Sling Star")
    world.get_region(regname.DUSTY3ROCKY).connect(world.get_region(regname.DUSTY3GLASO),
                                                    "Dusty Dune 3: Rocky Launch Star")
    world.get_region(regname.DUSTY3GLASO).connect(world.get_region(regname.DUSTY3GLASI),
                                                    "Dusty Dune 3: Glass Tower Pipe")
    world.get_region(regname.DUSTY).connect(world.get_region(regname.DUSTY4LANDI),
                                                    "Dusty Dune Comet: Sandblast Speed Run")
    world.get_region(regname.DUSTY4LANDI).connect(world.get_region(regname.DUSTY4WOODE),
                                                    "Dusty Dune Comet: Landing Launch Star")
    world.get_region(regname.DUSTY4WOODE).connect(world.get_region(regname.DUSTY4SAND1),
                                                    "Dusty Dune Comet: Wooden Ring Sling Stars")
    world.get_region(regname.DUSTY4SAND1).connect(world.get_region(regname.DUSTY4SAND2),
                                                    "Dusty Dune Comet: Small Stream Sling Star")
    world.get_region(regname.DUSTY4SAND2).connect(world.get_region(regname.DUSTY4SAND3),
                                                    "Dusty Dune Comet: Sand Ring Pull Stars")
    world.get_region(regname.DUSTY4SAND3).connect(world.get_region(regname.DUSTY4NOTES),
                                                    "Dusty Dune Comet: Sand Sphere Green pipe")
    world.get_region(regname.DUSTY4NOTES).connect(world.get_region(regname.DUSTY4MAZEY),
                                                    "Dusty Dune Comet: Note Room Green Pipe")
    world.get_region(regname.DUSTY4SAND3).connect(world.get_region(regname.DUSTY4MAZEY),
                                                    "Dusty Dune Comet: Sand Sphere Launch Star")
    world.get_region(regname.DUSTY).connect(world.get_region(regname.DUSTY5MAZEY),
                                                    "Dusty Dune Purple Coins: Purple Coins in the Desert")

    world.get_region(regname.BEDROOM).connect(world.get_region(regname.HONEYCLIMB), "Dome 4 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Fourth Orbit"], 21)))
    world.get_region(regname.HONEYCLIMB).connect(world.get_region(regname.HONEYCL1WALL1),
                                                    "Honeyclimb: Scaling the Sticky Wall")
    world.get_region(regname.HONEYCL1WALL1).connect(world.get_region(regname.HONEYCL1WALL2),
                                                    "Honeyclimb: First Wall Launch Star")
    world.get_region(regname.HONEYCL1WALL2).connect(world.get_region(regname.HONEYCL1WALL3),
                                                    "Honeyclimb: Second Wall Launch Star")

    world.get_region(regname.BEDROOM).connect(world.get_region(regname.BOWSER2), "Dome 4 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Fifth Orbit"], 22)))
    world.get_region(regname.BOWSER2).connect(world.get_region(regname.DARKMAT1CASTB),
                                                    "Dark Matter Plant: Darkness on the Horizon")
    world.get_region(regname.DARKMAT1CASTB).connect(world.get_region(regname.DARKMAT1GRAVI))
    world.get_region(regname.DARKMAT1GRAVI).connect(world.get_region(regname.DARKMAT1TOWER))
    world.get_region(regname.DARKMAT1TOWER).connect(world.get_region(regname.DARKMAT1BOSSA))

    # Dome 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.ENGINE), "Dome 5 Entry",
                    Has("Grand Star", 4))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.GOLDLEAF), "Dome 5 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["First Orbit"], 23)))
    world.get_region(regname.GOLDLEAF).connect(world.get_region(regname.GOLDLE1LANDI),
                                                    "Gold Leaf 1: Star Bunnies on the Hunt")
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1BIGTR))
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1FOUNC),
                                                   "Gold Leaf 1: Swing to Sling Star")
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1CLIFF),
                                                   "Gold Leaf 1: Beneath Planet Sling Star")
    world.get_region(regname.GOLDLE1CLIFF).connect(world.get_region(regname.GOLDLE1BOULD),
                                                   "Gold Leaf 1: Clifftop Green Pipe")
    world.get_region(regname.GOLDLE1BIGTR).connect(world.get_region(regname.GOLDLE1POUND))
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1SMLHI))
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1WATRP))
    world.get_region(regname.GOLDLE1LANDI).connect(world.get_region(regname.GOLDLE1WOODE),
                                                   "Gold Leaf 1: Pull to Launch Star")
    world.get_region(regname.GOLDLEAF).connect(world.get_region(regname.GOLDLE2LANDI),
                                                    "Gold Leaf 2: Cataquack to the Skies")
    world.get_region(regname.GOLDLE2LANDI).connect(world.get_region(regname.GOLDLE2BIGTR))
    world.get_region(regname.GOLDLE2POUND).connect(world.get_region(regname.GOLDLE2FOUNC))
    world.get_region(regname.GOLDLE2LANDI).connect(world.get_region(regname.GOLDLE2CLIFF),
                                                   "Gold Leaf 2: Beneath Planet Sling Star")
    world.get_region(regname.GOLDLE2CLIFF).connect(world.get_region(regname.GOLDLE2BOULD),
                                                   "Gold Leaf 2: Clifftop Green Pipe")
    world.get_region(regname.GOLDLE2BIGTR).connect(world.get_region(regname.GOLDLE2POUND))
    world.get_region(regname.GOLDLE2LANDI).connect(world.get_region(regname.GOLDLE2SMLHI))
    world.get_region(regname.GOLDLE2LANDI).connect(world.get_region(regname.GOLDLE2WATRP))
    world.get_region(regname.GOLDLE2FOUNC).connect(world.get_region(regname.GOLDLE2HONYP),
                                                   "Gold Leaf 2: Fountain Cliff Launch Star")
    world.get_region(regname.GOLDLE2HONYP).connect(world.get_region(regname.GOLDLE2QCUBE))
    world.get_region(regname.GOLDLE2QCUBE).connect(world.get_region(regname.GOLDLE2BIGMM))
    world.get_region(regname.GOLDLE2BIGMM).connect(world.get_region(regname.GOLDLE2BELLS),
                                                   "Gold Leaf 2: Big M-Block Launch Star")
    world.get_region(regname.GOLDLE2BELLS).connect(world.get_region(regname.GOLDLE2FLOWE))
    world.get_region(regname.GOLDLEAF).connect(world.get_region(regname.GOLDLE3LANDI),
                                                    "Gold Leaf 3: When It Rains, It Pours")
    world.get_region(regname.GOLDLE3LANDI).connect(world.get_region(regname.GOLDLE3POUND))
    world.get_region(regname.GOLDLE3LANDI).connect(world.get_region(regname.GOLDLE3FOUNC))
    world.get_region(regname.GOLDLE3LANDI).connect(world.get_region(regname.GOLDLE3CLIFF),
                                                   "Gold Leaf 3: Beneath Planet Sling Star")
    world.get_region(regname.GOLDLE3CLIFF).connect(world.get_region(regname.GOLDLE3BOULD),
                                                   "Gold Leaf 3: Clifftop Green Pipe")
    world.get_region(regname.GOLDLE3POUND).connect(world.get_region(regname.GOLDLE3BIGTR))
    world.get_region(regname.GOLDLE3LANDI).connect(world.get_region(regname.GOLDLE3SMLHI))
    world.get_region(regname.GOLDLE3LANDI).connect(world.get_region(regname.GOLDLE3WATRP))
    world.get_region(regname.GOLDLE3POUND).connect(world.get_region(regname.GOLDLE3FLOAT))
    world.get_region(regname.GOLDLE3FLOAT).connect(world.get_region(regname.GOLDLE3TOWER))
    world.get_region(regname.GOLDLE3TOWER).connect(world.get_region(regname.GOLDLE3CANNO))
    world.get_region(regname.GOLDLEAF).connect(world.get_region(regname.GOLDLE4LANDI),
                                                    "Gold Leaf Comet: Cosmic Mario Forest Race")
    world.get_region(regname.GOLDLE4LANDI).connect(world.get_region(regname.GOLDLE4POUND))
    world.get_region(regname.GOLDLE4LANDI).connect(world.get_region(regname.GOLDLE4FOUNC))
    world.get_region(regname.GOLDLE4POUND).connect(world.get_region(regname.GOLDLE4BIGTR))
    world.get_region(regname.GOLDLE4LANDI).connect(world.get_region(regname.GOLDLE4SMLHI))
    world.get_region(regname.GOLDLE4LANDI).connect(world.get_region(regname.GOLDLE4WATRP))
    world.get_region(regname.GOLDLE4POUND).connect(world.get_region(regname.GOLDLE4FLOAT))
    world.get_region(regname.GOLDLE4FLOAT).connect(world.get_region(regname.GOLDLE4TOWER))
    world.get_region(regname.GOLDLE4TOWER).connect(world.get_region(regname.GOLDLE4CANNO))
    world.get_region(regname.GOLDLEAF).connect(world.get_region(regname.GOLDLE5LANDI),
                                                    "Gold Leaf Purple Coins: Purple Coins in the Woods")
    world.get_region(regname.GOLDLE5LANDI).connect(world.get_region(regname.GOLDLE5POUND))
    world.get_region(regname.GOLDLE5LANDI).connect(world.get_region(regname.GOLDLE5FOUNC))
    world.get_region(regname.GOLDLE5POUND).connect(world.get_region(regname.GOLDLE5BIGTR))
    world.get_region(regname.GOLDLE5LANDI).connect(world.get_region(regname.GOLDLE5SMLHI))
    world.get_region(regname.GOLDLE5LANDI).connect(world.get_region(regname.GOLDLE5WATRP))
    world.get_region(regname.GOLDLE5POUND).connect(world.get_region(regname.GOLDLE5FLOAT))
    world.get_region(regname.GOLDLE5FLOAT).connect(world.get_region(regname.GOLDLE5TOWER))
    world.get_region(regname.GOLDLE5TOWER).connect(world.get_region(regname.GOLDLE5CANNO))

    world.get_region(regname.ENGINE).connect(world.get_region(regname.SEASLIDE), "Dome 5 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Second Orbit"], 24)))
    world.get_region(regname.SEASLIDE).connect(world.get_region(regname.SEASLI1LANDI),
                                                    "Sea Slide 1: Going after Guppy")
    world.get_region(regname.SEASLI1LANDI).connect(world.get_region(regname.SEASLI1SLIDE))
    world.get_region(regname.SEASLI1SLIDE).connect(world.get_region(regname.SEASLI1TOADS))
    world.get_region(regname.SEASLIDE).connect(world.get_region(regname.SEASLI2LANDI),
                                                    "Sea Slide 2: Faster Than a Speeding Pengiun")
    world.get_region(regname.SEASLI2LANDI).connect(world.get_region(regname.SEASLI2SLIDE))
    world.get_region(regname.SEASLIDE).connect(world.get_region(regname.SEASLI3LANDI),
                                                    "Sea Slide 3: The Silver Stars of Sea Slide")
    world.get_region(regname.SEASLI3LANDI).connect(world.get_region(regname.SEASLI3SLIDE))
    world.get_region(regname.SEASLI3SLIDE).connect(world.get_region(regname.SEASLI3TOADS))
    world.get_region(regname.SEASLI3TOADS).connect(world.get_region(regname.SEASLI3SLIDE),
                                                   "Sea Slide 3: Toadship Sling Star")
    world.get_region(regname.SEASLI3SLIDE).connect(world.get_region(regname.SEASLI3BIGTR),
                                                   "Sea Slide 3: Big Tree Sling Star")
    world.get_region(regname.SEASLI3SLIDE).connect(world.get_region(regname.SEASLI3CENTE))
    world.get_region(regname.SEASLI3CENTE).connect(world.get_region(regname.SEASLI3SLIDE),
                                                   "Sea Slide 3: Central Launch Star")
    world.get_region(regname.SEASLI3SLIDE).connect(world.get_region(regname.SEASLI6HURRY),
                                                   "Sea Slide Secret: Hungry Luma Launch Star")
    world.get_region(regname.SEASLIDE).connect(world.get_region(regname.SEASLI4LANDI),
                                                    "Sea Slide Comet: Underwater Cosmic Mario Race")
    world.get_region(regname.SEASLI4LANDI).connect(world.get_region(regname.SEASLI4SLIDE))
    world.get_region(regname.SEASLIDE).connect(world.get_region(regname.SEASLI5LANDI),
                                                    "Sea Slide Purple Coins: Purple Coins by the Seaside")
    world.get_region(regname.SEASLI5LANDI).connect(world.get_region(regname.SEASLI5SLIDE))
    world.get_region(regname.SEASLI5SLIDE).connect(world.get_region(regname.SEASLI5BIGTR))

    world.get_region(regname.ENGINE).connect(world.get_region(regname.TOYTIME), "Dome 5 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Third Orbit"], 25)))
    world.get_region(regname.TOYTIME).connect(world.get_region(regname.TOYTIME1LANDI),
                                                    "Toy Time 1: Heavy Metal Mecha-Bowser")
    world.get_region(regname.TOYTIME1LANDI).connect(world.get_region(regname.TOYTIME1GRAVI),
                                                    "Toy Time 1: Train Launch Star")
    world.get_region(regname.TOYTIME1LANDI).connect(world.get_region(regname.TOYTIME1GRAVI),
                                                    "Toy Time 1: Train Launch Star")
    world.get_region(regname.TOYTIME1GRAVI).connect(world.get_region(regname.TOYTIME1CONVE),
                                                    "Toy Time 1: Covered Launch Star")
    world.get_region(regname.TOYTIME1CONVE).connect(world.get_region(regname.TOYTIME1CYLIN),
                                                    "Toy Time 1: Conveyor Blocks Green Pipe")
    world.get_region(regname.TOYTIME1CONVE).connect(world.get_region(regname.TOYTIME1PLATE),
                                                    "Toy Time 1: Conveyors Launch Star")
    world.get_region(regname.TOYTIME1PLATE).connect(world.get_region(regname.TOYTIME1ROBOB),
                                                    "Toy Time 1: Salty Launch Star")
    world.get_region(regname.TOYTIME1ROBOB).connect(world.get_region(regname.TOYTIME1ROBOL))
    world.get_region(regname.TOYTIME1ROBOL).connect(world.get_region(regname.TOYTIME1ROBOD),
                                                    "Toy Time 1: Left Leg Sling Star")
    world.get_region(regname.TOYTIME1ROBOD).connect(world.get_region(regname.TOYTIME1ROBOA),
                                                    "Toy Time 1: Under Cover Pipe")
    world.get_region(regname.TOYTIME1ROBOA).connect(world.get_region(regname.TOYTIME1ROBOH),
                                                    "Toy Time 1: Right Shoulder Launch Star")
    world.get_region(regname.TOYTIME).connect(world.get_region(regname.TOYTIME2LANDI),
                                                    "Toy Time 2: Mario Meets Mario")
    world.get_region(regname.TOYTIME2LANDI).connect(world.get_region(regname.TOYTIME2SCREW),
                                                    "Toy Time 2: Train Launch Star")
    world.get_region(regname.TOYTIME2SCREW).connect(world.get_region(regname.TOYTIME2MARIO),
                                                    "Toy Time 2: Screw Tip Launch Star")
    world.get_region(regname.TOYTIME2SCREW).connect(world.get_region(regname.TOYTIME6CHAIN),
                                                    "Toy Time Secret: Hungry Luma Launch Star")
    world.get_region(regname.TOYTIME).connect(world.get_region(regname.TOYTIME3LANDI),
                                                    "Toy Time 3: Bouncing Down Cake Lane")
    world.get_region(regname.TOYTIME3LANDI).connect(world.get_region(regname.TOYTIME3SWEET),
                                                    "Toy Time 3: Train Launch Star")
    world.get_region(regname.TOYTIME3SWEET).connect(world.get_region(regname.TOYTIME3CREAM),
                                                    "Toy Time 3: Spinning Cake Sling Star")
    world.get_region(regname.TOYTIME3CREAM).connect(world.get_region(regname.TOYTIME3CAKES),
                                                    "Toy Time 3: Cannon Launch Star")
    world.get_region(regname.TOYTIME3CAKES).connect(world.get_region(regname.TOYTIME3PIPES),
                                                    "Toy Time 3: Cake Green Pipe")
    world.get_region(regname.TOYTIME3CAKES).connect(world.get_region(regname.TOYTIME3CANNO),
                                                    "Toy Time 3: Cake Candles Launch Star")
    world.get_region(regname.TOYTIME).connect(world.get_region(regname.TOYTIME4CHAIN),
                                                    "Toy Time Comet: Fast Foes of Toy Time")
    world.get_region(regname.TOYTIME).connect(world.get_region(regname.TOYTIME5LUIGI),
                                                    "Toy Time Purple Coins: Luigi's Purple Coins")

    world.get_region(regname.ENGINE).connect(world.get_region(regname.BONEFIN), "Dome 5 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Fourth Orbit"], 26)))
    world.get_region(regname.BONEFIN).connect(world.get_region(regname.BONEFINTOAD),
                                                    "Bonefin: Kingfin's Fearsome Waters")
    world.get_region(regname.BONEFINTOAD).connect(world.get_region(regname.BONEFINWATR),
                                                    "Bonefin: Green Toadship Launch Star")

    world.get_region(regname.ENGINE).connect(world.get_region(regname.BOWJR3), "Dome 5 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Fifth Orbit"], 27)))
    world.get_region(regname.BOWJR3).connect(world.get_region(regname.LAVREALANDI),
                                                    "Lava Reactor: King Kaliente's Spicy Return")
    world.get_region(regname.LAVREALANDI).connect(world.get_region(regname.LAVREALAVA1),
                                                    "Lava Reactor: Caged Launch Star")
    world.get_region(regname.LAVREALAVA1).connect(world.get_region(regname.LAVREALAVA2),
                                                    "Lava Reactor: Sinking Platforms Launch Star")
    # Dome 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.GARDEN), "Dome 6 Entry",
                    Has("Grand Star", 5))
    world.get_region(regname.GARDEN).connect(world.get_region(regname.DEEPDARK), "Dome 6 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["First Orbit"], 28)))
    world.get_region(regname.DEEPDARK).connect(world.get_region(regname.DEEPDA1BEACH),
                                                    "Deep Dark 1: The Underground Ghost Ship")
    world.get_region(regname.DEEPDA1BEACH).connect(world.get_region(regname.DEEPDA1BWATR))
    world.get_region(regname.DEEPDA1BEACH).connect(world.get_region(regname.DEEPDA1WOODE))
    world.get_region(regname.DEEPDA1WOODE).connect(world.get_region(regname.DEEPDA1BEACH),
                                                   "Deep Dark 1: Wooden Planet Sling Star")
    world.get_region(regname.DEEPDA1BEACH).connect(world.get_region(regname.DEEPDA1FHOME))
    world.get_region(regname.DEEPDA1BEACH).connect(world.get_region(regname.DEEPDA1GATES))
    world.get_region(regname.DEEPDA1GATES).connect(world.get_region(regname.DEEPDA1WATER))
    world.get_region(regname.DEEPDA1WATER).connect(world.get_region(regname.DEEPDA6BOOBX),
                                                   "Deep Dark 1: Ship Hidden Launch Star")
    world.get_region(regname.DEEPDA1WATER).connect(world.get_region(regname.DEEPDA1SHIPC))
    world.get_region(regname.DEEPDA1SHIPC).connect(world.get_region(regname.DEEPDA1SMAST))
    world.get_region(regname.DEEPDARK).connect(world.get_region(regname.DEEPDA2BEACH),
                                                    "Deep Dark 2: Bubble Blastoff")
    world.get_region(regname.DEEPDA2BEACH).connect(world.get_region(regname.DEEPDA2BWATR))
    world.get_region(regname.DEEPDA2BEACH).connect(world.get_region(regname.DEEPDA2WOODE))
    world.get_region(regname.DEEPDA2WOODE).connect(world.get_region(regname.DEEPDA2BEACH),
                                                   "Deep Dark 2: Wooden Planet Sling Star")
    world.get_region(regname.DEEPDA2BEACH).connect(world.get_region(regname.DEEPDA2FHOME))
    world.get_region(regname.DEEPDA2BEACH).connect(world.get_region(regname.DEEPDA2WATER))
    world.get_region(regname.DEEPDA2WATER).connect(world.get_region(regname.DEEPDA6BOOBX),
                                                   "Deep Dark 2: Ship Hidden Launch Star")
    world.get_region(regname.DEEPDA2WATER).connect(world.get_region(regname.DEEPDA2CLIFF))
    world.get_region(regname.DEEPDA2CLIFF).connect(world.get_region(regname.DEEPDA2CLIFP),
                                                   "Deep Dark 2: Clifftop Green Pipe")
    world.get_region(regname.DEEPDA2CLIFF).connect(world.get_region(regname.DEEPDA2CHEEP))
    world.get_region(regname.DEEPDA2CHEEP).connect(world.get_region(regname.DEEPDA2MELON))
    world.get_region(regname.DEEPDARK).connect(world.get_region(regname.DEEPDA3BEACH),
                                                    "Deep Dark 3: Guppy and the Underground Lake")
    world.get_region(regname.DEEPDA3BEACH).connect(world.get_region(regname.DEEPDA3BWATR))
    world.get_region(regname.DEEPDA3BEACH).connect(world.get_region(regname.DEEPDA3WATER))
    world.get_region(regname.DEEPDA3WATER).connect(world.get_region(regname.DEEPDA6BOOBX),
                                                   "Deep Dark 3: Ship Hidden Launch Star")
    world.get_region(regname.DEEPDARK).connect(world.get_region(regname.DEEPDA4SHIPC),
                                                    "Deep Dark Comet: Ghost Ship Daredevil Rune")
    world.get_region(regname.DEEPDA4SHIPC).connect(world.get_region(regname.DEEPDA4SHIPW))
    world.get_region(regname.DEEPDA4SHIPC).connect(world.get_region(regname.DEEPDA4SMAST))
    world.get_region(regname.DEEPDARK).connect(world.get_region(regname.DEEPDA5SHIPC),
                                                    "Deep Dark Purple Coins: Plunder the Purple Coins")
    world.get_region(regname.DEEPDA5SHIPC).connect(world.get_region(regname.DEEPDA5SHIPW))
    world.get_region(regname.DEEPDA5SHIPC).connect(world.get_region(regname.DEEPDA5SMAST))

    world.get_region(regname.GARDEN).connect(world.get_region(regname.DREADNOUGHT), "Dome 6 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["Second Orbit"], 29)))
    world.get_region(regname.DREADNOUGHT).connect(world.get_region(regname.DREADN1HOURG),
                                                    "Dreadnought 1: Infiltrating the Dreadnought")
    world.get_region(regname.DREADN1HOURG).connect(world.get_region(regname.DREADN1ENTRY),
                                                    "Dreadnought 1: Hourglass Launch Star")
    world.get_region(regname.DREADN1ENTRY).connect(world.get_region(regname.DREADN1INSD1),
                                                    "Dreadnought 1: Dreadnought Entry Green Pipe")
    world.get_region(regname.DREADN1INSD1).connect(world.get_region(regname.DREADN1TOPMN),
                                                    "Dreadnought 1: Inside Dreadnought Green Pipe")
    world.get_region(regname.DREADN1TOPMN).connect(world.get_region(regname.DREADN1METAL),
                                                    "Dreadnought 1: Climb Launch Star")
    world.get_region(regname.DREADN1METAL).connect(world.get_region(regname.DREADN1PLATF),
                                                    "Dreadnought 1: Metal Cube Sling Star")
    world.get_region(regname.DREADNOUGHT).connect(world.get_region(regname.DREADN2CHIMP),
                                                    "Dreadnought 2: Dreadnought's Colossal Cannons")
    world.get_region(regname.DREADN2CHIMP).connect(world.get_region(regname.DREADN2AUTOS),
                                                    "Dreadnought 2: Bridge Launch Star")
    world.get_region(regname.DREADNOUGHT).connect(world.get_region(regname.DREADN3LANDI),
                                                    "Dreadnought 3: Revenge of the Topman Tribe")
    world.get_region(regname.DREADN3LANDI).connect(world.get_region(regname.DREADN3TOPPL),
                                                    "Dreadnought 3: Landing Sling Star")
    world.get_region(regname.DREADN3TOPPL).connect(world.get_region(regname.DREADN3METAL),
                                                    "Dreadnought 3: Caged Luma Sling Star")
    world.get_region(regname.DREADN3METAL).connect(world.get_region(regname.DREADN3PULLP),
                                                    "Dreadnought 3: Pull to Launch Star")
    world.get_region(regname.DREADN3PULLP).connect(world.get_region(regname.DREADN3MINES),
                                                    "Dreadnought 3: Cannon Pull Launch Star")
    world.get_region(regname.DREADN3MINES).connect(world.get_region(regname.DREADN3BOSSA),
                                                    "Dreadnought 3: Minefield Launch Star")
    world.get_region(regname.DREADNOUGHT).connect(world.get_region(regname.DREADN4LANDI),
                                                    "Dreadnought Comet: Topman Tribe Speed Run")
    world.get_region(regname.DREADN4LANDI).connect(world.get_region(regname.DREADN4TOPPL),
                                                    "Dreadnought Comet: Landing Sling Star")
    world.get_region(regname.DREADN4TOPPL).connect(world.get_region(regname.DREADN4METAL),
                                                    "Dreadnought Comet: Caged Luma Sling Star")
    world.get_region(regname.DREADN4METAL).connect(world.get_region(regname.DREADN4PULLP),
                                                    "Dreadnought Comet: Pull to Launch Star")
    world.get_region(regname.DREADN4PULLP).connect(world.get_region(regname.DREADN4MINES),
                                                    "Dreadnought Comet: Cannon Pull Launch Star")
    world.get_region(regname.DREADN4MINES).connect(world.get_region(regname.DREADN4BOSSA),
                                                    "Dreadnought Comet: Minefield Launch Star")
    world.get_region(regname.DREADNOUGHT).connect(world.get_region(regname.DREADN5AUTOS),
                                                    "Dreadnought Purple Coins: Battlestation's Purple Coins")
    world.get_region(regname.DREADN5AUTOS).connect(world.get_region(regname.DREADN5STARS),
                                                    "Dreadnought Purple Coins: Autoscroller Launch Star")

    world.get_region(regname.GARDEN).connect(world.get_region(regname.MATTER), "Dome 6 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["Third Orbit"], 30)))


    world.get_region(regname.GARDEN).connect(world.get_region(regname.MELTY), "Dome 6 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["Fourth Orbit"], 31)))


    #Remaining Ship Connections
    world.get_region(regname.SHIP).connect(world.get_region(regname.LIBRARY), "Library Entrance")
    world.get_region(regname.SHIP).connect(world.get_region(regname.COTU), "Center Of the Universe Entry",
                    Has("Grand Star", 5) and HasGroup("Power Stars", count=world.options.stars_to_finish.value))
    world.get_region(regname.COTU).connect(world.get_region(regname.BOWSER3), "Galaxy's Center")
    world.get_region(regname.BOWSER3).connect(world.get_region(regname.GALREAC1LANDI),
                                              "Galaxy Reactor: The Fate of the Universe")
    world.get_region(regname.GALREAC1LANDI).connect(world.get_region(regname.GALREAC1WALLS))
    world.get_region(regname.GALREAC1WALLS).connect(world.get_region(regname.GALREAC1SMSUN))
    world.get_region(regname.GALREAC1SMSUN).connect(world.get_region(regname.GALREAC1BLSUN))
    world.get_region(regname.GALREAC1BLSUN).connect(world.get_region(regname.GALREAC1SANDY))
    world.get_region(regname.GALREAC1SANDY).connect(world.get_region(regname.GALREAC1GRAVI))
    world.get_region(regname.GALREAC1GRAVI).connect(world.get_region(regname.GALREAC1LAVAT))
    world.get_region(regname.GALREAC1LAVAT).connect(world.get_region(regname.GALREAC1STAIR),
                                                    "Galaxy Reactor: Lava Launch Star")
    world.get_region(regname.GALREAC1STAIR).connect(world.get_region(regname.GALREAC1BOSS))
    world.get_region(regname.SHIP).connect(world.get_region(regname.SWEETSWEET), "Sweet Sweet Hungry Luma")
    world.get_region(regname.SWEETSWEET).connect(world.get_region(regname.SWEETSW1SWEET),
                                                 "Sweet Sweet: Rocky Road")
    world.get_region(regname.SHIP).connect(world.get_region(regname.SLINGPOD), "Sling Pod Hungry Luma",
                    Has("Grand Star"))
    world.get_region(regname.SLINGPOD).connect(world.get_region(regname.SLINGPO1WEBPU),
                                               "Sling Pod: A Very Sticky Situation")
    world.get_region(regname.SHIP).connect(world.get_region(regname.DRIPDROP), "Drip Drop Hungry Luma",
                    Has("Grand Star", 2))
    world.get_region(regname.DRIPDROP).connect(world.get_region(regname.DRIPDRO1WATER),
                                               "Drip Drop: Giant Eel Outbreak")
    world.get_region(regname.SHIP).connect(world.get_region(regname.BIGMOUTH), "Bigmouth Hungry Luma",
                    Has("Grand Star", 3))
    world.get_region(regname.BIGMOUTH).connect(world.get_region(regname.BIGMOUT1ENTRY),
                                               "Bigmouth: Bigmouth's Gold Bait")
    world.get_region(regname.BIGMOUT1ENTRY).connect(world.get_region(regname.BIGMOUT1THROA))
    world.get_region(regname.BIGMOUT1THROA).connect(world.get_region(regname.BIGMOUT1LOWER))
    world.get_region(regname.BIGMOUT1LOWER).connect(world.get_region(regname.BIGMOUT1UPPER),
                                                    "Bigmouth: Stomach Sling Star")
    world.get_region(regname.SHIP).connect(world.get_region(regname.SANDSPIRAL), "Sand Spiral Hungry Luma",
                    Has("Grand Star", 4))
    world.get_region(regname.SANDSPIRAL).connect(world.get_region(regname.SANDSPI1SHIPB),
                                                 "Sand Spiral: Choosing a Favorite Snack")
    world.get_region(regname.SANDSPI1SHIPB).connect(world.get_region(regname.SANDSPI1SANDT),
                                                 "Sand Spiral: Ship Bow Sling Star")
    world.get_region(regname.SANDSPI1SANDT).connect(world.get_region(regname.SANDSPI1SPIRA),
                                                 "Sand Spiral: Tunnel Sling Star")
    world.get_region(regname.SHIP).connect(world.get_region(regname.SNOWCAP), "Snow Cap Hungry Luma",
                    Has("Grand Star", 5))
    world.get_region(regname.SNOWCAP).connect(world.get_region(regname.SNOWCAP1GLASS),
                                                 "Snow Cap: Star Bunnies in the Snow")
    world.get_region(regname.SNOWCAP1GLASS).connect(world.get_region(regname.SNOWCAP1SNOWY),
                                                 "Snow Cap: Glass Sphere Sling Star")
    world.get_region(regname.SHIP).connect(world.get_region(regname.GATEWAY), "Gateway Dome",
                    Has("Grand Star", 5))
    world.get_region(regname.GATEWAY).connect(world.get_region(regname.GATEWAY1HOMEP),
                                              "Gateway: Grand Star Rescue")
    world.get_region(regname.GATEWAY).connect(world.get_region(regname.GATEWAY2HOMEP),
                                              "Gateway Comet: Gateway's Purple Coins")
    world.get_region(regname.GATEWAY1HOMEP).connect(world.get_region(regname.GATEWAY1HOLEY),
                                                    "Gateway: Home Planet Launch Star")
    world.get_region(regname.GATEWAY1HOLEY).connect(world.get_region(regname.GATEWAY1SMLTU),
                                                    "Gateway: Holey Planet Launch Star")
    world.get_region(regname.GATEWAY1SMLTU).connect(world.get_region(regname.GATEWAY1LRGTU),
                                                    "Gateway: Small Tuning Planet Launch Star")
    world.get_region(regname.GATEWAY1LRGTU).connect(world.get_region(regname.GATEWAY1LRGTI),
                                                    "Gateway: Large Tuning Planet Pipe")
    world.get_region(regname.GATEWAY).connect(world.get_region(regname.GATEWAY2HOMEP),
                                              "Gateway Comet: Gateway's Purple Coins")
    world.get_region(regname.SHIP).connect(world.get_region(regname.BOOBONE), "Boo's Boneyard Hungry Luma",
                    Has("Grand Star", 5))
    world.get_region(regname.BOOBONE).connect(world.get_region(regname.BOOBONE1SKULL),
                                                 "Boo's Boneyard: Racing the Spooky Speedster")
    world.get_region(regname.BOOBONE1SKULL).connect(world.get_region(regname.BOOBONE1PIT),
                                                 "Boo's Boneyard: Skull Orange Pipe")
    world.get_region(regname.SHIP).connect(world.get_region(regname.TRIALS), "Planet of Trials Launch Star",
                    Has("Green Star"))
    world.get_region(regname.TRIALS).connect(world.get_region(regname.ROLLINGGIZ), "Rolling Gizmo Launch Star")
    world.get_region(regname.ROLLINGGIZ).connect(world.get_region(regname.ROLLGIZ1LANDI),
                                                 "Rolling Gizmo: Gizmos, Gears, and Gadgets")
    world.get_region(regname.ROLLGIZ1LANDI).connect(world.get_region(regname.ROLLGIZ1MAINA),
                                                 "Rolling Gizmo: Landing Ball Launcher")
    world.get_region(regname.TRIALS).connect(world.get_region(regname.LOOPDEESWOOP), "Loopdeeswoop Launch Star")
    world.get_region(regname.LOOPDEESWOOP).connect(world.get_region(regname.LOOPSWO1LANDI),
                                                   "Loopdeeswoop: The Galaxy's Greatest Wave")
    world.get_region(regname.LOOPSWO1LANDI).connect(world.get_region(regname.LOOPSWO1TERR1),
                                                    "Loopdeeswoop: Landing Sling Star")
    world.get_region(regname.LOOPSWO1TERR1).connect(world.get_region(regname.LOOPSWO1TERR2),
                                                    "Loopdeeswoop: First Terrace Sling Star")
    world.get_region(regname.LOOPSWO1TERR2).connect(world.get_region(regname.LOOPSWO1LANDI),
                                                    "Loopdeeswoop: Second Terrace Sling Star")
    world.get_region(regname.LOOPSWO1LANDI).connect(world.get_region(regname.LOOPSWO1SWOOP),
                                                    "Loopdeeswoop: Surfing Course")
    world.get_region(regname.TRIALS).connect(world.get_region(regname.BUBBLEBLAST), "Bubble Blast Launch Star")
    world.get_region(regname.BUBBLEBLAST).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: The Electric Labyrinth")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LNORTH),
                                                  "Bubble Blast: Star Platform North Pipe")
    world.get_region(regname.BUBBLAS1LNORTH).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: North Sling Star")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LNORTW),
                                                  "Bubble Blast: Star Platform Northwest Pipe")
    world.get_region(regname.BUBBLAS1LNORTW).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: Northwest Sling Star")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LNORTE),
                                                  "Bubble Blast: Star Platform Northeast Pipe")
    world.get_region(regname.BUBBLAS1LNORTE).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: Northeast Sling Star")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LSOUTE),
                                                  "Bubble Blast: Star Platform Southeast Pipe")
    world.get_region(regname.BUBBLAS1LSOUTE).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: Southeast Sling Star")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LSOUTW),
                                                  "Bubble Blast: Star Platform Southwest Pipe")
    world.get_region(regname.BUBBLAS1LSOUTW).connect(world.get_region(regname.BUBBLAS1LSTARP),
                                                  "Bubble Blast: Southwest Sling Star")
    world.get_region(regname.BUBBLAS1LSTARP).connect(world.get_region(regname.BUBBLAS1LLONGF),
                                                  "Bubble Blast: Star Platform Launch Star")
    # world.get_region(regname.TRIALS).connect(world.get_region(regname.FINALE), "Grand Finale Launch Star",
    #                  HasGroup("Power Star", 120))
    # world.get_region(regname.FINALE).connect(world.get_region(regname.GRANDFINALE), "Grand Finale: The Star Festival")
    world.set_completion_rule(Has("Peach"))

def rules_from_er_placements(world: "SMGWorld"):
    available_locations: int = 4
    dome_orbits: list[str] = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    for dome_num in [1, 2, 3, 4, 5, 6]:
        dome_galaxy_dict: dict = dict(sorted(dict([(d_key, d_val) for d_key, d_val in world.galaxy_counts.items()
                                                   if f"D{dome_num}" in d_key]).items(), key=lambda item: item[1]))
        for galaxy, star_count in dome_galaxy_dict.items():
            gal_num: int = int(galaxy[3:])
            orbit_name:str = dome_orbits[(gal_num-1)]

            galaxy_entr: Entrance = world.get_entrance(f"Dome {dome_num} {orbit_name} Galaxy")
            galaxy_type: str = region_list[galaxy_entr.connected_region.name].type

            if star_count <= available_locations:
                world.set_rule(galaxy_entr, HasGroup("Power Stars", count=star_count))
            else:
                world.set_rule(galaxy_entr, HasGroup("Power Stars", count=available_locations))
                world.galaxy_counts[galaxy] = available_locations

            available_locations += 4 if galaxy_type == "Major" else 1

    for galaxy_slot in all_galaxy_slots:
        world.shuffled_levels[world.get_entrance(galaxy_slot).name] = world.get_entrance(galaxy_slot).connected_region.name


    # # special stages logic Left here for reference later on default values
    # add_rule(world.get_location("LDL: Surfing 101"), Has("Power Star", player, 5))
    # add_rule(world.get_location("FS: Painting the Planet Yellow"), Has("Power Star", player, 7))
    # add_rule(world.get_location("RG: Rolling in the Clouds"), Has("Power Star", player, 11) and state.has("Progressive Grand Star"))
    # add_rule(world.get_location("HS: Shrinking Satellite"), lambda state: state.has ("Power Star", player, 18) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BUB: Through the Poison Swamp"), lambda state: state.has ("Power Star", player, 19) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BB: The Secret of Buoy Base"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BB: The Floating Fortress"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BF: Kingfin's Fearsome Waters"), lambda state: state.has("Power Star", player, 55) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("MS: Watch Your Step"), lambda state: state.has("Power Star", player, 50) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("DDR: Giant Eel Breakout"), lambda state: state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("RGT: Gizmos, Gears, and Gadgets"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("LDT: The Galaxy's Greatest Wave"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("BBT: The Electric Labyrinth"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("SS: Rocky Road"), lambda state: state.has("Power Stars", player, 7))
    # add_rule(world.get_location("SP: A Very Sticky Situation"), lambda state: state.has("Progressive Grand Star", player) and state.has("Power Stars", player, 9))
    # add_rule(world.get_location("BM: Bigmouth's Gold Bait"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Stars", player, 29))
    # add_rule(world.get_location("Sandy Spiral: Choosing a Favorite Snack"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Stars", player, 36) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("Bone's Boneyard: Racing the Spooky Speedster"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("SC: Star Bunnies in the Snow"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Stars", player, 52))
    # # comet logic
    # add_rule(world.get_location("GE: Dino Piranha Speed Run"), lambda state: state.has("Power Stars", player, 13))
    # add_rule(world.get_location("HH: Honeyhive Cosmic Mario Race"), lambda state: state.has("Power Stars", player, 13))
    # add_rule(world.get_location("SJ: Pull Star Path Speed Run"), lambda state: state.has("Power Stars", player, 13))
    # add_rule(world.get_location("BR: Topmanic's Dardevil Run"), lambda state: state.has("Power Stars", player, 13))
    # add_rule(world.get_location("BB: Fast Foes on the Cyclone Stone"), lambda state: state.has("Power Stars", player, 13))
    # # boss stage logic
    # add_rule(world.get_location("BJ: Megaleg's Moon"), lambda state: state.has("Power Stars", player, 8))
    # add_rule(world.get_location("B: The Firery Stronghold"), lambda state: state.has("Power Stars", player, 15) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BJ: Sinking the Airships"), lambda state: state.has("Power Stars", player, 23) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BJ: King Kaliente's Spicy Return"), lambda state: state.has("Power Stars", player, 45) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B:  Darkness on the Horizon"), lambda state: state.has("Power Stars", player, 33) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B: Bowser's Galaxy Reactor"), lambda state: state.has("Power Stars", player, world.options.stars_to_finish.value) and state.has("Progressive Grand Star", player, 2))
    #
    #
    # # purple coin star logic
    # if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
    #     add_rule(world.get_location("DN: Battlestation's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("MM: Red-Hot Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("TT: Luigi's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DD: Plunder the Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GL: Purple Coins in the Woods"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("FF: Purple Coins on the Summit"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SS: Purple Coins by the Seaside"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Purple Coins on the Puzzle Cube"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("G: Purple Coins in the Bone Pen"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DDune: Purple Coin in the Desert"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("BR: Purple Coins on the Battlerock"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GE: Purple Coin Omelet"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("HH: The Honeyhive's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SJ: Purple Coin Spacewalk"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Peach", player))
    # elif world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_main_game_only:
    #       add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Grand Star Engine", player))
    # else:
    #     return


