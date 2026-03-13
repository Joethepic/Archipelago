from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0

class DOLExtended(DOL):
    """To read data, call self.read_data and use the corresponding fs_helper function as read_callback"""
    path = "DATA/sys/main.dol"

    def __init__(self, base_path):
        super().__init__(self)
        self.file_path = base_path + self.path
        self.file = open(self.file_path, 'rb+')
        self.read(self.file)


class RARCExtended(RARC):
    def __init__(self, filepath):
        self.filepath = filepath
        super().__init__(filepath)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.filepath, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
