from io import BytesIO

from gclib.rarc import RARC
from gclib.j3d import BDL
from gclib.yaz0_yay0 import Yaz0

from wiithon import WiiIsoPatcher
from wiithon.file_helper.rarc import *

from ...Constants.patch_constants import *
from ..SMGDOL import SMGDOL

class Gateway:
    arc_file: Rarc
    bdl_entry: BytesIO
    patcher: WiiIsoPatcher
    dol: SMGDOL

    def __init__(self, patcher: WiiIsoPatcher, dol: SMGDOL):
        self.patcher = patcher
        self.dol = dol
        self.arc_file = Rarc.read(Yaz0.decompress(BytesIO(patcher.read_file(GATEWAY_PATH))))
        self.bdl_entry = BytesIO(self.arc_file.get_file(GATEWAY_BDL_NAME))

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
        self.arc_file.replace_file(GATEWAY_BDL_NAME, bdl.data.getvalue())

        # Instantiate an empty ARC file and populate it with they BDL entry
        name: str = MINIATURE_GATEWAY_NAME.lower()
        empty_arc: RARC = RARC()

        empty_arc.add_root_directory()

        root_node = empty_arc.get_node_by_path('')
        root_node.name = "minisurprisedgalaxy"

        empty_arc.add_new_file(name + ".bdl", self.bdl_entry, root_node)
        empty_arc.save_changes()

        new_file_path = GATEWAY_PATH + MINIATURE_GATEWAY_NAME + ".arc"

        print(f"Creating {MINIATURE_GATEWAY_NAME}.arc")
        self.patcher.add_file(new_file_path, Yaz0.compress(empty_arc.data).getvalue())

    def replace_loading(self, name_address: int) -> None:
        """
        Replaces typical loading of gateway galaxy of the gateway island. Replaces both the entrance and exit.
        """
        self.replace_entrance(name_address)
        self.replace_exit(name_address)

    def replace_entrance(self, name_address: int) -> None:
        upper_bytes: int = name_address >> 16
        lower_bytes: int = name_address & 0xFFFF

        new_instruction = b'\x3c\x60' + int.to_bytes(upper_bytes, 2)
        self.dol.dol.write_at(GATEWAY_ENTRANCE_ADDRESS_ONE, new_instruction)

        new_instruction = b'\x60\x63' + int.to_bytes(lower_bytes, 2)
        self.dol.dol.write_at(GATEWAY_ENTRANCE_ADDRESS_TWO, new_instruction)

    def replace_exit(self, name_address: int) -> None:
        upper_bytes: int = name_address >> 16
        lower_bytes: int = name_address & 0xFFFF

        new_instruction = b'\x3c\x60' + int.to_bytes(upper_bytes, 2)
        self.dol.dol.write_at(GATEWAY_EXIT_ADDRESS_ONE, new_instruction)

        new_instruction = b'\x60\x63' + int.to_bytes(lower_bytes, 2)
        self.dol.dol.write_at(GATEWAY_EXIT_ADDRESS_TWO, new_instruction)
