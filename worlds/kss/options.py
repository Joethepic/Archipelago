from typing import TypedDict
from Options import Choice, Range

class Goldgoal(Range):
    display_name = "Gold required for goal"
    range_start = 100000
    range_end = 1000000
    default = 50000
    
kss_options = {
    "Gold_goal": Goldgoal
}