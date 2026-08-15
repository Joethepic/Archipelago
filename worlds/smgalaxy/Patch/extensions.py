from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import ContextManager, T

from wiithon import WiiIsoPatcher
from wiithon.file_helper.bcsv import BCSV

from . import hashtable

NOP = b'\x60\x00\x00\x00'

class SMGObject(ABC):
    patcher: WiiIsoPatcher
    path: str

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def update(self, **kwargs) -> None:
        """Arguments are variable depending on the given object."""
        ...

    """
    @contextmanager
    def edit_bcsv(self, path: str) -> ContextManager[T]:
        return self.patcher.edit_as(self.path + '/' + path, BCSV, field_names=hashtable.hash_to_name, str_fmt="shift-jis")
    """
