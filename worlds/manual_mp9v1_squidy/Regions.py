from BaseClasses import Entrance, MultiWorld, Region
from .Locations import ManualLocation
from ..AutoWorld import World

regionMap = {
	"Manual": []
}

def create_regions(base: World, world: MultiWorld, player: int): 
    # Create regions and assign locations to each region
    for region in regionMap:
        exit_array = regionMap[region]
        if len(exit_array) == 0:
            exit_array = None

        new_region = create_region(base, world, player, region, [
            location["name"] for location in base.location_table if location["region"] == region
        ], exit_array)
        world.regions += [new_region]

    menu = create_region(base, world, player, "Menu", None, ["Manual"])
    world.regions += [menu]
    menuConn = world.get_entrance("MenuToManual", player)
    menuConn.connect(world.get_region("Manual", player))

    # Link regions together
    for region in regionMap:
        for linkedRegion in regionMap[region]:
            connection = world.get_entrance(getConnectionName(region, linkedRegion), player)
            connection.connect(world.get_region(linkedRegion, player))

def create_region(base: World, world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    
    if locations:
        for location in locations:
            loc_id = base.location_name_to_id.get(location, 0)
            locationObj = ManualLocation(player, location, loc_id, ret)
            ret.locations.append(locationObj)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, getConnectionName(name, exit), ret))
    return ret

def getConnectionName(entranceName: str, exitName: str):
    return entranceName + "To" + exitName


