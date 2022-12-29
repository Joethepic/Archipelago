import imp
import typing
from .Options import EnablePurpleCoinStars, galaxy_options
from BaseClasses import Region, Location, RegionType, Entrance, MultiWorld
from .locations import SMGLocation, location_table, locHH_table, locGE_table, \
                                                   locSJ_table, locBR_table, locBB_table, \
                                                   locGG_table, locFF_table, locDD_table, locDDune_table, \
                                                   locGL_table, locSS_table, locTT_table, \
                                                   locDN_table, locMM_table, \
                                                   locspecialstages_table

def create_regions(world: MultiWorld, player: int, self: int):
    #defines the commet obserbatory
    regspecialstages = Region("Menu", RegionType.Generic, "Ship", player, world)
    create_default_locs(regspecialstages, locspecialstages_table, player)
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_main_game_only:
       regspecialstages.locations.append(SMGLocation(player, "GG: Gateway's Purple coins", location_table["GG: Gateway's Purple coins"], regspecialstages))
    world.regions.append(regspecialstages)    
    # defines the good egg galaxy region
    regGE = Region("Menu", RegionType.Generic, "Good Egg", player, world)
    locGE_names = [name for name, id in locGE_table.items()]
    regGE.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGE) for loc_name in locGE_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGE.locations.append(SMGLocation(player, "GE: Purple Coin Omelet", location_table["GE: Purple Coin Omelet"], regGE))
    world.regions.append(regGE)    
    # defines the honeyhive galaxey region
    regHH = Region("Menu", RegionType.Generic, "Honeyhive", player, world)
    locHH_names = [name for name, id in locHH_table.items()]
    regHH.locations += [SMGLocation(player, loc_name, location_table[loc_name], regHH) for loc_name in locHH_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regHH.locations.append(SMGLocation(player, "HH: The Honeyhive's Purple Coins", location_table["HH: The Honeyhive's Purple Coins"], regHH))
    world.regions.append(regHH)    
    # defines the Space Junk galaxy region
    regSJ = Region("Menu", RegionType.Generic, "Space Junk", player, world)
    locSJ_names = [name for name, id in locSJ_table.items()]
    regSJ.locations += [SMGLocation(player, loc_name, location_table[loc_name], regSJ) for loc_name in locSJ_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regHH.locations.append(SMGLocation(player, "SJ: Purple Coin Spacewalk", location_table["SJ: Purple Coin Spacewalk"], regSJ))
    world.regions.append(regSJ)  
    # defines the Battlerock galaxy
    regBR = Region("Menu", RegionType.Generic, "Battlerock", player, world)
    locBR_names = [name for name, id in locBR_table.items()]
    regBR.locations += [SMGLocation(player, loc_name, location_table[loc_name], regBR) for loc_name in locBR_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regBR.locations.append(SMGLocation(player, "BR: Purple Coins on the Battlerock", location_table["BR: Purple Coins on the Battlerock"], regBR)) 
    world.regions.append(regBR)     
    # defines the Beach Bowl galaxy
    regBB = Region("Menu", RegionType.Generic, "Beach Bowl", player, world)
    locBB_names = [name for name, id in locBB_table.items()]
    regBB.locations += [SMGLocation(player, loc_name, location_table[loc_name], regBB) for loc_name in locBB_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regBB.locations.append(SMGLocation(player, "BB: Beachcombing for Purple Coins", location_table["BB: Beachcombing for Purple Coins"], regBB))    
    world.regions.append(regBB)  
    # define Ghostly galaxy
    regG = Region("Menu", RegionType.Generic, "Ghostly", player, world)
    locG_names = [name for name, id in locGG_table.items()]
    regG.locations += [SMGLocation(player, loc_name, location_table[loc_name], regG) for loc_name in locG_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regG.locations.append(SMGLocation(player, "G: Purple Coins in the Bone Pen", location_table["G: Purple Coins in the Bone Pen"], regG))    
    world.regions.append(regG)  
    # defines the Gusty Gardens galaxy 
    regGG = Region("Menu", RegionType.Generic, "Gusty Gardens", player, world)
    locGG_names = [name for name, id in locGG_table.items()]
    regGG.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGG) for loc_name in locGG_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGG.locations.append(SMGLocation(player, "GG: Purple Coins on the Puzzle Cube", location_table["GG: Purple Coins on the Puzzle Cube"], regGG))    
    world.regions.append(regGG)  
    # defines Freezeflame galaxy
    regFF = Region("Menu", RegionType.Generic, "Freezeflame", player, world)
    locFF_names = [name for name, id in locFF_table.items()]
    regFF.locations += [SMGLocation(player, loc_name, location_table[loc_name], regFF) for loc_name in locFF_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGG.locations.append(SMGLocation(player, "FF: Purple Coins on the Summit", location_table["FF: Purple Coins on the Summit"], regFF))  
    world.regions.append(regFF)  
    # defines DustyDune Galaxy
    regDDune = Region("Menu", RegionType.Generic, "Dusty Dune", player, world)
    locDDune_names = [name for name, id in locDDune_table.items()]
    regDDune.locations += [SMGLocation(player, loc_name, location_table[loc_name], regDDune) for loc_name in locDDune_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDDune.locations.append(SMGLocation(player, "DDune: Purple Coins in the Desert", location_table["DDune: Purple Coin in the Desert"], regDDune))  
    world.regions.append(regDDune)  
    # defines golden leaf galaxy
    regGL = Region("Menu", RegionType.Generic, "Gold Leaf", player, world)
    locGL_names = [name for name, id in locGL_table.items()]
    regGL.locations += [SMGLocation(player, loc_name, location_table[loc_name], regGL) for loc_name in locGL_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regGL.locations.append(SMGLocation(player, "GL: Purple Coins in the Woods", location_table["GL: Purple Coins in the Woods"], regGL)) 
    world.regions.append(regGL)  
    # defines the Sea slide galaxy
    regSS = Region("Menu", RegionType.Generic, "Sea Slide", player, world)
    locSS_names = [name for name, id in locSS_table.items()]
    regSS.locations += [SMGLocation(player, loc_name, location_table[loc_name], regSS) for loc_name in locSS_names]    
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regSS.locations.append(SMGLocation(player, "SS: Purple Coins by the Seaside", location_table["SS: Purple Coins by the Seaside"], regSS)) 
    world.regions.append(regSS)
    # defines toy time galaxy 
    regTT = Region("Menu", RegionType.Generic, "Toy Time", player, world)
    locTT_names = [name for name, id in locTT_table.items()]
    regTT.locations += [SMGLocation(player, loc_name, location_table[loc_name], regTT) for loc_name in locTT_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regSS.locations.append(SMGLocation(player, "TT: Luigi's Purple Coins", location_table["TT: Luigi's Purple Coins"], regSS)) 
    world.regions.append(regTT)  
    # defines deep dark galaxy
    regDD = Region("Menu", RegionType.Generic, "Deep Dark", player, world)
    locDD_names = [name for name, id in locDD_table.items()]
    regDD.locations += [SMGLocation(player, loc_name, location_table[loc_name], regDD) for loc_name in locDD_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDD.locations.append(SMGLocation(player, "DD: Plunder the Purple Coins", location_table["DD: Plunder the Purple Coins"], regDD)) 
    world.regions.append(regDD)  
    # defines Dreadnaught galaxy
    regDN = Region("Menu", RegionType.Generic, "Dreadnaught", player, world)
    locDN_names = [name for name, id in locDN_table.items()]
    regDN.locations += [SMGLocation (player, loc_name, location_table[loc_name], regDN) for loc_name in locDN_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regDN.locations.append(SMGLocation(player, "DN: Battlestation's Purple Coins", location_table["DN: Battlestation's Purple Coins"], regDN)) 
    world.regions.append(regDN)  
    # defines Melty Molten galaxy
    regMM = Region("Menu", RegionType.Generic, "Melty Molten", player, world)
    locMM_names = [name for name, id in locMM_table.items()]
    regMM.locations += [SMGLocation (player, loc_name, location_table[loc_name], regMM) for loc_name in locMM_names]
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        regMM.locations.append(SMGLocation(player, "MM: Red-Hot Purple Coins", location_table["MM: Red-Hot Purple Coins"], regMM)) 
    world.regions.append(regMM)  
    
    #defines the fountain
    regFountain = create_region("Fountain", player, world)
    world.regions.append(regFountain)
    #defines the kitchen
    regKitchen = create_region("Kitchen", player, world)
    world.regions.append(regKitchen)
    #defines the bedroom
    regBedroom = create_region("Bedroom", player, world)
    world.regions.append(regBedroom)
    #defines the Engine Room
    regEngineRoom = create_region("Engine Room", player, world)
    world.regions.append(regEngineRoom)
    #defines the garden
    regGarden = create_region("Garden", player, world)
    world.regions.append(regGarden)      
def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule=None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, '', sourceRegion)
    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, player: int, world: MultiWorld) -> Region:
    return Region(name, RegionType.Generic, name, player, world)

def create_default_locs(reg: Region, locs, player):
    reg_names = [name for name, id in locs.items()]
    reg.locations += [SMGLocation(player, loc_name, location_table[loc_name], reg) for loc_name in locs]

