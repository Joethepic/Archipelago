import typing
from Options import Option, Choice, Range
 
 
class EnablePurpleCoinStars(Choice):
    """tuning this off we allow purple coin stars to count as checks do note all purple coin stars are postgame only but one."""
    display_name = "enable_purple_coin_stars"
    option_main_game_only = 0
    option_all = 1
    option_none = 2
    default = 0
 
class StarstoFinish(Range):
    "This will set the number of stars required to reach the center of the universe."
    display_name = "Stars_to_finish"
    range_start = 25
    range_end = 99
    default = 60
 
smg_options: typing.Dict[str, type(Option)] = {
    "enable_purple_coin_stars": EnablePurpleCoinStars,
    "Stars_to_finish": StarstoFinish,
}


