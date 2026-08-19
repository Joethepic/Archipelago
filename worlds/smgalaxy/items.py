from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional, Dict, Set

from.Constants.Names import item_names as itemname

class SMGItemData(NamedTuple):
    type: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None

# this lets us use these items by using SMGItem.
class SMGItem(Item):
    game: str = "Super Mario Galaxy"

    def __init__(self, name: str, player: int, data: SMGItemData):
        super(SMGItem, self).__init__(name, data.classification, data.code, player)
        self.type = data.type
        self.code = data.code


# This is all the items that are used by the game we define them here so they can be used.
item_table: dict[str, SMGItemData] = {
  itemname.POWER: SMGItemData(["Power Stars"], 170000004, IC.progression_deprioritized_skip_balancing),# rom address  0x007ACCA0F2FF8760 don't remeber how i found this or if it's acurate so could use double check.
  itemname.GRAND: SMGItemData(["Grand Stars", "Power Stars"], 170000005, IC.progression),
  itemname.GREEN: SMGItemData(["Green Stars", "Power Stars"], 170000006, IC.progression),
  
  #This is not going to be used in v1 as disccused "Progressive Comets": SMGItemData(["Comet"], 170000008, IC.progression),
  "Peach": SMGItemData(["Victory"], None, IC.progression)

}

filler_item_table: dict [str, SMGItemData] = {
    itemname.ONEUP: SMGItemData(["Filler Items"], 170000007, IC.filler),
}


all_items_table: dict[str, SMGItemData] = {**item_table, **filler_item_table}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in all_items_table.items() if data.code is not None}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in all_items_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories
