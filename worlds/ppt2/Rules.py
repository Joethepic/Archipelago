from ..generic.Rules import set_rule, add_rule
from .Locations import exclusion_table, get_postgame_advancements
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin

set_rule(world.get_location("1-1", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-2", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-3", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-4", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-5", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-6", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("1-7", player), lambda state: state.has("W1Key", player))
set_rule(world.get_location("Marle 1", player), lambda state: state.has("W1Key", player))