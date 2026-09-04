from enum import IntEnum

from ..extensions import SMGDOLObject, CharPointer
from ...Constants.patch_constants import *

class FlagType(IntEnum):
    Type_0 = 0
    PowerStarCount = 1
    GalaxyUnlock = 2
    Scenario = 3
    Event = 4
    Type_5 = 5
    Type_6 = 6
    ScenarioFlag = 7
    Starbits = 8
    EventFlag = 9
    Complete = 10
    Progress = 11

class GameEventFlagTableEntry:
    def __init__(self, flag_name_pointer: CharPointer, flag_type: FlagType, dont_save: bool,
                 condition1: int, condition2: int, condition3: CharPointer, condition4: CharPointer):
        self.flag_name_pointer: CharPointer = flag_name_pointer
        self.flag_type: FlagType = flag_type
        self.dont_save: bool = dont_save
        self.condition1: int = condition1
        self.condition2: int = condition2
        self.condition3: CharPointer = condition3
        self.condition4: CharPointer = condition4

    def __str__(self):
        return ' '.join[self.flag_name_pointer.string,
                        str(self.flag_type),
                        str(self.dont_save),
                        str(self.condition1),
                        str(self.condition2),
                        self.condition3.string,
                        self.condition4.string]


class GameEventFlagTable(SMGDOLObject):
    entries: list[GameEventFlagTableEntry]

    def __init__(self):
        self.entries = []

        start_address = GAME_EVENT_FLAG_TABLE_START_ADDRESS
        element_count = GAME_EVENT_FLAG_TABLE_ELEMENT_COUNT
        element_size = GAME_EVENT_FLAG_TABLE_ELEMENT_SIZE
        
        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            
            flag_name_pointer = CharPointer(offset + 0x0)
            flag_type = FlagType(int.from_bytes(self.dol.read_at(offset + 0x4, 1)))
            dont_save = int.from_bytes(self.dol.read_at(offset + 0x5, 1))
            condition1 = int.from_bytes(self.dol.read_at(offset + 0x6, 1))
            condition2 = int.from_bytes(self.dol.read_at(offset + 0x7, 1))
            condition3 = CharPointer(offset + 0xC)
            condition4 = CharPointer(offset + 0x10)
            
            entry = GameEventFlagTableEntry(flag_name_pointer, flag_type, dont_save, condition1, condition2, condition3, condition4)
            self.entries.append(entry)

    def set_entry(self, flag_name: str, flag_type: FlagType = None, dont_save: bool = None,
                  condition1: int = None, condition2: int = None,
                  condition3: CharPointer = None, condition4: CharPointer = None) -> None:
        element = None
        for entry in self.entries:
            if entry.flag_name_pointer.string == flag_name:
                element = entry
                break

        if element == None:
            raise ValueError(f"{flag_name} could not be found in the GameEventFlagTable.")
        
        if flag_type != None:
            element.flag_type = flag_type
        
        if dont_save != None:
            element.dont_save = dont_save
        
        if condition1 != None:
            element.condition1 = condition1

        if condition2 != None:
            element.condition2 = condition2

        if condition3 != None:
            element.condition3 = condition3
        
        if condition4 != None:
            element.condition4 = condition4
    
    def get_entry(self, flag_name: str) -> GameEventFlagTableEntry:
        for entry in self.entries:
            if entry.flag_name_pointer == flag_name:
                return entry
        
        raise ValueError(f"{flag_name} could not be found in the GameEventFlagTable.")

    def update(self, **kwargs) -> None:
        assert len(self.entries) == GAME_EVENT_FLAG_TABLE_ELEMENT_COUNT
        
        for entry in self.entries:
            flag_name = entry.flag_name_pointer.string
            if not flag_name.startswith("Appear"):
                continue

            entry.flag_type = FlagType.PowerStarCount
            entry.condition1 = 0
            entry.condition2 = 0
            entry.condition3.zero()
            entry.condition4.zero()

        # Write all the entry values
        start_address = GAME_EVENT_FLAG_TABLE_START_ADDRESS
        element_size = GAME_EVENT_FLAG_TABLE_ELEMENT_SIZE

        for entry_index, entry in enumerate(self.entries):
            offset = start_address + element_size * entry_index
            entry.flag_name_pointer.write_pointer()
            self.dol.write_at(offset + 0x4, entry.flag_type.to_bytes())
            self.dol.write_at(offset + 0x5, entry.dont_save.to_bytes())
            self.dol.write_at(offset + 0x6, entry.condition1.to_bytes())
            self.dol.write_at(offset + 0x7, entry.condition2.to_bytes())
            entry.condition3.write_pointer()
            entry.condition4.write_pointer()
