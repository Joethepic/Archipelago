from gclib.rarc import RARC
from gclib.dol import DOL
from gclib.yaz0_yay0 import Yaz0
from .change_dol import *
from .bcsv import BCSV

shuffle = {1: 3,
           2: 2,
           3: 4,
           4: 1,
           5: 6,
           6: 5}

def is_valid_shuffle(dome_shuffle: dict[int, int]) -> bool:
    """Validate that the dome shuffle mapping contains all indices 1-6 as both keys and values."""
    for index in range(1,7):
        if index not in dome_shuffle.keys() or index not in dome_shuffle.values():
            return False
    return True

def update_domes(arc: RARC, dome_shuffle: dict[int, int]) -> None:
    for file in arc.get_node_by_path('').files:
        if file.name == "scenariodata.bcsv":
            scenariodata = BCSV(file)
    
    scenariono_index = scenariodata.get_field_index("ScenarioNo")
    astrodome_index = scenariodata.get_field_index("AstroDome")

    for entry_index in range(scenariodata.entry_count):
        scenariono = scenariodata.get_value_by_index(entry_index, scenariono_index)
        new_value = 2**(dome_shuffle[scenariono] - 1)
        scenariodata.set_value_by_index(entry_index, astrodome_index, new_value)
    
    scenariodata.save_changes()
    arc.save_changes()

def update_observatory(arc: RARC, dome_shuffle: dict[int, int]) -> None:
    if not is_valid_shuffle(dome_shuffle):
        raise ValueError(f"Invalid shuffle: {dome_shuffle}")
    
    for file in arc.get_node_by_path('jmp/placement/common').files:
        if file.name == 'objinfo':
            objinfo = BCSV(file)

    name_index = objinfo.get_field_index("name")
    objarg0_index = objinfo.get_field_index("Obj_arg0")
    posx_index = objinfo.get_field_index("pos_x")
    posy_index = objinfo.get_field_index("pos_y")
    posz_index = objinfo.get_field_index("pos_z")
    dirx_index = objinfo.get_field_index("dir_x")
    diry_index = objinfo.get_field_index("dir_y")
    dirz_index = objinfo.get_field_index("dir_z")
    swsleep_index = objinfo.get_field_index("SW_SLEEP")
    groupid_index = objinfo.get_field_index("GroupId")

    domes = {}

    for entry_index in range(objinfo.entry_count):
        if objinfo.get_value_by_index(entry_index, name_index) == "AstroDomeEntrance":
            objarg0 = objinfo.get_value_by_index(entry_index, objarg0_index)
            domes[objarg0] = {'entry_index': entry_index,
                              'pos_x': objinfo.get_value_by_index(entry_index, posx_index),
                              'pos_y': objinfo.get_value_by_index(entry_index, posy_index),
                              'pos_z': objinfo.get_value_by_index(entry_index, posz_index),
                              'dir_x': objinfo.get_value_by_index(entry_index, dirx_index),
                              'dir_y': objinfo.get_value_by_index(entry_index, diry_index),
                              'dir_z': objinfo.get_value_by_index(entry_index, dirz_index),}
        
        """
        if objinfo.get_value_by_index(entry_index, name_index) == 'SuperSpinDriverPink':
            objinfo.set_value_by_index(entry_index, groupid_index, -1)"""
        if objinfo.get_value_by_index(entry_index, name_index) == 'SurpCocoonExGalaxy':
            objinfo.replace_entry_name_by_index(entry_index, 'MiniCubeBubbleExLv1Galaxy')
            #objinfo.set_value_by_index(entry_index, swsleep_index, -1)
    
    reverse_shuffle = {}
    for key, value in dome_shuffle.items():
        reverse_shuffle[value] = key

    for objarg0 in domes.keys():
        entry_index = domes[objarg0]['entry_index']
        new_dome = reverse_shuffle[objarg0]
        new_values = domes[new_dome]
        print(entry_index, new_values)
        objinfo.set_value_by_index(entry_index, posx_index, new_values['pos_x'])
        objinfo.set_value_by_index(entry_index, posy_index, new_values['pos_y'])
        objinfo.set_value_by_index(entry_index, posz_index, new_values['pos_z'])
        objinfo.set_value_by_index(entry_index, dirx_index, new_values['dir_x'])
        objinfo.set_value_by_index(entry_index, diry_index, new_values['dir_y'])
        objinfo.set_value_by_index(entry_index, dirz_index, new_values['dir_z'])

    objinfo.save_changes()
    arc.save_changes()


if __name__ == "__main__":
    path = r"worlds/smgalaxy/Patch/temp/DATA/files/StageData/AstroGalaxy.arc"
    arc = RARC(path)
    update_observatory(arc, shuffle)

    with open(path, 'wb') as f:
        f.write(Yaz0.compress(arc.data).getvalue())
    
    dol = get_dol(r"worlds/smgalaxy/Patch/temp/DATA/sys/main.dol")
    write_to_dol(dol, 0x80536fa4, b'\x80\x59\x80\xd5')

    path = r"worlds/smgalaxy/Patch/temp/DATA/files/StageData/AstroDome/AstroDomeScenario.arc"
    arc = RARC(path)
    update_domes(arc, shuffle)
