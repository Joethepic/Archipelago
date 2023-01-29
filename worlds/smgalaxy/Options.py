from typing import TypedDict
from Options import Choice, Range, Toggle
 
# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Choice):
    "tuning this off we allow purple coin stars to count as checks do note all purple coin stars are postgame only but one."
    display_name = "Enable Purple Coin Stars"
    option_main_game_only = 0
    option_all = 1
    option_none = 2
    # add back when caregories are fully done and enough settings to justify category = Randomized
# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    "This will set the number of stars required to reach the center of the universe."
    display_name = "Stars to finish"
    range_start = 25
    range_end = 99
    default = 60
    # add back when caregories are fully done and enough settings to justify category = Game Length

class ProgressiveGrandStars(Toggle):
   "This will make the grand stars progressive unlocking in the same order as the base game."
    display_name = "Progressive grand stars"
    # add back when caregories are fully done and enough settings to justify category = Game Length

class GalaxyShuffle(Toggle):
    """This will shuffle the galaxies so they will be in different locations."""
    display_name = "Galaxy_shuffle"
# add back when caregories are fully done and enough settings to justify category = Randomized
class Powerups(Toggle):
    """This enables the Powerups to be in the item pool."""
    display_name = "Shuffle Powerups"
# add back when caregories are fully done and enough settings to justify category = Randomized
class ExtraStars(Range):
    """This is how many extra power stars will be in the item pool."""
    range_start = 0
    range_end = 102
    display_name = "ExtraStars"
    # add back when caregories are fully done and enough settings to justify category = Game Length
# this defines all the options.
galaxy_options = {
    "enable_purple_coin_stars": EnablePurpleCoinStars,
    "Stars_to_finish": StarstoFinish,
    "Progressive_grand_stars": ProgressiveGrandStars,
    "Galaxy_shuffle": GalaxyShuffle,
    "randomize_Powerups": Powerups,
    "Extra_stars": ExtraStars,
}


