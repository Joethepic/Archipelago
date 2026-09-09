from io import BytesIO

from gclib.j3d import BDL

from wiithon import WiiIsoPatcher
from wiithon.formats.rarc import Rarc, RarcFileEntry
from wiithon.formats.yaz0 import Yaz0

from ...Constants.patch_constants import *

class Gateway:
    arc_file: Rarc
    bdl_entry: RarcFileEntry
    patcher: WiiIsoPatcher

    def __init__(self, patcher: WiiIsoPatcher):
        self.patcher = patcher

        compressed_bytes = patcher.read_file(GATEWAY_PATH)
        uncompressed_bytes = Yaz0.read(BytesIO(compressed_bytes)).data
        self.arc_file = Rarc.read(BytesIO(uncompressed_bytes))
        
        self.bdl_entry = self.arc_file.get_file(GATEWAY_BDL_NAME)

    def create_miniature(self):
        bdl = BDL(BytesIO(self.bdl_entry.data))

        # Scale the BDL to the desired size
        for joint in bdl.jnt1.joints:
            scale = 3.14
            joint.bounding_sphere_radius *= scale
            joint.scale.x *= scale
            joint.scale.y *= scale
            joint.scale.z *= scale
            joint.bounding_box_min.x *= scale
            joint.bounding_box_min.y *= scale
            joint.bounding_box_min.z *= scale
            joint.bounding_box_max.x *= scale
            joint.bounding_box_max.y *= scale
            joint.bounding_box_max.z *= scale
        
        bdl.jnt1.save()
        for chunk in bdl.chunks:
            chunk.save()
        bdl.save()

        name: str = MINIATURE_GATEWAY_NAME.lower()
        self.arc_file.get_node('.').name = name
        self.arc_file.replace_file(GATEWAY_BDL_NAME, bdl.data.getvalue(), name + ".bdl")
        self.arc_file.remove_file("astrochildroom.kcl")
        self.arc_file.remove_file("astrochildroom.pa")
        self.arc_file.remove_file("collisionversion")
        self.arc_file.remove_file("revival.brk")

        new_file_path = OBJECT_DATA_PATH + MINIATURE_GATEWAY_NAME + ".arc"

        print(f"Creating {MINIATURE_GATEWAY_NAME}.arc")

        self.patcher.add_file(new_file_path, self.arc_file.get_bytes())
