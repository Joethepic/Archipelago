from gclib.bti import BTI
from gclib.j3d import BDL
from gclib.rarc import RARC
import gclib.texture_utils as txt_util
from gclib.yaz0_yay0 import Yaz0
from PIL import Image

def replace_pixels(img: Image, threshold_values: tuple, new_colour: tuple):
    pixels = img.load()
    width = img.size[0]
    height = img.size[1]

    for x in range(width):
        for y in range(height):
            if False not in [pixels[x,y][i] <= threshold_values[i] for i in [0,1,2]]:
                pixels[x, y] = (*new_colour, 255)

def get_img(bdl: BDL, texture_name):
    if texture_name not in bdl.tex1.textures_by_name:
        raise ValueError(f"Texture not found in bdl file: {texture_name}")

    bti = bdl.tex1.textures_by_name[texture_name][0]
    img = txt_util.decode_image(bti.image_data, bti.palette_data,
                                bti.image_format, bti.palette_format,
                                bti.num_colors, bti.width, bti.height)
    return img

def set_img(bdl: BDL, texture_name, img: Image):
    if texture_name not in bdl.tex1.textures_by_name:
        raise ValueError(f"Texture not found in bdl file: {texture_name}")

    bti = bdl.tex1.textures_by_name[texture_name][0]
    bti.replace_image(img)
    bdl.tex1.textures_by_name[texture_name][0] = bti
    
def replace_pixels_in_img(bdl: BDL, texture_name: str, threshold_values: tuple, new_colour: tuple):
    img = get_img(bdl, texture_name)
    replace_pixels(img, threshold_values, new_colour)
    set_img(bdl, texture_name, img)

def change_mario_colours(mario_arc: RARC, mario_part: str, new_colour: tuple):
    """
    Change the color of a specific Mario part in a RARC archive.
    Args:
        mario_arc (RARC): The Mario.arc archive file containing mario.bdl.
        mario_part (str): The part of Mario to recolor (Accepted parts: 'Hat', 'Overalls').
        new_colour (tuple): RGB color tuple (r, g, b) with values 0-255.
    """

    if "mario.bdl" not in [file.name for file in mario_arc.file_entries]:
        raise ValueError("Arc file is not expected arc file: Mario.arc")
    
    if mario_part not in ['Hat', 'Overalls']:
        raise ValueError(f"Mario part is not an accepted part: {mario_part}")

    mario_arc_bdl = mario_arc.get_file("mario.bdl", BDL)

    if mario_part == 'Hat':
        replace_pixels_in_img(mario_arc_bdl, 'MarioCap.0', (255,50,50), new_colour)
    elif mario_part == 'Overalls':
        replace_pixels_in_img(mario_arc_bdl, 'MarioBody.0', (50,55,255), new_colour)

    mario_arc_bdl.save()
    for ch in mario_arc_bdl.chunks:
        ch.save()
    
    mario_arc.save_changes()

if __name__ == "__main__":
    mario_file = r"temp/DATA/files/ObjectData/Mario.arc"
    mario_arc = RARC(mario_file)

    change_mario_colours(mario_arc, 'Hat', (255,0,255))
    change_mario_colours(mario_arc, 'Overalls', (169,64,100))

    with open('Mario.arc', 'wb') as f:
        f.write(mario_arc.data.getvalue())