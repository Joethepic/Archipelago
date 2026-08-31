from worlds.smgalaxy.Patch.extensions import SMGDOLObject, CharPointer, FunctionPointer
from ...Constants.patch_constants import *


class Name2CreateFuncElement:
    name: CharPointer
    create_func: FunctionPointer
    archive_name: CharPointer

    def __init__(self, name_pointer: CharPointer, create_function_pointer: FunctionPointer,
                 archive_name_pointer: CharPointer):
        self.name = name_pointer
        self.create_func = create_function_pointer
        self.archive_name = archive_name_pointer


class Name2CreateFuncManager:
    create_funcs: list[Name2CreateFuncElement]

    def __init__(self):
        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

        start_address = NAME_TO_CREATE_FUNCTION_START_ADDRESS
        element_count = NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE

        self.create_funcs = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_addr = offset + 0x0
            create_func_addr = offset + 0x4
            archive_name_addr = offset + 0x8

            name: CharPointer = CharPointer(name_addr)
            create_func: FunctionPointer = FunctionPointer(create_func_addr)
            archive_name: CharPointer = CharPointer(archive_name_addr)
            element: Name2CreateFuncElement = Name2CreateFuncElement(name, create_func, archive_name)
            self.create_funcs.append(element)

            if name.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_create_element: Name2CreateFuncElement = element


    def get_create_funcs_by_name(self, name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.create_funcs if element.name.string == name]

    def get_create_funcs_by_func(self, create_func: int) -> list[Name2CreateFuncElement]:
        return [element for element in self.create_funcs if element.create_func.pointing_address == create_func]

    def get_create_funcs_by_arch_name(self, archive_name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.create_funcs if element.archive_name.string == archive_name]


    def set_galaxies(self, surp_galaxies: list[Name2CreateFuncElement], mini_galaxies: list[Name2CreateFuncElement]) -> None:
        for element in surp_galaxies:
            self.set_surp_name(element)

        for element in mini_galaxies:
            self.set_mini_name(element)


    def set_mini_name(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Mini"
        element.name.replace_prefix("Mini")

        # Set the create function as the create miniature galaxy function
        element.create_func.write_function_address(self.miniature_function_address)

        # Empty the archive name
        element.archive_name.pointing_address = 0
        element.archive_name.write_pointer()

    def set_surp_name(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Surp"
        element.name.replace_prefix("Surp")

        # Set the create function as the create surprised galaxy function
        element.create_func.write_function_address(self.surprised_function_address)

        # Set the archive name to "MiniSurprisedGalaxy"
        element.archive_name.pointing_address = self.surprised_galaxy_string_address
        element.archive_name.write_pointer()


class Name2ArchiveElement:
    """
    Object Name -> Archive Name, which basically switches the pointers to load different file instead.
    """
    object_name_pointer: CharPointer
    archive_name_pointer: CharPointer

    def __init__(self, object_name_pointer: CharPointer, archive_name_pointer: CharPointer):
        self.object_name_pointer = object_name_pointer
        self.archive_name_pointer = archive_name_pointer


class Name2ArchiveManager:
    archive_elems: list[Name2ArchiveElement]

    def __init__(self):
        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

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


class Name2MakeArchiveListFuncElement:
    """
    Name -> Archive function, which specifies what to do with a file archive once its found.
    """
    name_pointer: CharPointer
    archive_function_pointer: FunctionPointer

    def __init__(self, name_pointer: CharPointer, archive_function_pointer: FunctionPointer):
        self.name_pointer = name_pointer
        self.archive_function_pointer = archive_function_pointer


class Name2MakeArchiveListFuncManager:
    archive_elems: list[Name2MakeArchiveListFuncElement]

    def __init__(self):
        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

        start_address = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS
        element_count = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE

        self.archive_elems = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_address = offset + 0x0
            archive_function_address = offset + 0x4

            name_pointer: CharPointer = CharPointer(name_address)
            archive_function_pointer: FunctionPointer = FunctionPointer(archive_function_address)

            element: Name2MakeArchiveListFuncElement = Name2MakeArchiveListFuncElement(name_pointer,
                                                                                       archive_function_pointer)

            self.archive_elems.append(element)

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_archive_element: Name2MakeArchiveListFuncElement = element


    def set_mini_archive_func(self, new_miniature_names: list[CharPointer]) -> None:
        print([name.string for name in new_miniature_names])
        archive_elems: list[Name2MakeArchiveListFuncElement] = []

        for element in self.archive_elems:
            if element.name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                continue

            if element.name_pointer.string.startswith("Mini"):
                archive_elems.append(element)

        for archive_miniature_element, new_miniature_name_pointer in zip(archive_elems, new_miniature_names):
            archive_miniature_element.name_pointer.pointing_address = new_miniature_name_pointer.pointing_address
            archive_miniature_element.name_pointer.write_pointer()


class NameObjFactory(SMGDOLObject):
    create_mgr: Name2CreateFuncManager
    archive_obj_mgr: Name2ArchiveManager
    archive_func_mgr: Name2MakeArchiveListFuncManager

    def __init__(self):
        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

        self.create_mgr = Name2CreateFuncManager()
        self.archive_obj_mgr = Name2ArchiveManager()
        self.archive_func_mgr = Name2MakeArchiveListFuncManager()

    def update(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str], **kwargs) -> None:
        # Get the elements in the array that should be converted to dome and luma galaxies
        to_miniature_elements: list[Name2CreateFuncElement] = [element for element in
            self.create_mgr.create_funcs if element.name.string[4:] in miniature_galaxy_names]

        to_surprised_elements: list[Name2CreateFuncElement] = [element for element in
            self.create_mgr.create_funcs if element.name.string[4:] in surprised_galaxy_names]

        if GATEWAY_IN_GAME in miniature_galaxy_names:
            self.create_mgr.extra_create_element.name.string = "Mini" + GATEWAY_IN_GAME
            self.create_mgr.extra_create_element.name.write_string()
            to_miniature_elements.append(self.create_mgr.extra_create_element)

        if GATEWAY_IN_GAME in surprised_galaxy_names:
            self.create_mgr.extra_create_element.name.string = "Surp" + GATEWAY_IN_GAME
            self.create_mgr.extra_create_element.name.write_string()
            to_surprised_elements.append(self.create_mgr.extra_create_element)

        self.create_mgr.set_galaxies(to_surprised_elements, to_miniature_elements)

        self.archive_func_mgr.set_mini_archive_func([element.name for element in to_miniature_elements])
