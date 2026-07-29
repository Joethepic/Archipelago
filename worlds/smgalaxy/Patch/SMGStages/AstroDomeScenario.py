from wiithon import WiiIsoPatcher
from wiithon.file_helper.bcsv import BCSV

from ...Constants.patch_constants import *
from ..extensions import SMGObject

class AstroDomeScenario(SMGObject):
    def __init__(self, patcher: WiiIsoPatcher):
        super().__init__(patcher, ASTRO_DOME_SCENARIO_PATH)

    def update(self, shuffle: dict[int, int]) -> None:
        self.shuffle_loading_zones(shuffle)

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

        print("Updating dome loading zones...")

        bcsv: BCSV
        with self.edit_bcsv(SCENARIO_DATA_FILE_NAME) as bcsv:
            for entry in bcsv.entries:
                scenariono = entry["ScenarioNo"]

                print(f"Loading zone dome {scenariono} -> dome {shuffle[scenariono]}")

                entry["ScenarioNo"] = 1 << (shuffle[scenariono] - 1)
