import struct
from enum import Enum
from typing import NamedTuple

from .Constants.constants import PowerStarColorEnum
from .Constants.ram_constants import GAMESYSTEM

import dolphin_memory_engine as dme

from .locations import SMGLocationData, location_table


class TypeTuple(NamedTuple):
    format: str
    size: int


class ValueType(Enum):
    BOOL = TypeTuple(">B", 1)
    u8 = TypeTuple(">B", 1)
    u16 = TypeTuple(">H", 2)
    u32 = TypeTuple(">I", 4)
    s8 = TypeTuple(">b", 1)
    s16 = TypeTuple(">h", 2)
    s32 = TypeTuple(">i", 4)
    string32 = TypeTuple(">32s", 32)
    string64 = TypeTuple(">64s", 64)


class Pointer:
    address: int
    offsets: list[int]
    value_type: ValueType
    base: int

    def __init__(self, offsets: list[int], value_type: ValueType, base: int = GAMESYSTEM):
        self.address = -1
        self.offsets = offsets
        self.value_type = value_type
        self.base = base

    async def recalculate(self) -> None:
        """Recalculates the address of the offset chain."""
        if self.offsets is not None:
            self.address = dme.follow_pointers(self.base, self.offsets)
        else:
            self.address = self.base

    async def get_value(self) -> int | str:
        """Gets the value of the pointer at its address. Raises a ValueError if not properly initialised.

        Returns:
            int: The value at the address.
            str: The value at the address.
        """
        if self.address == -1:
            raise ValueError(
                f"Address of pointer is not initialised.\nOffsets: {self.offsets}\nType: {self.value_type}\nBase address: {hex(self.base)}")

        value = dme.read_bytes(self.address, self.value_type.value.size)
        unpack_val = struct.unpack(self.value_type.value.format, value)[0]
        if self.value_type == ValueType.string32 or self.value_type == ValueType.string64:
            unpack_val = unpack_val.decode("ascii").split("\x00")[0]
        return unpack_val

    def write_value(self, value: int | str) -> None:
        """Write a value at the addresss of the pointer.

        Args:
            value (int | str): Value to write at the pointed address.
        """
        value = struct.pack(self.value_type.value.format, value)
        dme.write_bytes(self.address, value)


class StarColor(NamedTuple):
    name: str
    pointer: Pointer


class StarColorHandler:
    pointers: dict[str, Pointer]
    star_colors: list[StarColor] = []
    initialised: bool

    def __init__(self, pointers: dict[str, Pointer]):
        self.star_colors = []
        self.pointers = pointers
        self.initialised = False

    def set_star_colors(self, galaxyName: str, starNum: int):
        for star in self.star_colors:
            if star.name == galaxyName + "Colours" + str(starNum):
                star.pointer.write_value(PowerStarColorEnum.GREEN)

    def init_all_star_colors(self):
        if self.initialised == True:
            return

        self.star_colors = []
        for location in location_table.values():
            starname = self.get_pointer_name(location)
            star_color = StarColor(starname, self.pointers[starname])
            self.star_colors.append(star_color)

        self.initialised = True

    def get_pointer_name(self, location: SMGLocationData):
        return location.in_game_galaxy_name + "Colours" + str(location.game_address)