from gclib.rarc import RARC
from .bcsv import BCSV

index_to_layer = {0: 'layera',
                  1: 'layerb',
                  2: 'layerc',
                  3: 'layerd',
                  4: 'layere',
                  5: 'layerf'}

def change_dome_miniature(astrodome: RARC, old_galaxies: list[list[str]], new_galaxies: list[list[str]], obj_arg0: list[list[int]]):
    for dome_index in range(6):
        layer = index_to_layer[dome_index]
        objinfo = next((BCSV(file) for file in astrodome.get_node_by_path(f"jmp/placement/{layer}").files if file.name == "objinfo"), None)
        
        # Check if it actually got a file
        if objinfo is None:
            raise ValueError(f"Could not find objinfo in: {astrodome}")
        
        entry_index = []
        for old_galaxy in old_galaxies[dome_index]:
            entry_index.append(objinfo.get_entry_index_by_name(old_galaxy))

        objarg0_index = objinfo.get_field_index('Obj_arg0')

        for i, new_galaxy in enumerate(new_galaxies[dome_index]):
            new_galaxy = 'Mini' + new_galaxy[4:]
            objinfo.replace_entry_name_by_index(entry_index[i], new_galaxy)
        
            objinfo.set_value_by_index(entry_index[i], objarg0_index, obj_arg0[dome_index][i])

        objinfo.save_changes()
    astrodome.save_changes()