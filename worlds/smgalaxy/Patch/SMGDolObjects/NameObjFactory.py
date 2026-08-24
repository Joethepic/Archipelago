from worlds.smgalaxy.Patch.extensions import SMGDOLObject, CharPointer, FunctionPointer
from ...Constants.patch_constants import *


class Name2CreateFuncElement:
    name_pointer: CharPointer
    create_function_pointer: FunctionPointer
    archive_name_pointer: CharPointer

    def __init__(self, name_pointer: CharPointer, create_function_pointer: FunctionPointer,
                 archive_name_pointer: CharPointer):
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

            element: Name2CreateFuncElement = Name2CreateFuncElement(name_pointer, create_function_pointer,
                                                                     archive_name_pointer)

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

            element: Name2MakeArchiveListFuncElement = Name2MakeArchiveListFuncElement(name_pointer,
                                                                                       archive_function_pointer)

            self.name_to_make_archive_list_function_elements.append(element)

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_archive_element: Name2MakeArchiveListFuncElement = element

    def get_name_to_create_function_elements_by_name(self, name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.name_pointer.string == name]

    def get_name_to_create_function_elements_by_create_function(self, create_function_address: int) -> list[
        Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.create_function_pointer.pointing_address == create_function_address]

    def get_name_to_create_function_elements_by_archive_name(self, archive_name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.archive_name_pointer.string == archive_name]

    def set_miniature_galaxy_name_to_make_archive_list_function_elements(self, new_miniature_name_pointers: list[
        CharPointer]) -> None:
        archive_miniature_elements: list[Name2MakeArchiveListFuncElement] = []

        for element in self.name_to_make_archive_list_function_elements:
            if element.name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                continue

            if element.name_pointer.string.startswith("Mini"):
                archive_miniature_elements.append(element)

        for archive_miniature_element, new_miniature_name_pointer in zip(archive_miniature_elements,
                                                                         new_miniature_name_pointers):
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
        self.set_miniature_galaxy_name_to_make_archive_list_function_elements(
            [element.name_pointer for element in miniature_elements])

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
        to_miniature_elements: list[Name2CreateFuncElement] = [element for element in
                                                               self.name_to_create_function_elements
                                                               if element.name_pointer.string[
                                                                   4:] in miniature_galaxy_names]
        to_surprised_elements: list[Name2CreateFuncElement] = [element for element in
                                                               self.name_to_create_function_elements
                                                               if element.name_pointer.string[
                                                                   4:] in surprised_galaxy_names]

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