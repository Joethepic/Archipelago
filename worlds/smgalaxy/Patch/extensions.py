from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import ContextManager, T

from wiithon import WiiIsoPatcher
from wiithon.formats.dol import DOL
from wiithon.formats.bcsv import BCSV

from . import hashtable

NOP = b'\x60\x00\x00\x00'

class SMGObject(ABC):
    patcher: WiiIsoPatcher
    path: str

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...

    """
    @contextmanager
    def edit_bcsv(self, path: str) -> ContextManager[T]:
        return self.patcher.edit_as(self.path + '/' + path, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis")
    """

class SMGDOLObject(ABC):
    dol: DOL

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...
