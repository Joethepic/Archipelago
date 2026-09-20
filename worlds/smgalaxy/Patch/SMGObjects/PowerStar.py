import copy
from io import BytesIO
from PIL import ImageOps

from gclib.j3d import BDL
from gclib.bti import BTI

from wiithon.formats.rarc import Rarc
from wiithon.formats.yaz0 import Yaz0

from ..extensions import SMGObject
from ...Constants.patch_constants import *
from ...Constants.constants import *

PADDING_STRING: str = "This is padding data to alignme"

def read_u16(stream: BytesIO) -> int:
    return int.from_bytes(stream.read(2), "big")

def read_u32(stream: BytesIO) -> int:
    return int.from_bytes(stream.read(4), "big")

def write_u16(stream: BytesIO, value: int) -> None:
    stream.write(value.to_bytes(2))

def write_u32(stream: BytesIO, value: int) -> None:
    stream.write(value.to_bytes(4))

def string(stream: BytesIO) -> str:
    out = b''
    while True:
        char = stream.read(1)
        if char == b'\x00':
            break
        out += char
    return out.decode()

class KeyFrame(NamedTuple):
    frame_count: int
    first_index_offset: int

class BTP:
    def __init__(self):
        self.animation_length: int = 0
        self.key_frames: list[KeyFrame] = []
        self.index_offsets: list[int] = []
        self.remap_table: bytes = b''
        self.names: list[str] = []
        
    @classmethod
    def read(cls, stream: BytesIO) -> "BTP":
        obj = cls()
        stream.read(0x2A)

        obj.animation_length = read_u16(stream)
        key_frame_count = read_u16(stream)
        index_offset_count = read_u16(stream)

        key_frame_data_offset = read_u32(stream)
        texture_index_offset = read_u32(stream)
        remap_table_offset = read_u32(stream)
        string_table_offset = read_u32(stream)

        stream.seek(key_frame_data_offset + 0x20)
        for key_frame in range(key_frame_count):
            obj.key_frames.append(KeyFrame(read_u16(stream), read_u16(stream)))

        stream.seek(texture_index_offset + 0x20)
        for index_offset in range(index_offset_count):
            obj.index_offsets.append(read_u16(stream))

        stream.seek(remap_table_offset + 0x20)
        obj.remap_table = stream.read(string_table_offset - remap_table_offset)

        stream.seek(string_table_offset + 0x20)
        string_count = read_u16(stream)
        stream.read(2)

        string_offsets: list[int] = []
        for string_index in range(string_count):
            stream.read(2)
            string_offsets.append(read_u16(stream))

        for string_offset in string_offsets:
            stream.seek(string_table_offset + string_offset + 0x20)
            obj.names.append(string(stream))

        return obj

    def write(self, stream: BytesIO) -> None:
        # File Header
        stream.write(b'J3D1btp1')
        write_u32(stream, 0)
        write_u32(stream, 1)
        stream.write(b'\xFF' * 0x10)

        # Section Header
        stream.write(b'TPT1')
        write_u32(stream, 0)
        stream.write(b'\x00\xFF')
        write_u16(stream, self.animation_length)
        write_u16(stream, len(self.key_frames))
        write_u16(stream, len(self.index_offsets))
        write_u32(stream, 0)
        write_u32(stream, 0)
        write_u32(stream, 0)
        write_u32(stream, 0)

        # Actual data
        key_frame_offset = stream.tell()
        for key_frame in self.key_frames:
            write_u16(stream, key_frame.frame_count)
            write_u16(stream, key_frame.first_index_offset)
            stream.write(b'\x00\xFF\xFF\xFF')

        texture_index_offset = stream.tell()
        for index_offset in self.index_offsets:
            write_u16(stream, index_offset)

        remap_table_offset = stream.tell()
        stream.write(self.remap_table)

        string_table_offset = stream.tell()
        write_u16(stream, len(self.names))
        stream.write(b'\xFF\xFF')

        offsets: list[int] = [4 + len(self.names) * 4]
        for string in self.names:
            offsets.append(offsets[-1] + len(string) + 1)

        def hash(string: str) -> int:
            out = 0
            for char in string.encode():
                out *= 3
                out += char

            return out & 0xFFFF

        for offset, string in zip(offsets, self.names):
            write_u16(stream, hash(string))
            write_u16(stream, offset)

        for string in self.names:
            stream.write(string.encode())
            stream.write(b'\x00')

        pad_boundary = (stream.tell() + 0x1F) & ~0x1F
        pad_size = pad_boundary - stream.tell()
        stream.write(PADDING_STRING[:pad_size].encode())

        file_size = stream.tell()
        stream.seek(0x8)
        write_u32(stream, file_size)

        stream.seek(0x24)
        write_u32(stream, file_size - 0x20)

        stream.seek(0x30)
        write_u32(stream, key_frame_offset)
        write_u32(stream, texture_index_offset)
        write_u32(stream, remap_table_offset)
        write_u32(stream, string_table_offset)

        print("WRITING BTP")
        print(self.index_offsets)

class PowerStar(SMGObject):
    arc_file: Rarc

    def __init__(self):
        super().__init__(POWER_STAR_PATH)

        compressed_bytes = self.patcher.read_file(self.path)
        uncompressed_bytes = Yaz0.read(BytesIO(compressed_bytes)).data
        self.arc_file = Rarc.read(BytesIO(uncompressed_bytes))

    def update(self, **kwargs):

        class SuperBDL(BDL):
            @classmethod
            def read(cls, stream: BytesIO) -> "SuperBDL":
                obj = cls()
                obj.data = stream
                BDL.read(obj)
                return obj

            def write(self, stream: BytesIO) -> None:
                print("WRITING SUPERBDL")
                stream.write(self.data.getvalue())

        def replace_colour(texture: BTI, colour: tuple):
            img = texture.render()
            gray = ImageOps.grayscale(img)
            coloured_img = ImageOps.colorize(gray, black=(165, 69, 0), white=colour).convert("RGBA")
            coloured_img.putalpha(img.getchannel("A"))
            texture.replace_image(coloured_img)

        new_colours: list[tuple] = [PINK, PURPLE, BROWN, BLACK]

        bdl: SuperBDL
        with self.patcher.edit_as(self.path +"/powerstar.bdl", SuperBDL) as bdl:
            for colour in new_colours:
                texture = copy.deepcopy(bdl.tex1.textures[1])
                replace_colour(texture, colour)
                bdl.tex1.textures.append(texture)
                bdl.tex1.texture_names.append(f"PowerStar.{bdl.tex1.num_textures - 3}")
                bdl.tex1.num_textures += 1

            colour_indices = [i for i in range(len(bdl.tex1.texture_names)) if bdl.tex1.texture_names[i].startswith("PowerStar")]
            bdl.save()

        btp: BTP
        with self.patcher.edit_as(self.path + "/powerstar.btp", BTP) as btp:
            btp.index_offsets = colour_indices + [colour_indices[-1]]
            btp.key_frames = [KeyFrame(len(colour_indices), 0)]
            btp.animation_length = len(colour_indices)

        self.patcher.replace_file(self.path, self.arc_file.get_bytes())
