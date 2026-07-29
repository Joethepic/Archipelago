from typing import Self
from io import BytesIO

from wiithon import WiiIsoPatcher
from wiithon.file_helper.dol import DOL
from wiithon.file_helper.bcsv import BCSV
from wiithon.helpers.Utils import read_string_until_null, write_string as wr_str

from .hashtable import hash_to_name
from ..Constants.patch_constants import *

class Pointer:
    base_address: int
    pointing_address: int
    
    def __init__(self, dol: "SMGDOL", base_address: int):
        self.dol = dol
        
        self.base_address = base_address

        self.read_pointer()

    def read_pointer(self):
        self.pointing_address = int.from_bytes(self.dol.dol.read_at(self.base_address, 4))
    
    def write_pointer(self):
        self.dol.dol.write_at(self.base_address, int.to_bytes(self.pointing_address, 4, "big"))

    def swap_with_pointer(self, other: Self):
        self.pointing_address, other.pointing_address = other.pointing_address, self.pointing_address

        self.write_pointer()
        other.write_pointer()

class CharPointer(Pointer):
    string: str | None

    def read_pointer(self):
        super().read_pointer()

        if self.pointing_address != 0:
            self.string = read_string_until_null(self.dol.data, self.pointing_address, "utf-8")
        else:
            self.string = None
    
    def write_string(self) -> None:
        wr_str(self.dol.data, self.string, len(self.string.encode("utf-8")),
            offset=self.pointing_address, str_fmt="utf-8", add_null_byte=True)

    def replace_prefix(self, new_prefix: str) -> None:
        self.string = new_prefix + self.string[len(new_prefix):]
        self.write_string()

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

    def __init__(self, dol: "SMGDOL"):
        self.dol = dol

        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

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

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_create_element: Name2CreateFuncElement = element

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

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_archive_element: Name2MakeArchiveListFuncElement = element

    def get_name_to_create_function_elements_by_name(self, name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.name_pointer.string == name]

    def get_name_to_create_function_elements_by_create_function(self, create_function_address: int) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.create_function_pointer.pointing_address == create_function_address]
    
    def get_name_to_create_function_elements_by_archive_name(self, archive_name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.archive_name_pointer.string == archive_name]

    def get_miniature_galaxy_name_to_make_archive_list_function_elements(self) -> list[Name2MakeArchiveListFuncElement]:
        return [element for element in self.name_to_make_archive_list_function_elements
                if element.name_pointer.string.startswith("Mini")][:-1]

    def set_miniature_galaxy_name_to_make_archive_list_function_elements(self, new_miniature_name_pointers: list[CharPointer]) -> None:
        archive_miniature_elements = self.get_miniature_galaxy_name_to_make_archive_list_function_elements()
        
        for archive_miniature_element, new_miniature_name_pointer in zip(archive_miniature_elements, new_miniature_name_pointers):
            archive_miniature_element.name_pointer.pointing_address = new_miniature_name_pointer.pointing_address
            archive_miniature_element.name_pointer.write_pointer()

    def set_miniature_galaxy_name_to_create_function_element(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Mini"
        element.name_pointer.replace_prefix("Mini")

        # Set the create function as the create miniature galaxy function
        element.create_function_pointer.write_function_address(self.miniature_function_address)
        
        # Empty the archive name
        element.archive_name_pointer.pointing_address = 0
        element.archive_name_pointer.write_pointer()

    def set_as_miniature_galaxies(self, miniature_elements: list[Name2CreateFuncElement]) -> None:
        self.set_miniature_galaxy_name_to_make_archive_list_function_elements([element.name_pointer for element in miniature_elements])

        for element in miniature_elements:
            self.set_miniature_galaxy_name_to_create_function_element(element)

    def set_name_to_create_function_element_as_surprised(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Surp"
        element.name_pointer.replace_prefix("Surp")

        # Set the create function as the create surprised galaxy function
        element.create_function_pointer.write_function_address(self.surprised_function_address)

        # Set the archive name to "MiniSurprisedGalaxy"
        element.archive_name_pointer.pointing_address = self.surprised_galaxy_string_address
        element.archive_name_pointer.write_pointer()

    def set_as_surprised_galaxies(self, surprised_elements: list[Name2CreateFuncElement]) -> None:
        for element in surprised_elements:
            self.set_name_to_create_function_element_as_surprised(element)

    def set_galaxies(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str]) -> None:
        # Get the elements in the array that should be converted to dome and luma galaxies
        to_miniature_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in miniature_galaxy_names]
        to_surprised_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in surprised_galaxy_names]

        if GATEWAY_IN_GAME in miniature_galaxy_names:
            self.extra_create_element.name_pointer.string = "Mini" + GATEWAY_IN_GAME
            self.extra_create_element.name_pointer.write_string()
            to_miniature_elements.append(self.extra_create_element)
        
        self.set_as_miniature_galaxies(to_miniature_elements)
        self.set_as_surprised_galaxies(to_surprised_elements)

    def swap_pointers(self, pointer1: Pointer, pointer2: Pointer) -> None:
        pointer1.swap_with_pointer(pointer2)

class GalaxyUnlockTableFieldNames(StrEnum):
    NAME = "name"
    MAP_PANE_NAME = "MapPaneName"
    OPEN_CONDITION0 = "OpenCondition0"
    OPEN_CONDITION1 = "OpenCondition1"
    OPEN_CONDITION2 = "OpenCondition2"
    POWER_STAR_REQUIREMENT = "PowerStarNum"
    RETURN_DOME = "GrandGalaxyNo"

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

class GalaxyUnlockTable:
    table: BCSV

    start_address: int
    end_address: int
    size: int

    entries: list[GalaxyUnlockTableEntry]

    def __init__(self, dol: DOL):
        self.start_address = GALAXY_UNLOCK_TABLE_START_ADDRESS
        self.end_address = GALAXY_UNLOCK_TABLE_END_ADDRESS
        self.size = self.end_address - self.start_address

        self.entries = []

        table_bytes: bytes = dol.read_at(self.start_address, self.size)
        self.table = BCSV.import_bcsv(BytesIO(table_bytes), field_names=hash_to_name, str_fmt="shift-jis")
        
        for entry_index in range(len(self.table.entries)):
            entry = self.get_entry(entry_index)

            # Set empty by default, to be overridden later
            entry.open_condition0 = ''
            entry.open_condition1 = ''
            entry.power_star_requirement = 0
            entry.return_dome = 0
            self.set_entry(entry)
            
            self.entries.append(entry)

    def get_entry(self, entry_index: int) -> GalaxyUnlockTableEntry:
        name = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.NAME]
        open_condition0 = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION0]
        open_condition1 = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION1]
        power_star_requirement = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT]
        return_dome = self.table.entries[entry_index][GalaxyUnlockTableFieldNames.RETURN_DOME]

        return GalaxyUnlockTableEntry(entry_index, name, open_condition0, open_condition1,
                                      power_star_requirement, return_dome)
    
    def set_entry(self, entry: GalaxyUnlockTableEntry) -> None:
        self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.NAME] = entry.name
        self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION0] = entry.open_condition0
        self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION1] = entry.open_condition1
        self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT] = entry.power_star_requirement
        self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.RETURN_DOME] = entry.return_dome

    def save_to_dol(self, dol: DOL, address: int) -> None:
        bcsv_bytes = self.table.export_bcsv(str_fmt="shift-jis")
        dol.write_at(address, bcsv_bytes.getvalue())

class AstroDomeModels:
    astro_dome: list[CharPointer]
    astro_dome_sky: list[CharPointer]
    astro_dome_entrance: list[CharPointer]
    astro_star_plate: list[CharPointer]

    def __init__(self, dol: "SMGDOL"):
        self.astro_dome_address: int = ASTRO_DOME_ARRAY_ADDRESS
        self.astro_dome_sky_address: int = ASTRO_DOME_SKY_ARRAY_ADDRESS
        self.astro_dome_entrance_address: int = ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS
        self.astro_star_plate_address: int = ASTRO_STAR_PLATE_ARRAY_ADDRESS

        self.astro_dome = []
        self.astro_dome_sky = []
        self.astro_dome_entrance = []
        self.astro_star_plate = []
        
        for index in range(6):
            astro_dome_pointer = CharPointer(dol, self.astro_dome_address + index * 0x4)
            astro_dome_sky_pointer = CharPointer(dol, self.astro_dome_sky_address + index * 0x4)
            astro_dome_entrance_pointer = CharPointer(dol, self.astro_dome_entrance_address + index * 0x4)
            astro_star_plate_pointer = CharPointer(dol, self.astro_star_plate_address + index * 0x4)

            self.astro_dome.append(astro_dome_pointer)
            self.astro_dome_sky.append(astro_dome_sky_pointer)
            self.astro_dome_entrance.append(astro_dome_entrance_pointer)
            self.astro_star_plate.append(astro_star_plate_pointer)
    
    def shuffle_list(self, pointer_list: list[CharPointer], shuffle: dict[int, int]):
        assert len(pointer_list) == 6
        
        reverse_shuffle: dict[int, int] = {value: key for key, value in shuffle.items()}
        addresses: list[int] = [pointer_list[i].pointing_address for i in range(6)]
        for index, address in enumerate(addresses):
            new_index = reverse_shuffle[index + 1] - 1
            pointer_list[new_index].pointing_address = address
            pointer_list[new_index].write_pointer()
    
    def shuffle(self, shuffle: dict[int, int]):
        #self.shuffle_list(self.astro_dome, shuffle)
        #self.shuffle_list(self.astro_dome_sky, shuffle)
        self.shuffle_list(self.astro_dome_entrance, shuffle)
        #self.shuffle_list(self.astro_dome, shuffle)

class SMGDOL:
    """Extends the gclib DOL class to be easily useable for Super Mario Galaxy."""
    name_object_factory: NameObjFactory
    galaxy_unlock_table: GalaxyUnlockTable
    data: BytesIO
    custom_section_size: int = 0x1000

    def __init__(self, patcher: WiiIsoPatcher):
        self.dol: DOL = patcher.read_dol()
        self.data = BytesIO(self.dol.to_bytes())

        self.name_object_factory = NameObjFactory(self)
        self.galaxy_unlock_table = GalaxyUnlockTable(self.dol)
        self.astro_dome_models = AstroDomeModels(self)

        self.dol.add_text_section(CUSTOM_SECTION_START, b"" * self.custom_section_size)

    def set_name_object_factory_galaxies(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str]) -> None:
        self.name_object_factory.set_galaxies(miniature_galaxy_names, surprised_galaxy_names)

    def get_galaxy_unlock_table_entry_by_name(self, name: str) -> GalaxyUnlockTableEntry | None:
        for entry in self.galaxy_unlock_table.entries:
            if entry.name == name:
                return entry

        print(f"Entry was not found in Unlock table: {name}")
        return None

    def add_deathlink(self):
        self.dol.write_at(0x804A16C0, b'\x38\x63\xef\x90')
        self.dol.write_at(0x804AAC98, b'\x38\xa5\xef\x90')

        # Return
        instructions = b'\x39\x61\x01\x00\x4b\xe6\x85\xcd\x80\x01\x01\x04\x7c\x08\x03\xa6\x38\x21\x01\x00\x4e\x80\x00\x20'
        address: int = (CUSTOM_SECTION_START + self.custom_section_size) - len(instructions)
        self.dol.write_at(address, instructions)

        # Setup
        instructions = b'\x94\x21\xff\x00\x7c\x08\x02\xa6\x90\x01\x01\x04\x39\x61\x01\x00\x4b\xe6\x95\x5d\x4b\xce\xbb\x4d'
        self.dol.write_at(CUSTOM_SECTION_START, instructions)

        # Set 0x8000 into higher bits of r3
        # Load byte from 0x80001af0 into r3
        # Compare 0x80001af0 with 0
        # Jump over if its not 0
        # Jump to forceKillPlayerByAbyss
        # Set 0 into r3
        # Store byte from r3 (0) into 0x80001af0 and reset it
        address = CUSTOM_SECTION_START + len(instructions) # Previous Instructions first
        instructions = b'\x3f\xe0\x80\x00\x88\x7f\x1a\xf0\x2c\x03\x00\x00\x41\x82\x00\x10\x4b\xd4\x3e\xbd\x38\x60\x00\x00\x98\x7f\x1a\xf0'
        self.dol.write_at(address, instructions)

    def save(self):
        self.add_deathlink()
        self.dol.write_at(self.galaxy_unlock_table.start_address, b'\x00' * self.galaxy_unlock_table.size)
        self.galaxy_unlock_table.save_to_dol(self.dol, self.galaxy_unlock_table.start_address)
