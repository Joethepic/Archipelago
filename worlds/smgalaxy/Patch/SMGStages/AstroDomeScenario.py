from enum import StrEnum

from ..extensions import RARCExtended
from ..bcsv import BCSV

ASTRO_DOME_SCENARIO_RELATIVE_PATH = "/DATA/files/StageData/AstroDome/AstroDomeScenario.arc"
SCENARIO_DATA_FILE_NAME = "scenariodata.bcsv"

class ScenarioDataFieldName(StrEnum):
    SCENARIO_NUMBER: str = "ScenarioNo"
    SCENARIO_NAME: str = "ScenarioName"
    POWER_STAR_ID: str = "PowerStarId"
    APPEAR_POWER_STAR_OBJect: str = "AppearPowerStarObj"
    COMET: str = "Comet"
    LUIGI_MODE_TIMER: str = "LuigiModeTimer"
    ASTRO_DOME: str = "AstroDome"
    IS_HIDDEN: str = "IsHidden"
    ERROR_CHECK: str = "ErrorCheck"


class AstroDomeScenario(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRO_DOME_SCENARIO_RELATIVE_PATH
        super().__init__()

        for file in self.get_node_by_path('').files:
            if file.name == SCENARIO_DATA_FILE_NAME:
                self.scenariodata = BCSV(file)

    def update(self, dome_shuffle: dict[int, int]) -> None:
        scenariono_index = self.scenariodata.get_field_index(ScenarioDataFieldName.SCENARIO_NUMBER)
        astrodome_index = self.scenariodata.get_field_index(ScenarioDataFieldName.ASTRO_DOME)

        reverse_shuffle: dict[int, int] = {value: key for key, value in dome_shuffle.items()}

        print("Updating dome loading zones...")
        
        for entry_index in range(self.scenariodata.entry_count):
            scenariono = self.scenariodata.get_value_by_index(entry_index, scenariono_index)
            new_value = 2**(reverse_shuffle[scenariono] - 1)

            print(f"Loading zone dome {scenariono} -> dome {reverse_shuffle[scenariono]}")

            self.scenariodata.set_value_by_index(entry_index, astrodome_index, new_value)

        self.scenariodata.save_changes()
