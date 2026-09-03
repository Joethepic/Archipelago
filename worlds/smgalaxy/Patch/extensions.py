from abc import ABC, abstractmethod

from wiithon import WiiIsoPatcher
from wiithon.formats.dol import DOL

NOP = b'\x60\x00\x00\x00'


class SMGObject(ABC):
    patcher: WiiIsoPatcher
    path: str

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...


class SMGDOLObject(ABC):
    dol: DOL

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...


class Pointer:
    dol: DOL
    base_address: int
    pointing_address: int

    def __init__(self, base_address: int):
        self.base_address = base_address
        self.read_pointer()

    def read_pointer(self):
        self.pointing_address = int.from_bytes(self.dol.read_at(self.base_address, 4))

    def write_pointer(self):
        self.dol.write_at(self.base_address, int.to_bytes(self.pointing_address, 4, "big"))


class CharPointer(Pointer):
    string: str | None

    def read_pointer(self):
        super().read_pointer()

        if self.pointing_address == 0:
            self.string = None
            return

        raw = self.dol.read_until_null_at(self.pointing_address)
        self.string = raw.decode("shift-jis")

    def write_string(self) -> None:
        self.dol.write_at(self.pointing_address, self.string.encode("shift-jis") + b'\0')

    def replace_prefix(self, new_prefix: str) -> None:
        prefix_size = len(new_prefix)

        if prefix_size > len(self.string):
            raise ValueError(f"New prefix is larger than the string.\nPrefix: {new_prefix}, string: {self.string}")

        self.string = new_prefix + self.string[len(new_prefix):]
        self.write_string()


class FunctionPointer(Pointer):
    def write_function_address(self, new_function_address: int):
        self.pointing_address = new_function_address

        self.write_pointer()