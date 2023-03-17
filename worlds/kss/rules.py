from sqlite3 import connect

from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule
from .options import Goldgoal

def set_rules(world, player: int, self):

    world.completion_condition[player] = lambda state: state.has("Victory", player)