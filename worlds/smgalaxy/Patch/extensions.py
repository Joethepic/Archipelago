from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
from io import BytesIO

class DOLExtended(DOL):
    """To read data, call self.read_data and use the corresponding fs_helper function as read_callback"""
    # Path to be set before calling classes that inherit from this class
    iso_base_path = ''

    # Path to be set in each class that inherits this class
    relative_path = ''

    def __init__(self):
        if self.iso_base_path is '' or self.relative_path is '':
            raise ValueError(f"ISO path and relative path must not be empty. \
                             \nISO path: {self.iso_base_path}\nRelative path: {self.relative_path}")
        
        self.absolute_file_path = self.iso_base_path + self.relative_path
        super().__init__()
        
        with open(self.absolute_file_path, 'rb') as file:
            data = BytesIO(file.read())
            self.read(data)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.absolute_file_path, 'wb') as f:
            f.write(self.data.getvalue())

class RARCExtended(RARC):
    """Extends the functionality of the gclib RARC class. Is meant as a base class for other classes to inherit from.
    Assumes the file path is an absolute path to the .arc file and uses that to write it back when saving.
    Set iso_path before instantiating inheriting classes.
    Set relative_path before initialising inheriting class instance"""
    # Path to be set before calling classes that inherit from this class
    iso_base_path = ''

    # Path to be set in each class that inherits this class
    relative_path = ''

    def __init__(self):
        if self.iso_base_path is '' or self.relative_path is '':
            raise ValueError(f"ISO path and relative path must not be empty. \
                             \nISO path: {self.iso_base_path}\nRelative path: {self.relative_path}")
        
        self.absolute_file_path = self.iso_base_path + self.relative_path
        super().__init__(self.absolute_file_path)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.absolute_file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
    
    def save_to_new_file(self, new_file_path: str) -> None:
        self.save_changes()

        with open(new_file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())