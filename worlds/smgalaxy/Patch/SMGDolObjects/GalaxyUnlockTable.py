from io import BytesIO

from wiithon.formats.bcsv import BCSV

from ..hashtable import hash_to_name
from worlds.smgalaxy.Patch.extensions import SMGDOLObject
from ...Constants.patch_constants import *

class GalaxyUnlockTableEntry:
    def __init__(self, entry_index: int, name: str, open_condition0: str, open_condition1: str,
                 power_star_requirement: int, return_dome: int):
        self.entry_index: int = entry_index
        self.name: str = name
        self.open_condition0: str = open_condition0
        self.open_condition1: str = open_condition1
        self.power_star_requirement: int = power_star_requirement
        self.return_dome: int = return_dome

    def __str__(self):
        return ' '.join([str(self.entry_index),
                         str(self.name),
                         str(self.open_condition0),
                         str(self.open_condition1),
                         str(self.power_star_requirement),
                         str(self.return_dome)])


class GalaxyUnlockTable(SMGDOLObject):
    table: BCSV

    start_address: int
    end_address: int
    size: int

    entries: list[GalaxyUnlockTableEntry]

    def __init__(self):
        self.start_address = GALAXY_UNLOCK_TABLE_START_ADDRESS
        self.end_address = GALAXY_UNLOCK_TABLE_END_ADDRESS
        self.size = self.end_address - self.start_address

        self.entries = []

        table_bytes: bytes = self.dol.read_at(self.start_address, self.size)
        self.table = BCSV.import_bcsv(BytesIO(table_bytes), field_names=hash_to_name, str_fmt="shift-jis")

        for entry_index in range(len(self.table.entries)):
            name = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.NAME]
            entry = GalaxyUnlockTableEntry(entry_index, name, '', '', 0, 0)
            self.entries.append(entry)

    def set_new_entry_values(self, name: str, star_requirement: int, dome_index: int) -> None:
        for entry in self.entries:
            if entry.name != name:
                continue

            entry.power_star_requirement = star_requirement
            entry.return_dome = dome_index

    def update(self, dome_galaxies: list[GalaxyDestination], star_requirements: dict[str, int], **kwargs) -> None:
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1, 7)}

        for location, requirement in star_requirements.items():
            dome_index = int(location[1])
            orbit_index = int(location[3:])

            requirements[dome_index][orbit_index] = requirement

        for galaxy in dome_galaxies:
            star_requirement: int = requirements[galaxy.dome_index][galaxy.orbit_index + 1]

            self.set_new_entry_values(galaxy.name, star_requirement, galaxy.dome_index)

        for entry in self.entries:
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.NAME] = entry.name
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION0] = entry.open_condition0
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION1] = entry.open_condition1
            self.table.entries[entry.entry_index][
                GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT] = entry.power_star_requirement
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.RETURN_DOME] = entry.return_dome

        bcsv_bytes = self.table.export_bcsv(str_fmt="shift-jis")

        if bcsv_bytes.seek(2, 0) > self.size:
            raise ValueError(
                f"New embedded BCSV is bigger than the original BCSV.\nNew size: {bcsv_bytes.seek(2, 0)}, old size: {self.size}")

        self.dol.write_at(self.start_address, bcsv_bytes.getvalue())
