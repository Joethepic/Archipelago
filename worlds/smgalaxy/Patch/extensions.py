import abc
from contextlib import contextmanager
from typing import ContextManager, T

from wiithon import WiiIsoPatcher

from worlds.smgalaxy.Patch import hashtable

from .bcsv import BCSV

NOP = b'\x60\x00\x00\x00'

class SMGObject(abc.ABC):
    patcher: WiiIsoPatcher
    path: str

    def __init__(self, patcher: WiiIsoPatcher, path: str):
        self.patcher = patcher
        self.path = path

    @abc.abstractmethod
    def update(self) -> None:
        raise NotImplementedError(f"Unimplemented update method for object: {type(self)}")

    @contextmanager
    def edit_bcsv(self, path: str) -> ContextManager[T]:
        return self.patcher.edit_as(self.path + '/' + path, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis")