from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
from bcsv import BCSV
from io import BytesIO
import gclib.fs_helpers as fs


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

class SMGDOL(DOLExtended):
    """Extends the gclib DOL class to be easily useable for Super Mario Galaxy"""
    path = "/DATA/sys/main.dol"

    nameobjfactory_address = 0x80533980
    nameobjfactory_element_count = 1183
    nameobjfactory_element_size = 0xc

    archivelist_address = 0x80537eb4
    archivelist_element_count = 91
    archivelist_element_size = 0x8

        
    unlabeled_table_start_address = 0x8053c800
    unlabeled_table_end_address = 0x8053d520
    unlabeled_table_size = unlabeled_table_end_address - unlabeled_table_start_address
    
    def __init__(self, base_path):
        self.file_path = base_path + self.path
        super().__init__(self.file_path)
        
        self.unlabeled_table_bytes = self.read_data(fs.read_bytes, self.unlabeled_table_start_address, self.unlabeled_table_size)
        self.unlabeled_table = BCSV(self.unlabeled_table_bytes)

    def get_nameobjfactory_element(self, index: int) -> dict:
        if index < 0 or index >= self.nameobjfactory_element_count:
            raise ValueError(f"Index is out of range: {index}")
        
        offset = self.nameobjfactory_address + self.nameobjfactory_element_size * index
        name_pointer, create_pointer, archive_pointer = self.read_data(fs.read_and_unpack_bytes, offset,
                                                                       self.nameobjfactory_element_size, ">III")

        name = self.read_data(fs.read_str_until_null_character, name_pointer)
        if archive_pointer != 0:
            archive_name = self.read_data(fs.read_str_until_null_character, archive_pointer)
        else:
            archive_name = ''

        return {"Name Pointer": name_pointer,
                "Name": name,
                "Create Function": create_pointer,
                "Archive Pointer": archive_pointer,
                "Archive Name": archive_name}

    def get_archivelist_element(self, index: int) -> dict:
        if index < 0 or index >= self.archivelist_element_count:
            raise ValueError(f"Index is out of range: {index}")

        offset = self.archivelist_address + self.archivelist_element_size * index
        name_pointer, make_archivelist_pointer = self.read_data(fs.read_and_unpack_bytes, offset,
                                                                self.archivelist_element_size, ">II")
        
        name = self.read_data(fs.read_str_until_null_character, name_pointer)

        return {"Name Pointer": name_pointer,
                "Name": name,
                "Make Archivelist Pointer": make_archivelist_pointer}
    
    def save(self):
        self.unlabeled_table.save_changes()
        self.write_data(fs.write_bytes, self.unlabeled_table_start_address, self.unlabeled_table.data)
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
