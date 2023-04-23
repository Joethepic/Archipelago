from ..generic.Rules import set_rule
from ..AutoWorld import World
from BaseClasses import MultiWorld

def set_rules(base: World, world: MultiWorld, player: int):
    # Location access rules
    for location in base.location_table:
        locFromWorld = world.get_location(location["name"], player)
        if "requires" in location: # Specific item access required
            def fullLocationCheck(state, location=location):
                canAccess = True

                for item in location["requires"]:
                    # if the require entry is an object with "or" or a list of items, treat it as a standalone require of its own
                    if (isinstance(item, dict) and "or" in item and isinstance(item["or"], list)) or (isinstance(item, list)):
                        canAccessOr = True
                        or_items = item
                        
                        if isinstance(item, dict):
                            or_items = item["or"]

                        for or_item in or_items:
                            or_item_parts = or_item.split(":")
                            or_item_name = or_item
                            or_item_count = 1

                            if len(or_item_parts) > 1:
                                or_item_name = or_item_parts[0]
                                or_item_count = int(or_item_parts[1])

                            if not state.has(or_item_name, player, or_item_count):
                                canAccessOr = False

                        if canAccessOr:
                            canAccess = True
                            break
                    else:
                        item_parts = item.split(":")
                        item_name = item
                        item_count = 1

                        if len(item_parts) > 1:
                            item_name = item_parts[0]
                            item_count = int(item_parts[1])

                        if not state.has(item_name, player, item_count):
                            canAccess = False

                return canAccess
            set_rule(locFromWorld, fullLocationCheck)
        else: # Only region access required
            def allRegionsAccessible(state, location=location):
                return True
            set_rule(locFromWorld, allRegionsAccessible) # everything is in the same region in manual

    # Victory requirement
    world.completion_condition[player] = lambda state: state.has("__Victory__", player)