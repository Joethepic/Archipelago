from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
from io import BytesIO

class DOLExtended(DOL):
    """To read data, call self.read_data and use the corresponding fs_helper function as read_callback"""
    path = "/DATA/sys/main.dol"

    def __init__(self, base_path):
        super().__init__()
        self.file_path = base_path + self.path
        with open(self.file_path, 'rb') as file:
            data = BytesIO(file.read())
            self.read(data)
    
    def save(self):
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.file_path, 'wb') as f:
            f.write(self.data.getvalue())

class RARCExtended(RARC):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(self.file_path)

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
