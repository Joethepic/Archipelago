from dataclasses import dataclass
from typing import Dict, Any


from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle, OptionCounter, OptionDict, OptionGroup, \
    DeathLinkMixin
from .items import trap_filler_items

class GalaxyShuffle(OptionSet):
    """
    Determine what kinds of galaxies should be added to the shuffle pool. Leave empty to disable shuffling

    Full: Any galaxy in any galaxy position

    Dome Majors: Add Major galaxies to shuffle pool

    Dome Minors: Add Minor galaxies to shuffle pool

    Observatory Specials: Add Direct from Observatory galaxies to shuffle pool, such as Trials or Hungry Luma galaxies

    Bosses: Add Boss galaxies to shuffle pool
    """
    display_name = "Galaxy Shuffle"
    internal_name = "galaxy_shuffle"
    valid_keys = {"Full", "Dome Majors", "Dome Minors", "Observatory Specials", "Bosses"}

class GalaxyShuffleType(Choice):
    """
    Choose how galaxies are shuffled between slots. Does nothing if no galaxies are randomized

    By Type - Galaxies will only be shuffled between slots of the same kind. Major galaxies on major galaxies,
    Boss galaxies on Boss galaxies, Observatory Galaxies on observatory galaxies

    Major Separately - Major galaxies will only be shuffled among themselves, but all other galaxies can go anywhere

    Full - Any galaxy can go on any Galaxy slot
    """
    display_name = "Galaxy Shuffle Type"
    internal_name = "galaxy_shuffle_type"
    option_By_Type = 0
    option_Major_Separate = 1
    option_Full = 2

class ShuffleDomes(Toggle):
    """
    Shuffle Dome entrances
    """
    display_name = "Dome Shuffle"
    internal_name = "dome_shuffle"

# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Toggle):
    """
    Add Purple Coin star locations. These will turn Purple Coin stars into locations, accessible before Final Bowser. If
    this option is off, Purple Coin stars will give nothing when completed.
    """
    display_name = "Enable Purple Coin Stars"
    internal_name = "enable_purple_coin_stars"

# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    """
    This will set the number of stars required to reach the center of the universe.
    This will be capped at 103 stars if extra locations are not enabled.
    """
    display_name = "Stars to finish"
    internal_name = "stars_to_finish"
    range_start = 25
    range_end = 119
    default = 60

class Dome1Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 1, which is the Terrace in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations
    The first orbit in Dome 1 will always have no star requirement.

    These are based on each orbit in the dome, in case levels are shuffled. First Orbit is excluded, to ensure you have
    at least one world to start.
    """
    display_name = "Dome 1 Access"
    internal_name = "dome_one_counts"
    min = 0
    max = 8
    valid_keys = ["Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }


class Dome2Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 2, which is the Fountain in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 2 Access"
    internal_name = "dome_two_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome3Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 3, which is the Kitchen in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 3 Access"
    internal_name = "dome_three_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome4Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 4, which is the Bedroom in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 4 Access"
    internal_name = "dome_four_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome5Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 5, which is the Engine Room in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 5 Access"
    internal_name = "dome_five_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome6Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 6, which is the Garden in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and will be capped based on an estimated number of available locations

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 6 Access"
    internal_name = "dome_six_counts"
    min = 0
    max = 20
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0
    }


class MarioColors(OptionDict):
    """
    Choose new colors for part of Mario's Outfit! (These will also be applied to Luigi)
    4 pieces are changeable: 'Hat' , 'Overalls', 'Shoes', 'Gloves'

    The following predetermined colors are available:
    "Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black", "Brown", "White", "Pink", "Gray"

    Putting Random with any color will set all 4 pieces to a random color. If a piece of clothing is missing from the option,
    a random color will be chosen for it. (example Random: Green)
    If a given piece of clothing does not have a valid value or is not included at all, one will be chosen for you.
    Invalid colors other than the ones above will turn into a random color.
    """
    display_name = "Mario Colors"
    internal_name = "mario_colors"
    valid_keys = ["Hat", "Overalls", "Shoes", "Gloves", "Random"]
    valid_values = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black", "Brown", "White", "Pink", "Gray"]
    default = {
        "Hat": "Red",
        "Overalls": "Blue",
        "Shoes": "Brown",
        "Gloves": "White"
    }
    slot_req = False

class HideGalaxy(Choice):
    """
    Choose Galaxy visibility in domes

    Visible - All galaxies will have a shadow silhouette represent the galaxy present and show star count required to open

    Hide Minors - Minor Galaxies will appear as question mark blocks until opened for the first time. Majors will still
        show a galaxy silhouette but minors will not show the star count required to open them.

    Hide All - All Galaxies will appear as question mark blocks until opened for the first time. Neither will show how
        many stars are required to open the galaxy.
    """
    display_name = "Hide Galaxy"
    internal_name = "hide_galaxy"
    default = 1
    option_Visible = 0
    option_Hide_Minors = 1
    option_Hide_All = 2
    slot_req = False

class StarColors(Toggle):
    """
    If this option is enabled, each star in the Star Select screen will be colored according to the classification of
    the item on that star location. After it has been collected, the star will be clear

    If the option is disabled, all stars will start clear and become colored according to item classification after
    clearing the stage.
    """
    display_name = "Star Colors"
    internal_name = "star_colors"
    slot_req = False

class TrapWeights(OptionCounter):
    """
    Set Trap Weights for traps chosen as filler items, if Trap Percentage is greater than 0
    Each weight represents a number of balls in a lottery roller with that trap on it.
    So if you had ___ Trap set to 3, and ___ Trap set to 7, and the rest set to 0,
    you would have a 3/10 for a ___ Trap to be chosen when rolling for trap fillers
    Must be between 0 and 100
    """
    display_name = "Trap Weights"
    internal_name = "trap_weights"
    min = 0
    max = 100
    valid_keys = trap_filler_items.keys()
    default = {item: data.default_weight for item, data in trap_filler_items.items()}
    all_on_dict = {item: 100 for item in trap_filler_items.keys()}
    all_off_dict = {item: 0 for item in trap_filler_items.keys()}

class TrapPercentage(Range):
    """
    Set the percentage of filler items that are traps. Default percentage is 0%
    """
    display_name = "Trap Percentage"
    internal_name = "trap_percentage"
    range_start = 0
    range_end = 100
    default = 0

# this defines all the options.
@dataclass
class SMGOptions(PerGameCommonOptions, DeathLinkMixin):
    enable_purple_coin_stars: EnablePurpleCoinStars
    stars_to_finish: StarstoFinish
    mario_colors: MarioColors
    dome_one_counts: Dome1Offsets
    dome_two_counts: Dome2Offsets
    dome_three_counts: Dome3Offsets
    dome_four_counts: Dome4Offsets
    dome_five_counts: Dome5Offsets
    dome_six_counts: Dome6Offsets
    dome_shuffle: ShuffleDomes
    galaxy_shuffle: GalaxyShuffle
    galaxy_shuffle_type: GalaxyShuffleType
    hide_galaxy: HideGalaxy
    star_colors: StarColors
    trap_weights: TrapWeights
    trap_percentage: TrapPercentage

option_groups = [
    OptionGroup("Extra Locations", [
        EnablePurpleCoinStars,
    ]),
    OptionGroup("Access Options", [
        StarstoFinish,
        ShuffleDomes,
        GalaxyShuffle,
        GalaxyShuffleType
    ]),
    OptionGroup("Dome Offsets", [
       Dome1Offsets,
       Dome2Offsets,
       Dome3Offsets,
       Dome4Offsets,
       Dome5Offsets,
       Dome6Offsets
    ]),
#    OptionGroup("Observatory Luma Behavior", [

#    ]),
    OptionGroup("Cosmetics", [
        MarioColors,
        StarColors,
        HideGalaxy,
    ]),
    OptionGroup("Item Pool Modifications", [
        TrapWeights,
        TrapPercentage,
    ])
]


option_presets: dict[str, dict[str, Any]] = {

}
