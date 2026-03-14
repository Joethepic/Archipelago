from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
from .bcsv import BCSV
from io import BytesIO
import gclib.fs_helpers as fs
from typing import NamedTuple

class DOLExtended(DOL):
    """To read data, call self.read_data and use the corresponding fs_helper function as read_callback"""
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__()
        
        with open(file_path, 'rb') as file:
            data = BytesIO(file.read())
            self.read(data)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.file_path, 'wb') as f:
            f.write(self.data.getvalue())


class NameObjFactoryElement(NamedTuple):
    name: str
    name_pointer: int
    create_pointer: int
    archive_name: str
    archive_pointer: int
    index: int


class ArchiveListElement(NamedTuple):
    name: str
    name_pointer: int
    make_archivelist_pointer: int
    index: int

class SMGDOL(DOLExtended):
    """Extends the gclib DOL class to be easily useable for Super Mario Galaxy"""
    path = "/DATA/sys/main.dol"

    nameobjfactory_address = 0x80533980
    nameobjfactory_element_count = 1183
    nameobjfactory_element_size = 0xc
    
    miniatures_nameobjfactory_start = 0x80536e30
    miniatures_nameobjfactory_count = 42

    archivelist_address = 0x80537eb4
    archivelist_element_count = 91
    archivelist_element_size = 0x8

    unlabeled_table_start_address = 0x8053c800
    unlabeled_table_end_address = 0x8053d520
    unlabeled_table_size = unlabeled_table_end_address - unlabeled_table_start_address

    create_nameobj_miniature_galaxy_function = 0x8026a8cc
    make_archivelist_miniature_galaxy_function = 0x801feea8

    def __init__(self, base_path):
        self.file_path = base_path + self.path
        super().__init__(self.file_path)
        
        self.unlabeled_table_bytes = self.read_data(fs.read_bytes, self.unlabeled_table_start_address, self.unlabeled_table_size)
        self.unlabeled_table = BCSV(BytesIO(self.unlabeled_table_bytes))

    def get_nameobjfactory_offset(self, index: int):
        return self.nameobjfactory_address + self.nameobjfactory_element_size * index

    def get_nameobjfactory_element(self, index: int) -> NameObjFactoryElement:
        if index < 0 or index >= self.nameobjfactory_element_count:
            raise ValueError(f"Index is out of range: {index}")
        
        offset = self.get_nameobjfactory_offset(index)
        name_pointer, create_pointer, archive_pointer = self.read_data(fs.read_and_unpack_bytes, offset,
                                                                       self.nameobjfactory_element_size, ">III")

        name = self.read_data(fs.read_str_until_null_character, name_pointer)
        if archive_pointer != 0:
            archive_name = self.read_data(fs.read_str_until_null_character, archive_pointer)
        else:
            archive_name = ''

        return NameObjFactoryElement(name, name_pointer, create_pointer, archive_name, archive_pointer, index)

    def get_nameobjfactory_elements(self) -> list[NameObjFactoryElement]:
        nameobjfactory = []
        for index in range(self.nameobjfactory_element_count):
            nameobjfactory.append(self.get_nameobjfactory_element(index))
        
        return nameobjfactory

    def set_nameobjfactory_element(self, element: NameObjFactoryElement):
        offset = self.get_nameobjfactory_offset(element.index)
        self.write_data(fs.write_and_pack_bytes, offset,
                        [element.name_pointer, element.create_pointer, element.archive_pointer], ">III")

    def get_archivelist_offset(self, index: int):
        return self.archivelist_address + self.archivelist_element_size * index

    def get_archivelist_element(self, index: int) -> ArchiveListElement:
        if index < 0 or index >= self.archivelist_element_count:
            raise ValueError(f"Index is out of range: {index}")

        offset = self.get_archivelist_offset(index)
        name_pointer, make_archivelist_pointer = self.read_data(fs.read_and_unpack_bytes, offset,
                                                                self.archivelist_element_size, ">II")
        
        name = self.read_data(fs.read_str_until_null_character, name_pointer)

        return ArchiveListElement(name, name_pointer, make_archivelist_pointer, index)

    def get_archivelist_elements(self) -> list[ArchiveListElement]:
        archivelist = []
        for index in range(self.archivelist_element_count):
            archivelist.append(self.get_archivelist_element(index))
        
        return archivelist

    def set_archivelist_element(self, element: ArchiveListElement):
        offset = self.get_archivelist_offset(element.index)
        self.write_data(fs.write_and_pack_bytes, offset,
                        [element.name_pointer, element.make_archivelist_pointer], ">II")

    def save(self):
        self.unlabeled_table.save_changes()
        #self.write_data(fs.write_bytes, self.unlabeled_table_start_address, self.unlabeled_table.data.getvalue())
        self.save_changes()

        with open(self.file_path, 'wb') as f:
            f.write(self.data.getvalue())

class RARCExtended(RARC):
    """Extends the functionality of the gclib RARC class"""
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(self.file_path)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
