from gclib.rarc import RARC
from gclib.dol import DOL
from gclib.j3d import BDL
from gclib.yaz0_yay0 import Yaz0
from gclib.bunfoe_types import Vec3float
from .change_dol import *

def replace_miniatures(dol: DOL, objectdata_path: str, galaxies: dict):
    mini_galaxies = list(galaxies.keys())
    surp_galaxies = list(galaxies.values())
    
    adjust_table(dol, mini_galaxies, surp_galaxies)

    for mini_galaxy, surp_galaxy in galaxies.items():
        if mini_galaxy.startswith("Surp") or surp_galaxy.startwith("Mini"):
            continue
        path = objectdata_path + 'MiniSurprisedGalaxy.arc'
        base = RARC(path)
        
        surp_galaxy = surp_galaxy.replace('Surp', 'Mini')

        file_entry = base.get_file_entry('minisurprisedgalaxy.bdl')
        file_entry.name = surp_galaxy.lower()+'.bdl'
        
        bdl = BDL(file_entry)
        
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
        file_entry.save_changes()

        btk = base.get_file_entry('minisurprisedgalaxy.btk')
        btk.name = surp_galaxy.lower()+'.btk'
        btk.save_changes()

        base.save_changes()

        with open(objectdata_path + surp_galaxy + '.arc', 'wb') as f:
            f.write(Yaz0.compress(base.data).getvalue())

def adjust_table(dol: DOL, old_galaxies: list[str], new_galaxies: list[str]):
    addresses = adjust_nameobjfactory_table(dol, old_galaxies, new_galaxies)

    # ArchiveList
    archivelist_address = 0x80537eb4
    archivelist_elements = 91
    archivelist_element_size = 0x8

    for element in range(archivelist_elements):
        address = archivelist_address + archivelist_element_size * element
        string_address = read_pointer_from_dol(dol, address)
        string = read_string_from_dol(dol, string_address)

        if string in old_galaxies:
            index = old_galaxies.index(string)
            addresses[index][0] = address
        
    for old, new in addresses:
        write_pointer_to_dol(dol, old, new)
        write_string_to_dol(dol, new, 'Mini')


def adjust_nameobjfactory_table(dol: DOL, old_galaxies: str, new_galaxies: str):
    addresses = [[0,0] for i in range(len(old_galaxies))]
    
    # NameObjFactory
    nameobjfactory_address = 0x80533980
    nameobjfactory_elements = 1182
    nameobjfactory_element_size = 0xc

    for element in range(nameobjfactory_elements):
        address = nameobjfactory_address + nameobjfactory_element_size * element
        string_address = read_pointer_from_dol(dol, address)
        string = read_string_from_dol(dol, string_address)

        if string in old_galaxies and string.startswith("Mini"):
            index = old_galaxies.index(string)
            addresses[index][0] = address
        
        if string in new_galaxies and string.startswith("Surp"):
            index = new_galaxies.index(string)
            addresses[index][1] = string_address
    
    for old, new in addresses:
        write_pointer_to_dol(dol, old, new)
    return addresses

if __name__ == "__main__":

    new_name = 'SurpTamakoroExLv2Galaxy'
    miniature_base_name = 'MiniHoneyBeeKingdomGalaxy'

    #add_miniature(name)
    adjust_nameobjfactory_table(miniature_base_name, new_name)

