from io import BytesIO

from gclib.yaz0_yay0 import Yaz0

from wiithon.formats.rarc import Rarc

from ..extensions import SMGObject
from ...Constants.patch_constants import *

class PowerStar(SMGObject):
    arc_file: Rarc

    def __init__(self):
        super().__init__(POWER_STAR_PATH)

        compressed_bytes: BytesIO = BytesIO(self.patcher.read_file(self.path))
        self.arc_file: Rarc = Rarc.read(Yaz0.decompress(compressed_bytes))

    def update(self, **kwargs):
        arc_bytes: BytesIO = BytesIO()
        self.arc_file.write(arc_bytes)
        self.patcher.replace_file(self.path, Yaz0.compress(arc_bytes).getvalue())
