from ...Constants.patch_constants import *
from ..extensions import RARCExtended

class AstroDomeEntrance(RARCExtended):
    name: str

    def __init__(self, dome_name: str):
        self.relative_path = ASTRO_DOME_ENTRANCE_RELATIVE_PATH.format(dome_name)
        super().__init__()

        self.name = dome_name

    def rename(self, new_dome_name: str):
        self.relative_path = ASTRO_DOME_ENTRANCE_RELATIVE_PATH.format(new_dome_name)
        self.absolute_file_path = self.iso_base_path + self.relative_path
        
        print(f"Renaming dome: {self.name}")

        file_name: str = "astrodomeentrance" + new_dome_name.lower()

        root_node = self.get_node_by_path('')
        root_node.name = file_name
        
        for file in self.file_entries:
            if file.name.endswith(".bdl"):
                file.name = file_name + ".bdl"

        self.name = new_dome_name

class AstroDomeEntrances:
    entrances: list[AstroDomeEntrance]

    def __init__(self):
        self.entrances = [AstroDomeEntrance(DOMES[Domes.TERRACE]),
                          AstroDomeEntrance(DOMES[Domes.FOUNTAIN]),
                          AstroDomeEntrance(DOMES[Domes.KITCHEN]),
                          AstroDomeEntrance(DOMES[Domes.BEDROOM]),
                          AstroDomeEntrance(DOMES[Domes.ENGINE]),
                          AstroDomeEntrance(DOMES[Domes.GARDEN])]
    
    def rename_files(self, dome_shuffle: dict[int, int]):
        reverse_shuffle: dict[int, int] = {value: key for key, value in dome_shuffle.items()}

        for index, entrance in enumerate(self.entrances):
            new_index: int = reverse_shuffle[index + 1]
            new_dome_name: str = DOMES[new_index]
            
            entrance.rename(new_dome_name)

    def save(self):
        for entrance in self.entrances:
            entrance.save()
