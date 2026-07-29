from wiithon import WiiIsoPatcher

from ...Constants.patch_constants import *
from ..extensions import SMGObject

class AstroDomeEntrance(SMGObject):
    name: str
    file_data: bytes

    def __init__(self, patcher: WiiIsoPatcher, dome_name: str):
        super().__init__(patcher, ASTRO_DOME_ENTRANCE_PATH.format(dome_name) + ".arc")

        self.file_data = self.patcher.read_file(self.path)
        self.name = dome_name

    def rename(self, new_dome_name: str):
        print(f"Renaming dome: {self.name}")

        self.patcher.add_file(ASTRO_DOME_ENTRANCE_PATH.format(new_dome_name) + ".arc", self.file_data)

class AstroDomeEntrances:
    entrances: list[AstroDomeEntrance]

    def __init__(self, patcher: WiiIsoPatcher):
        self.entrances = [AstroDomeEntrance(patcher, DOMES[Domes.TERRACE]),
                          AstroDomeEntrance(patcher, DOMES[Domes.FOUNTAIN]),
                          AstroDomeEntrance(patcher, DOMES[Domes.KITCHEN]),
                          AstroDomeEntrance(patcher, DOMES[Domes.BEDROOM]),
                          AstroDomeEntrance(patcher, DOMES[Domes.ENGINE]),
                          AstroDomeEntrance(patcher, DOMES[Domes.GARDEN])]

    def update(self, dome_shuffle: dict[int, int]):
        self.rename_files(dome_shuffle)
    
    def rename_files(self, dome_shuffle: dict[int, int]):
        for entrance in self.entrances:
            entrance.patcher.remove_file(entrance.path)

        reverse_shuffle: dict[int, int] = {value: key for key, value in dome_shuffle.items()}

        for index, entrance in enumerate(self.entrances):
            new_index: int = reverse_shuffle[index + 1]
            new_dome_name: str = DOMES[new_index]
            
            entrance.rename(new_dome_name)
