from typing import Self, NamedTuple
from io import BytesIO
from enum import StrEnum
import gclib.fs_helpers as fs
from gclib.dol import DOL

from .extensions import DOLExtended
from .bcsv import BCSV

DOL_RELATIVE_PATH: str = "/DATA/sys/main.dol"

NAME_TO_CREATE_FUNCTION_START_ADDRESS = 0x80533980
NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT = 1183
NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE = 0xC

NAME_TO_ARCHIVE_START_ADDRESS = 0x805370f4
NAME_TO_ARCHIVE_ELEMENT_COUNT = 440
NAME_TO_ARCHIVE_ELEMENT_SIZE = 0x8

NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS = 0x80537eb4
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT = 91
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE = 0x8

GALAXY_UNLOCK_TABLE_START_ADDRESS = 0x8053c800
GALAXY_UNLOCK_TABLE_END_ADDRESS = 0x8053d520

class Pointer:
    base_address: int
    pointing_address: int
    
    def __init__(self, dol: DOL, base_address: int):
        self.dol = dol
        
        self.base_address = base_address

        self.read_pointer()

    def read_pointer(self):
        self.pointing_address = self.dol.read_data(fs.read_u32, self.base_address)
    
    def write_pointer(self):
        self.dol.write_data(fs.write_u32, self.base_address, self.pointing_address)

    def swap_with_pointer(self, other: Self):
        self.pointing_address, other.pointing_address = other.pointing_address, self.pointing_address

        self.write_pointer()
        other.write_pointer()

class CharPointer(Pointer):
    string: str

    def read_pointer(self):
        super().read_pointer()

        if self.pointing_address != 0:
            self.string = self.dol.read_data(fs.read_str_until_null_character, self.pointing_address)
        else:
            self.string = None
    
    def write_string(self):
        self.dol.write_data(fs.write_str_with_null_byte, self.pointing_address, self.string)

class FunctionPointer(Pointer):
    def write_function_address(self, new_function_address: int):
        self.pointing_address = new_function_address

        self.write_pointer()

class Name2CreateFuncElement:
    name_pointer: CharPointer
    create_function_pointer: FunctionPointer
    archive_name_pointer: CharPointer

    def __init__(self, name_pointer: CharPointer, create_function_pointer: FunctionPointer, archive_name_pointer: CharPointer):
        self.name_pointer = name_pointer
        self.create_function_pointer = create_function_pointer
        self.archive_name_pointer = archive_name_pointer

class Name2ArchiveElement:
    object_name_pointer: CharPointer
    archive_name_pointer: CharPointer

    def __init__(self, object_name_pointer: CharPointer, archive_name_pointer: CharPointer):
        self.object_name_pointer = object_name_pointer
        self.archive_name_pointer = archive_name_pointer

class Name2MakeArchiveListFuncElement:
    name_pointer: CharPointer
    archive_function: FunctionPointer

    def __init__(self, name_pointer: CharPointer, archive_function: FunctionPointer):
        self.name_pointer = name_pointer
        self.archive_function = archive_function

class NameObjFactory:
    name_to_create_function_elements: list[Name2CreateFuncElement]
    name_to_archive_elements: list[Name2ArchiveElement]
    name_to_make_archive_list_function_elements: list[Name2MakeArchiveListFuncElement]

    def __init__(self, dol: DOL):
        self.dol = dol

        # Initialise the Name2CreateFunction list
        start_address = NAME_TO_CREATE_FUNCTION_START_ADDRESS
        element_count = NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE

        self.name_to_create_function_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_address = offset + 0x0
            create_function_address = offset + 0x4
            archive_name_address = offset + 0x8

            name_pointer: CharPointer = CharPointer(self.dol, name_address)
            create_function_pointer: FunctionPointer = FunctionPointer(self.dol, create_function_address)
            archive_name_pointer: CharPointer = CharPointer(self.dol, archive_name_address)

            element: Name2CreateFuncElement = Name2CreateFuncElement(name_pointer, create_function_pointer, archive_name_pointer)

            self.name_to_create_function_elements.append(element)

        # Initialise the Name2Archive list    
        start_address = NAME_TO_ARCHIVE_START_ADDRESS
        element_count = NAME_TO_ARCHIVE_ELEMENT_COUNT
        element_size = NAME_TO_ARCHIVE_ELEMENT_SIZE

        self.name_to_archive_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            object_name_address = offset + 0x0
            archive_name_address = offset + 0x4

            object_name_pointer: CharPointer = CharPointer(self.dol, object_name_address)
            archive_name_pointer: CharPointer = CharPointer(self.dol, archive_name_address)

            element: Name2ArchiveElement = Name2ArchiveElement(object_name_pointer, archive_name_pointer)

            self.name_to_archive_elements.append(element)

        # Initialise the Name2MakeArchiveList list
        start_address = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS
        element_count = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE

        self.name_to_make_archive_list_function_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_address = offset + 0x0
            archive_function_address = offset + 0x4

            name_pointer: CharPointer = CharPointer(self.dol, name_address)
            archive_function_pointer: FunctionPointer = FunctionPointer(self.dol, archive_function_address)

            element: Name2MakeArchiveListFuncElement = Name2MakeArchiveListFuncElement(name_pointer, archive_function_pointer)

            self.name_to_make_archive_list_function_elements.append(element)

    def get_name_to_create_function_elements_by_name(self, name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.name_pointer.string == name]

    def get_name_to_create_function_elements_by_create_function(self, create_function_address: int) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.create_function_pointer.pointing_address == create_function_address]
    
    def get_name_to_create_function_elements_by_archive_name(self, archive_name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.archive_name_pointer.string == archive_name]

class GalaxyUnlockTableFieldNames(StrEnum):
    NAME: str = "name"
    MAP_PANE_NAME: str = "MapPaneName"
    OPEN_CONDITION0: str = "OpenCondition0"
    OPEN_CONDITION1: str = "OpenCondition1"
    OPEN_CONDITION2: str = "OpenCondition2"
    POWER_STAR_REQUIREMENT: str = "PowerStarNum"
    RETURN_DOME: str = "GrandGalaxyNo"

class GalaxyUnlockTableEntry:
    def __init__(self, entry_index: int, name: str, open_condition0: str, open_condition1: str,
                 power_star_requirement: int, return_dome: int):
        self.entry_index: int = entry_index
        self.name: str = name
        self.open_condition0: str = open_condition0
        self.open_condition1: str = open_condition1
        self.power_star_requirement: int = power_star_requirement
        self.return_dome: int = return_dome

class GalaxyUnlockTable:
    table: BCSV

    entries: list[GalaxyUnlockTableEntry]

    def __init__(self, dol: DOL):
        start_address = GALAXY_UNLOCK_TABLE_START_ADDRESS
        end_address = GALAXY_UNLOCK_TABLE_END_ADDRESS
        size = end_address - start_address

        table_bytes: bytes = dol.read_data(fs.read_bytes, start_address, size)
        self.table = BCSV(BytesIO(table_bytes))

        self.name_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.NAME)
        self.open_condition0_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.OPEN_CONDITION0)
        self.open_condition1_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.OPEN_CONDITION1)
        self.power_star_requirement_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT)
        self.return_dome_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.RETURN_DOME)
        
        for entry_index in range(self.table.entry_count):
            entry = self.get_entry(entry_index)
            self.table.entries.append(entry)
    
    def get_entry(self, entry_index: int) -> GalaxyUnlockTableEntry:
        name = self.table.get_value_by_index(entry_index, self.name_index)
        open_condition0 = self.table.get_value_by_index(entry_index, self.open_condition0_index)
        open_condition1 = self.table.get_value_by_index(entry_index, self.open_condition1_index)
        power_star_requirement = self.table.get_value_by_index(entry_index, self.power_star_requirement_index)
        return_dome = self.table.get_value_by_index(entry_index, self.return_dome_index)

        return GalaxyUnlockTableEntry(entry_index, name, open_condition0, open_condition1,
                                      power_star_requirement, return_dome)
    
    def set_entry(self, entry: GalaxyUnlockTableEntry) -> None:
        self.table.set_value_by_index(entry.entry_index, self.name_index, entry.name)
        self.table.set_value_by_index(entry.entry_index, self.open_condition0_index, entry.open_condition0)
        self.table.set_value_by_index(entry.entry_index, self.open_condition1_index, entry.open_condition1)
        self.table.set_value_by_index(entry.entry_index, self.power_star_requirement_index, entry.power_star_requirement)
        self.table.set_value_by_index(entry.entry_index, self.return_dome_index, entry.return_dome)

class SMGDOL(DOLExtended):
    """Extends the gclib DOL class to be easily useable for Super Mario Galaxy."""
    unlabeled_table_start_address = 0x8053c800
    unlabeled_table_end_address = 0x8053d520
    unlabeled_table_size = unlabeled_table_end_address - unlabeled_table_start_address

    name_object_factory: NameObjFactory
    galaxy_unlock_table: GalaxyUnlockTable

    def __init__(self):
        self.relative_path = DOL_RELATIVE_PATH
        super().__init__()
        
        self.unlabeled_table_bytes = self.read_data(fs.read_bytes, self.unlabeled_table_start_address, self.unlabeled_table_size)
        self.unlabeled_table = BCSV(BytesIO(self.unlabeled_table_bytes))

        self.name_object_factory = NameObjFactory(self)
        self.galaxy_unlock_table = GalaxyUnlockTable(self)

    def save(self):
        self.unlabeled_table.save_changes()
        self.write_data(fs.write_bytes, self.unlabeled_table_start_address, self.unlabeled_table.data.getvalue())
        self.save_changes()

        with open(self.absolute_file_path, 'wb') as f:
            f.write(self.data.getvalue())
