from wiithon import WiiIsoPatcher
from wiithon.formats.bcsv import BCSV

from worlds.smgalaxy.Patch import hashtable

from ...Constants.patch_constants import *
from ..extensions import SMGObject

class AstroDomeScenario(SMGObject):
    def __init__(self):
        super().__init__(ASTRO_DOME_SCENARIO_PATH)

    def update(self, dome_shuffle: dict[int, int], **kwargs) -> None:
        self.shuffle_loading_zones(dome_shuffle)

    def is_valid_shuffle(self, dome_shuffle: dict[int, int]) -> bool:
        """Validate that the dome shuffle mapping contains all indices 1-6 as both keys and values."""
        for index in range(1,7):
            if index not in dome_shuffle.keys() or index not in dome_shuffle.values():
                return False
            
        return True

    def shuffle_loading_zones(self, shuffle: dict[int, int]) -> None:
        """
        Shuffle the loading zones for the domes within the observatory. The shuffle maps the old dome index to the new dome index (from 1 to 6).
        The shuffle dict must contain all indices from 1 to 6 as both keys and values. The information to load the dome is contained in scenariodata.
        Field "AstroDome" determines which loading zone it should load and gets set according to the shuffle dict. The value of "AstroDome"
        is equal to 1 bitshifted left by dome index minus 1.
        shuffle:
            key: old dome index (1-6)
            value: new dome index (1-6)
        """
        # Make sure its a valid shuffle
        if not self.is_valid_shuffle(shuffle):
            raise ValueError(f"Invalid shuffle: {shuffle}")

        reverse_shuffle = {value: key for key, value in shuffle.items()}

        print("Updating dome loading zones...")

        bcsv: BCSV
        with self.patcher.edit_as(self.path + '/' + SCENARIO_DATA_FILE_NAME, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis") as bcsv:
            for entry in bcsv.entries:
                scenario_no = entry["ScenarioNo"]

                print(f"Loading zone dome {scenario_no} -> dome {shuffle[scenario_no]}")

                entry["ScenarioNo"] = shuffle[scenario_no]
                entry["AstroDome"] = 1 << (reverse_shuffle[scenario_no] - 1)
