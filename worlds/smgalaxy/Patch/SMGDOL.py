from typing import Self
from io import BytesIO

from wiithon.ppc import instructions as PPC
from wiithon.formats.dol import DOL
from wiithon.formats.bcsv import BCSV

from worlds.smgalaxy.Patch.extensions import SMGObject, SMGDOLObject

from .hashtable import hash_to_name
from ..Constants.patch_constants import *

class Pointer:
    dol: DOL
    base_address: int
    pointing_address: int
    
    def __init__(self, base_address: int):
        self.base_address = base_address
        self.read_pointer()

    def read_pointer(self):
        self.pointing_address = int.from_bytes(self.dol.read_at(self.base_address, 4))
    
    def write_pointer(self):
        self.dol.write_at(self.base_address, int.to_bytes(self.pointing_address, 4, "big"))

class CharPointer(Pointer):
    string: str | None

    def read_pointer(self):
        super().read_pointer()

        if self.pointing_address == 0:
            self.string = None
            return

        raw = self.dol.read_until_null_at(self.pointing_address)
        self.string = raw.decode("shift-jis")
    
    def write_string(self) -> None:
        self.dol.write_at(self.pointing_address, self.string.encode("shift-jis") + b'\0')

    def replace_prefix(self, new_prefix: str) -> None:
        prefix_size = len(new_prefix)

        if prefix_size > len(self.string):
            raise ValueError(f"New prefix is larger than the string.\nPrefix: {new_prefix}, string: {self.string}")
        
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
    archive_function_pointer: FunctionPointer

    def __init__(self, name_pointer: CharPointer, archive_function_pointer: FunctionPointer):
        self.name_pointer = name_pointer
        self.archive_function_pointer = archive_function_pointer

class NameObjFactory(SMGDOLObject):
    name_to_create_function_elements: list[Name2CreateFuncElement]
    name_to_archive_elements: list[Name2ArchiveElement]
    name_to_make_archive_list_function_elements: list[Name2MakeArchiveListFuncElement]

    def __init__(self):
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

            name_pointer: CharPointer = CharPointer(name_address)
            create_function_pointer: FunctionPointer = FunctionPointer(create_function_address)
            archive_name_pointer: CharPointer = CharPointer(archive_name_address)

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

            object_name_pointer: CharPointer = CharPointer(object_name_address)
            archive_name_pointer: CharPointer = CharPointer(archive_name_address)

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

            name_pointer: CharPointer = CharPointer(name_address)
            archive_function_pointer: FunctionPointer = FunctionPointer(archive_function_address)

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

    def set_miniature_galaxy_name_to_make_archive_list_function_elements(self, new_miniature_name_pointers: list[CharPointer]) -> None:
        archive_miniature_elements: list[Name2MakeArchiveListFuncElement] = []

        for element in self.name_to_make_archive_list_function_elements:
            if element.name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                continue

            if element.name_pointer.string.startswith("Mini"):
                archive_miniature_elements.append(element)
        
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

    def update(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str], **kwargs) -> None:
        # Get the elements in the array that should be converted to dome and luma galaxies
        to_miniature_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in miniature_galaxy_names]
        to_surprised_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in surprised_galaxy_names]

        if GATEWAY_IN_GAME in miniature_galaxy_names:
            self.extra_create_element.name_pointer.string = "Mini" + GATEWAY_IN_GAME
            self.extra_create_element.name_pointer.write_string()
            to_miniature_elements.append(self.extra_create_element)

        if GATEWAY_IN_GAME in surprised_galaxy_names:
            self.extra_create_element.name_pointer.string = "Surp" + GATEWAY_IN_GAME
            self.extra_create_element.name_pointer.write_string()
            to_surprised_elements.append(self.extra_create_element)
        
        self.set_as_miniature_galaxies(to_miniature_elements)
        self.set_as_surprised_galaxies(to_surprised_elements)

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
            entry = GalaxyUnlockTableEntry(entry_index, name, '', '' , 0, 0)
            self.entries.append(entry)

    def set_new_entry_values(self, name: str, star_requirement: int, dome_index: int) -> None:
        for entry in self.entries:
            if entry.name != name:
                continue

            entry.power_star_requirement = star_requirement
            entry.return_dome = dome_index

    def update(self, dome_galaxies: list[GalaxyDestination], star_requirements: dict[str, int], **kwargs) -> None:
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1,7)}
                
        for location, requirement in star_requirements.items():
            dome_index = int(location[1])
            orbit_index = int(location[3:])

            requirements[dome_index][orbit_index] = requirement
        
        for galaxy in dome_galaxies:
            star_requirement: int = requirements[galaxy.dome_index][galaxy.orbit_index + 1]

            self.set_new_entry_values(galaxy.name, star_requirement, dome_index)
            
        for entry in self.entries:
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.NAME] = entry.name
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION0] = entry.open_condition0
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.OPEN_CONDITION1] = entry.open_condition1
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT] = entry.power_star_requirement
            self.table.entries[entry.entry_index][GalaxyUnlockTableFieldNames.RETURN_DOME] = entry.return_dome

        bcsv_bytes = self.table.export_bcsv(str_fmt="shift-jis")

        if bcsv_bytes.seek(2, 0) > self.size:
            raise ValueError(f"New embedded BCSV is bigger than the original BCSV.\nNew size: {bcsv_bytes.seek(2, 0)}, old size: {self.size}")

        self.dol.write_at(self.start_address, bcsv_bytes.getvalue())

class AstroDomeModels(SMGDOLObject):
    astro_dome: list[CharPointer]
    astro_dome_sky: list[CharPointer]
    astro_dome_entrance: list[CharPointer]
    astro_star_plate: list[CharPointer]

    def __init__(self):
        self.astro_dome_address: int = ASTRO_DOME_ARRAY_ADDRESS
        self.astro_dome_sky_address: int = ASTRO_DOME_SKY_ARRAY_ADDRESS
        self.astro_dome_entrance_address: int = ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS
        self.astro_star_plate_address: int = ASTRO_STAR_PLATE_ARRAY_ADDRESS

        self.astro_dome = []
        self.astro_dome_sky = []
        self.astro_dome_entrance = []
        self.astro_star_plate = []
        
        for index in range(6):
            offset = index * 0x4
            astro_dome_pointer = CharPointer(self.astro_dome_address + offset)
            astro_dome_sky_pointer = CharPointer(self.astro_dome_sky_address + offset)
            astro_dome_entrance_pointer = CharPointer(self.astro_dome_entrance_address + offset)
            astro_star_plate_pointer = CharPointer(self.astro_star_plate_address + offset)

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
    
    def update(self, dome_shuffle: dict[int, int], **kwargs):
        #self.shuffle_list(self.astro_dome, shuffle)
        #self.shuffle_list(self.astro_dome_sky, shuffle)
        self.shuffle_list(self.astro_dome_entrance, dome_shuffle)
        #self.shuffle_list(self.astro_dome, shuffle)

class SMGDOL(SMGObject):
    data: BytesIO
    custom_section_size: int = 0x1000
    custom_section_address: int

    objects: dict[str, SMGDOLObject]

    write_pointer: int

    def __init__(self, dol: DOL):
        self.dol: DOL = dol
        self.data = BytesIO(self.dol.to_bytes())

        Pointer.dol = self.dol
        SMGDOLObject.dol = self.dol

        self.objects = {
            "NameObjectFactory": NameObjFactory(),
            "GalaxyUnlockTable": GalaxyUnlockTable(),
            #"AstroDomeModels": AstroDomeModels()
        }

        self.write_pointer = 0

        size, addrs = self.dol.inject_above_arena([PPC.nop() * int(self.custom_section_size/4)])
        self.custom_section_address = addrs[0]

        # Return custom function
        self.write_pointer = self.custom_section_address + self.custom_section_size - 5 * 0x4
        self.write_instruction(PPC.bl(0x80517548, self.write_pointer))
        self.write_instruction(PPC.lwz(0, 0x104, 1))
        self.write_instruction(PPC.mtlr(0))
        self.write_instruction(PPC.addi(1, 1, 0x100))
        self.write_instruction(PPC.blr())

        # Setup custom function
        self.write_instruction(PPC.stwu(1, -0x100, 1), self.custom_section_address)
        self.write_instruction(PPC.mflr(0))
        self.write_instruction(PPC.stw(0, 0x104, 1))
        self.write_instruction(PPC.bl(0x805174fc, self.write_pointer))
        self.write_instruction(PPC.bl(0x80399af0, self.write_pointer))

    def write_instruction(self, instruction_bytes: bytes, address: int = None) -> None:
        if address is not None:
            self.write_pointer = address

        self.dol.write_at(self.write_pointer, instruction_bytes)
        self.write_pointer += 4

    def write_nop(self, count: int) -> None:
        for _ in range(count):
            self.write_instruction(PPC.nop())

    def add_deathlink(self):
        # Set 0x8000 into higher bits of r3
        # Load byte from 0x80001af0 into r3
        # Compare 0x80001af0 with 0
        # Jump over if its not 0
        # Jump to forceKillPlayerByAbyss
        # Set 0 into r3

        self.write_instruction(PPC.lis(31, -0x8000))
        self.write_instruction(PPC.lbz(3, 0x1AF0, 31))
        self.write_instruction(PPC.cmpi(0, 3, 0))
        self.write_instruction(PPC.bc(4, 0, self.write_pointer + 4 * 0x4, self.write_pointer))
        self.write_instruction(PPC.bl(0x803f1e74, self.write_pointer))
        self.write_instruction(PPC.li(3, 0))
        self.write_instruction(PPC.stb(3, 0x1AF0, 31))

    def skip_opening(self):
        #######################################################
        # Skip opening cutscene and go immediately to gateway #
        #######################################################
        self.write_instruction(PPC.li(3, 0), 0x803bb3cc)
        self.write_instruction(PPC.addi(3, 31, 0x3F8), 0x803bb3d8)
        self.write_instruction(PPC.li(0, 4))

    def set_swing_permission(self):
        ########################
        # Set swing permission #
        ########################
        self.write_instruction(PPC.li(3, 1), 0x803b55b0)

    def manipulate_miniature_orbit(self):
        #######################################
        # Miniature galaxy orbit manipulation #
        #######################################
        # Get obj_arg0 from miniature galaxy
        self.write_instruction(PPC.lwz(3, 0x8C, 31), 0x80200758)
        self.write_instruction(PPC.rlwnm(3, 3, 0x10, 0x10, 0x1F))

    def manipulate_star_loading(self):
        ################################
        # Scenario select star loading #
        ################################
        # Keep loading regular stars even if they're not available yet
        self.write_instruction(PPC.li(3, 1), 0x8037d9ec)

        # Calculate all secret/comet stars, including possibly normally unavailable ones
        self.write_instruction(PPC.li(3, 1), 0x8037da44)

        # Show secret/comet stars as calculated above
        self.write_instruction(PPC.li(3, 1), 0x8037db54)

        # Set visibility to 1 (not collected) if appearing as collected has failed (ensuring it shows up even if not available)
        self.write_instruction(PPC.li(6, 1), 0x8037db18)

        # Always show up and appear correctly as collected/not collected
        self.write_instruction(PPC.li(6, 1), 0x8037db74)

    def read_star_count(self):
        #######################################
        # Read star count from memory address #
        #######################################
        # Load upper 2 bytes of memory pointer (0x8000)
        self.write_instruction(PPC.lis(3, -0x8000), 0x803b10fc)

        # Load lower 2 bytes of memory pointer (0x1880), and load the byte at 0x80001880 into r3
        self.write_instruction(PPC.lwz(3, 0x1880, 3))

        # Skip the rest of the normal function
        self.write_instruction(PPC.b(0x803b113c, self.write_pointer))

    def custom_powerstar_colour_loading(self):
        ###################################
        # Custom powerstar colour loading #
        ###################################
        self.write_instruction(PPC.mr(31, 3), 0x8020f270)
        self.write_instruction(PPC.bl(0x803f5ab8, self.write_pointer))
        self.write_instruction(PPC.mr(4, 3))
        self.write_instruction(PPC.bl(0x803b0544, self.write_pointer))
        self.write_instruction(PPC.lwz(3, 0xC, 3))
        self.write_instruction(PPC.bl(0x803b1390, self.write_pointer))
        self.write_instruction(PPC.lis(4, -0x8000))
        self.write_instruction(PPC.ori(4, 4, 0x18FF))
        self.write_instruction(PPC.mulli(3, 3, 0x8))
        self.write_instruction(PPC.add(3, 3, 4))
        self.write_instruction(PPC.lbzx(3, 3, 31))
        self.write_nop(1)

    def custom_grandstar_count(self):
        ##################################
        # Custom grandstar count loading #
        ##################################
        self.write_instruction(PPC.lis(3, -0x8000), 0x803b1d10)
        self.write_instruction(PPC.lbz(3, 0x1882, 3))
        self.write_instruction(PPC.addi(3, 3, 1))
        self.write_instruction(PPC.cmp(0, 3, 4))
        self.write_instruction(PPC.bc(12, 0, self.write_pointer + 3 * 0x4, self.write_pointer))
        self.write_instruction(PPC.li(3, 1))
        self.write_instruction(PPC.b(self.write_pointer + 2 * 0x4, self.write_pointer))
        self.write_instruction(PPC.li(3, 0))
        self.write_nop(5)

    def skip_wii_strap(self):
        #########################
        # Skip wii strap screen #
        #########################
        self.write_instruction(PPC.addi(4, 13, -0x3080), 0x80340408)
        self.write_instruction(PPC.li(4, 1), 0x803406ac)
        self.write_instruction(PPC.li(4, 2), 0x803406d0)

    def show_bros_button(self):
        #################################################
        # Show the bros button to select Mario or Luigi #
        #################################################
        self.write_instruction(PPC.li(3, 1), 0x8017cd70)

    def hook_to_custom_function(self):
        ####################
        # Custom Functions #
        ####################
        # Jump to custom section
        self.write_pointer = 0x803995c0
        self.write_instruction(PPC.b(self.custom_section_address, self.write_pointer))

    def update_instructions(self):
        self.skip_opening()
        self.set_swing_permission()
        self.manipulate_miniature_orbit()
        self.manipulate_star_loading()
        self.read_star_count()
        self.custom_powerstar_colour_loading()

        #self.custom_grandstar_count()

        self.skip_wii_strap()
        self.show_bros_button()
        self.hook_to_custom_function()

    def update(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination], dome_shuffle: dict[int, int], star_requirements: dict[str, int]):
        for object_name, object in self.objects.items():
            print(f"Updating {object_name}")

            object.update(miniature_galaxy_names=[galaxy.name for galaxy in dome_galaxies],
                          surprised_galaxy_names=[galaxy.name for galaxy in luma_galaxies],
                          dome_shuffle=dome_shuffle,
                          dome_galaxies=dome_galaxies,
                          star_requirements=star_requirements)

        self.add_deathlink()

        self.update_instructions()
