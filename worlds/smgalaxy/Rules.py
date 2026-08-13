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
    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BUBBLEBREEZE), "Dome 3 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Second Orbit"], 14)))
    world.get_region(regname.KITCHEN).connect(world.get_region(regname.GHOSTLY), "Dome 3 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Third Orbit"], 15)))
    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BUOY), "Dome 3 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Fourth Orbit"], 16)))
    world.get_region(regname.KITCHEN).connect(world.get_region(regname.BOWJR2), "Dome 3 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_three_counts["Fifth Orbit"], 17)))
    # Dome 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.BEDROOM), "Dome 4 Entry",
                    Has("Grand Star", 3))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.GUSTY), "Dome 4 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["First Orbit"], 18)))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.FREEZEFLAME), "Dome 4 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Second Orbit"], 19)))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.DUSTY), "Dome 4 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Third Orbit"], 20)))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.HONEYCLIMB), "Dome 4 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Fourth Orbit"], 21)))
    world.get_region(regname.BEDROOM).connect(world.get_region(regname.BOWSER2), "Dome 4 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_four_counts["Fifth Orbit"], 22)))
    # Dome 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.ENGINE), "Dome 5 Entry",
                    Has("Grand Star", 4))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.GOLDLEAF), "Dome 5 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["First Orbit"], 23)))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.SEASLIDE), "Dome 5 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Second Orbit"], 24)))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.TOYTIME), "Dome 5 Third Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Third Orbit"], 25)))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.BONEFIN), "Dome 5 Fourth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Fourth Orbit"], 26)))
    world.get_region(regname.ENGINE).connect(world.get_region(regname.BOWJR3), "Dome 5 Fifth Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_five_counts["Fifth Orbit"], 27)))
    # Dome 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.GARDEN), "Dome 6 Entry",
                    Has("Grand Star", 5))
    world.get_region(regname.GARDEN).connect(world.get_region(regname.DEEPDARK), "Dome 6 First Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["First Orbit"], 28)))
    world.get_region(regname.GARDEN).connect(world.get_region(regname.DREADNOUGHT), "Dome 6 Second Orbit Galaxy",
                    HasGroup("Power Stars", count=min(world.options.dome_six_counts["Second Orbit"], 29)))
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


