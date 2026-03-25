from ..extensions import RARCExtended

GATEWAY_RELATIVE_PATH = "/DATA/files/ObjectData/AstroChildRoom.arc"

class Gateway(RARCExtended):
    bdl_base_name = "astrochildroom.bdl"

    def __init__(self):
        self.relative_path = GATEWAY_RELATIVE_PATH
        super().__init__()

    def get_bdl_entry(self):
        return self.get_file_entry(self.bdl_base_name)
    
    def create_miniature(self):
        pass