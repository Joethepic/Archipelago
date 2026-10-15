import dataclasses
import reprlib

# BEHOLD THE GCLIB MONKEY PATCHES REQUIRED TO WORK
# If _recursive_repr is missing, alias the public one from reprlib
if not hasattr(dataclasses, '_recursive_repr'):
    dataclasses._recursive_repr = reprlib.recursive_repr

import gclib.bunfoe as bunfoe
import typing

def _safe_issubclass(cls, class_or_tuple):
    if not isinstance(cls, type):
        # Resolve ForwardRef, GenericAlias, or anything else
        if isinstance(cls, typing.ForwardRef):
            try:
                cls = cls._evaluate(vars(bunfoe), None, None)
            except Exception:
                return False
        elif isinstance(cls, str):
            cls = getattr(bunfoe, cls, None)
        else:
            # Could be a GenericAlias like list[int] — check origin
            origin = getattr(cls, '__origin__', None)
            if origin is not None:
                cls = origin
        if not isinstance(cls, type):
            return False
    return issubclass(cls, class_or_tuple)

bunfoe.issubclass = _safe_issubclass

from io import BytesIO

from wiithon import BinaryReader, Yaz0, Rarc, BinaryWriter
from gclib import texture_utils
from gclib.gx_enums import ImageFormat, PaletteFormat

from ..extensions import SMGObject
from ...Constants.patch_constants import TITLE_SCREEN_LOGO_PATH, TITLE_SCREEN_BRLYT_PATH, TITLE_SCREEN_LOGO_FILE_PATH, \
    PROJECT_ROOT


class TitleScreen(SMGObject):
    def __init__(self) -> None:
        super().__init__(TITLE_SCREEN_LOGO_PATH)

        compressed_bytes = self.patcher.read_file(self.path)
        uncompressed_bytes = Yaz0.read(BytesIO(compressed_bytes)).data
        self.arc_file = Rarc.read(BytesIO(uncompressed_bytes))

    def update(self, **kwargs) -> None:

        names_image_data, _, _, width, height = texture_utils.encode_image_from_path(
            BytesIO(PROJECT_ROOT.joinpath('Patch', 'SMGObjects', 'names.png').read_bytes()),
            ImageFormat.RGB5A3, PaletteFormat.IA8)

        tpl_bytes = self.arc_file.get_file(TITLE_SCREEN_LOGO_FILE_PATH).data
        tpl_stream = BytesIO(tpl_bytes)
        tpl_reader = BinaryReader(tpl_stream)
        tpl_writer = BinaryWriter(tpl_stream)

        tpl_reader.seek(0x14)
        old_height = tpl_reader.u16()
        old_width = tpl_reader.u16()

        if old_width != width:
            raise ValueError(f"Width of the new title screen image is incorrect. Expected: {old_width}, got: {width}")

        height += old_height

        tpl_writer.seek(0x14)
        tpl_writer.u16(height)
        tpl_writer.u16(width)

        tpl_writer.seek(len(tpl_bytes))
        tpl_writer.raw(names_image_data.getvalue())
        
        self.arc_file.replace_file(TITLE_SCREEN_LOGO_FILE_PATH, tpl_writer.stream.getvalue())


        brlyt_bytes = self.arc_file.get_file(TITLE_SCREEN_BRLYT_PATH).data
        brlyt_stream = BytesIO(brlyt_bytes)
        brlyt_reader = BinaryReader(brlyt_stream)
        brlyt_writer = BinaryWriter(brlyt_stream)

        brlyt_reader.seek(0x92C)
        y_offset = brlyt_reader.float()

        brlyt_writer.seek(0x92C)
        brlyt_writer.float(y_offset - (height - old_height)/2.0)

        brlyt_writer.seek(0x94C)
        brlyt_writer.float(float(height))

        self.arc_file.replace_file(TITLE_SCREEN_BRLYT_PATH, brlyt_writer.stream.getvalue())

        self.patcher.replace_file(self.path, self.arc_file.get_bytes())
