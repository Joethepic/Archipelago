from io import BytesIO

from gclib.yaz0_yay0 import Yaz0

from wiithon.formats.rarc import Rarc

from ...Constants.patch_constants import *
from ..extensions import SMGObject

class AstroDomeEntrance(SMGObject):
    name: str
    index: int
    file_data: bytes

    def __init__(self, dome_name: str, index: int):
        super().__init__(ASTRO_DOME_ENTRANCE_PATH.format(dome_name))

        self.arc_file = Rarc.read(Yaz0.decompress(BytesIO(self.patcher.read_file(self.path))))
        self.name = dome_name
        self.index = index

    def update(self) -> None:
        pass

    def rename(self, new_dome_name: str):
        print(f"Renaming dome {self.name} -> {new_dome_name}")

        self.arc_file.get_node("astrodomeentrance" + self.name.lower()).name = "astrodomeentrance" + new_dome_name.lower()
        self.arc_file.get_file("astrodomeentrance" + self.name.lower() + ".bdl").name = "astrodomeentrance" + new_dome_name.lower() + ".bdl"

        self.patcher.replace_file(ASTRO_DOME_ENTRANCE_PATH.format(new_dome_name), self.arc_file.get_bytes())

class AstroDomeEntrances(SMGObject):
    entrances: list[AstroDomeEntrance]

    def __init__(self):
        self.entrances = [AstroDomeEntrance(Domes.TERRACE, 1),
                          AstroDomeEntrance(Domes.FOUNTAIN, 2),
                          AstroDomeEntrance(Domes.KITCHEN, 3),
                          AstroDomeEntrance(Domes.BEDROOM, 4),
                          AstroDomeEntrance(Domes.ENGINE, 5),
                          AstroDomeEntrance(Domes.GARDEN, 6)]

    def update(self, dome_shuffle: dict[int, int], **kwargs):
        reverse_shuffle: dict[int, int] = {value: key for key, value in dome_shuffle.items()}

        for index, entrance in enumerate(self.entrances):
            new_index: int = reverse_shuffle[index + 1] - 1
            new_dome_name = self.entrances[new_index].name
            
            entrance.rename(new_dome_name)
