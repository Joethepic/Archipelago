from gclib import texture_utils
from gclib.gx_enums import ImageFormat
from gclib.j3d import BDL
from enum import StrEnum
from PIL.Image import Image

from ...Options import MarioColors
from ..extensions import RARCExtended

MARIO_RELATIVE_PATH = "/DATA/files/ObjectData/Mario.arc"

WHITE = (255, 255, 255)
OLD_CAP_COLOUR = (181, 0, 0)
OLD_GLOVES_COLOUR = (153, 153, 153)

def lerp1(x: int | float, begin: int, end: int) -> int:
    return int(begin + (end - begin) * x)

def lerp(x: int | float, begin: tuple, end: tuple) -> tuple:
    return (lerp1(x, y, z) for y, z in zip(begin, end))

def distance(x: tuple, y: tuple) -> int:
    return sum([(i - j) ** 2 for i, j in zip(x, y)])

class MarioColours:
    """
    A utility class for modifying Mario's colours in Super Mario Galaxy.
    This class handles the extraction, manipulation, and replacement of colour values
    in Mario's character model textures (hat, overalls, gloves, and shoes) by working
    with BDL (Binary Display List) files. It uses pixel threshold detection to identify
    and replace specific colored regions in texture images.
    """
    colour_map: dict[str, tuple[int, int, int]] = {"Red"   : (255,  0,  0),
                                                   "Orange": (255,165,  0),
                                                   "Yellow": (255,255,  0),
                                                   "Green" : (  0,128,  0),
                                                   "Blue"  : (  0,  0,255),
                                                   "Purple": (128,  0,128),
                                                   "Black" : (  0,  0,  0),
                                                   "Brown" : (165, 42, 42),
                                                   "White" : (255,255,255),
                                                   "Pink"  : (255,192,203),
                                                   "Gray"  : (128,128,128)}

    class Parts(StrEnum):
        HAT: str = "Hat"
        OVERALLS: str = "Overalls"
        SHOES: str = "Shoes"
        GLOVES: str = "Gloves"

    def __init__(self, mario: RARCExtended):
        self.mario = mario

        if "mario.bdl" not in [file.name for file in self.mario.file_entries]:
            raise ValueError("Arc file is not expected arc file: Mario.arc")            
        
        self.bdl = self.mario.get_file("mario.bdl", BDL)
        
    def paint_hat(self, old_colour: tuple[int, int, int], new_colour: tuple[int, int, int], *args) -> tuple[int, int, int]:
        distance_to_old = distance(old_colour, OLD_CAP_COLOUR)
        max_distance = distance(OLD_CAP_COLOUR, WHITE)

        return lerp(1 - distance_to_old / max_distance, old_colour, new_colour)

    def paint_overalls(self, old_colour: tuple[int, int, int], new_colour: tuple[int, int, int], x, y, *args) -> tuple[int, int, int]:
        if x >= 128 and y >= 44:
            return old_colour
        
        return new_colour
    
    def paint_shoes(self, old_colour: tuple[int, int, int], new_colour: tuple[int, int, int], x, y, *args) -> tuple[int, int, int]:
        if x < 192 or y < 108:
            return old_colour
        
        return new_colour

    def paint_gloves(self, old_colour: tuple[int, int, int], new_colour: tuple[int, int, int], *args) -> tuple[int, int, int]:
        distance_to_old = distance(old_colour, OLD_GLOVES_COLOUR)
        max_distance = distance(OLD_GLOVES_COLOUR, WHITE)

        return lerp(distance_to_old / max_distance, old_colour, new_colour)

    def paint_pixels(self, img: Image, colour: tuple[int, int, int], paint_callback) -> Image:
        pixels = img.load()
        width, height = img.size

        for x in range(width):
            for y in range(height):
                old_colour = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2])
                pixels[x, y] = (*paint_callback(old_colour, colour, x, y), 255)

        return img
    
    def paint_texture(self, texture_name: str, paint_callback, colour, texture_count = 1) -> None:
        for texture_index in range(texture_count):
            bti = self.bdl.tex1.textures_by_name[texture_name][texture_index]
            img = texture_utils.decode_image(bti.image_data, bti.palette_data,
                                            bti.image_format, bti.palette_format,
                                            bti.num_colors, bti.width, bti.height)
            
            bti.image_format = ImageFormat.CMPR
            bti.replace_image(self.paint_pixels(img, colour, paint_callback))
            self.bdl.tex1.textures_by_name[texture_name][texture_index] = bti

    def update_part(self, mario_part: str, colour: str) -> None:
        if mario_part not in MarioColors.valid_keys:
            raise ValueError(f"Mario part is not an accepted part: {mario_part}")

        if colour is MarioColors.default[mario_part]:
            return
        
        print(f"Updating {mario_part.lower()} to {colour.lower()}")

        texture_count = 1

        match mario_part:
            case self.Parts.HAT:
                texture_name = "MarioCap.0"
                callback = self.paint_hat

            case self.Parts.OVERALLS:
                texture_name = "MarioBody.0"
                callback = self.paint_overalls

            case self.Parts.SHOES:
                texture_name = "MarioBody.0"
                callback = self.paint_shoes

            case self.Parts.GLOVES:
                texture_name = "MarioHand"
                callback = self.paint_gloves
                texture_count = 2

            case _:
                raise ValueError(f"Cannot find mario part: {mario_part}")

        if texture_name not in self.bdl.tex1.textures_by_name:
            raise ValueError(f"Texture not found in bdl file: {texture_name}")

        self.paint_texture(texture_name, callback, self.colour_map[colour], texture_count)

        self.bdl.save()
        for ch in self.bdl.chunks:
            ch.save()

class Mario(RARCExtended):
    def __init__(self):
        self.relative_path = MARIO_RELATIVE_PATH
        super().__init__()

        self.colours = MarioColours(self)
    
    def update_colours(self, items: dict[str, str]) -> None:
        for mario_part, colour in items.items():
            self.colours.update_part(mario_part, colour)
