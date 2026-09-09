from io import BytesIO

from wiithon.formats.rarc import Rarc
from wiithon.formats.yaz0 import Yaz0

from ..extensions import SMGObject
from ...Constants.patch_constants import *

class PowerStar(SMGObject):
    arc_file: Rarc

    def __init__(self):
        super().__init__(POWER_STAR_PATH)

        compressed_bytes = self.patcher.read_file(self.path)
        uncompressed_bytes = Yaz0.read(BytesIO(compressed_bytes)).data
        self.arc_file = Rarc.read(BytesIO(uncompressed_bytes))

    def update(self, **kwargs):
        self.patcher.replace_file(self.path, self.arc_file.get_bytes())
