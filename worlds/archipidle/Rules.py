from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class ArchipIDLELogic(LogicMixin):
    def _archipidle_location_is_accessible(self, player_id, items_required):
        items_received = 0
        for item in self.prog_items:
            if item[1] == player_id:
                items_received += 1

        return items_received >= items_required


def set_rules(world: MultiWorld, player: int):
    for i in range(16, 31):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 4)
        )

    for i in range(31, 51):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 10)
        )

    for i in range(51, 101):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 20)
        )

    for i in range(101, 201):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state._archipidle_location_is_accessible(player, 40)
        )

    world.completion_condition[player] =\
        lambda state:\
        state.can_reach(world.get_location("IDLE item number 200", player), "Location", player)
