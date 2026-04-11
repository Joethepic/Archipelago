from gclib.rarc import RARC
from gclib.j3d import BDL

from ..extensions import RARCExtended
from .SurprisedGalaxy import SurprisedGalaxy

OBJECT_DATA_RELATIVE_PATH = "/DATA/files/ObjectData/"
GATEWAY_RELATIVE_PATH: str = "/DATA/files/ObjectData/AstroChildRoom.arc"
MINIATURE_GATEWAY_NAME: str = "MiniHeavensDoorGalaxy"

class Gateway(RARCExtended):
    bdl_base_name = "astrochildroom.bdl"

    def __init__(self):
        self.object_data_absolute_path = self.iso_base_path +  OBJECT_DATA_RELATIVE_PATH
        self.relative_path = GATEWAY_RELATIVE_PATH
        super().__init__()

        self.bdl_entry = self.get_file_entry(self.bdl_base_name)

    def create_miniature(self):
        # Scale the BDL to the desired size
        bdl: BDL = BDL(self.bdl_entry)

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
        self.bdl_entry.save_changes()

        # Instantiate an empty ARC file and populate it with they BDL entry
        name: str = MINIATURE_GATEWAY_NAME.lower()
        empty_arc: RARC = RARC()

        empty_arc.add_root_directory()

        root_node = empty_arc.get_node_by_path('')
        root_node.name = "minisurprisedgalaxy"

        empty_arc.add_new_file(name + ".bdl", self.bdl_entry.data, root_node)
        empty_arc.save_changes()
        
        self.data = empty_arc.data
        self.read()

        new_file_path = self.object_data_absolute_path + MINIATURE_GATEWAY_NAME + ".arc"

        print(f"Creating {MINIATURE_GATEWAY_NAME}.arc")

        self.save_to_new_file(new_file_path)
