from io import BytesIO

from gclib.j3d import BDL
from gclib.yaz0_yay0 import Yaz0

from wiithon import WiiIsoPatcher
from wiithon.file_helper.rarc import Rarc

from ...Constants.patch_constants import OBJECT_DATA_PATH, SURPRISED_GALAXY_PATH


class SurprisedGalaxy:
    bdl_base_name: str = "minisurprisedgalaxy.bdl"
    btk_base_name: str = "minisurprisedgalaxy.btk"
    patcher: WiiIsoPatcher
    arc_file: Rarc
    bdl_entry: BytesIO
    btk_entry: BytesIO

    scaled = False

    def __init__(self, patcher: WiiIsoPatcher):
        super().__init__()
        self.patcher = patcher

        self.arc_file = Rarc.read(Yaz0.decompress(BytesIO(patcher.read_file(SURPRISED_GALAXY_PATH))))
        self.bdl_entry = BytesIO(self.arc_file.get_file(self.bdl_base_name))
        self.btk_entry = BytesIO(self.arc_file.get_file(self.btk_base_name))
    
    def scale_joints(self, bdl: BDL):
        if not self.scaled:
            self.scaled = True
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

    def create_luma_miniature(self, luma_galaxy_name: str):
        name: str = luma_galaxy_name.lower()
        self.bdl_entry.name = name +'.bdl'
        
        bdl = BDL(self.bdl_entry)
        
        self.scale_joints(bdl)
        
        bdl.jnt1.save()
        for chunk in bdl.chunks:
            chunk.save()
        bdl.save()
        self.arc_file.replace_file(self.bdl_base_name, bdl.data.getvalue())
        
        self.btk_entry.name = name +'.btk'
        self.arc_file.replace_file(self.btk_base_name, self.btk_entry.getvalue())

        new_file_path = OBJECT_DATA_PATH + luma_galaxy_name + '.arc'

        print(f"Creating {luma_galaxy_name}.arc")
        arc_data = BytesIO()
        self.arc_file.write(arc_data)
        self.patcher.add_file(new_file_path, Yaz0.compress(arc_data).getvalue())
