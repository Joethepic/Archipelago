from BaseClasses import Item, ItemClassification
from .locations import KSSLocationData
from typing import Dict, Set, NamedTuple
from .ExtractedData import items, logic_items, item_effects
class KSSItems(Item):
    game: str = "Kirby Super Star"
abilities_table: Dict[str, KSSLocationData] = {
  "Bomb": 272000000,
  "Cook": 272000001,
  "Copy": 272000002,
  "Figher": 272000003, 
  "Jet": 272000004,
  "Mirror": 272000005,
  "Paint": 272000006,
  "Plasma": 272000008,
  "Suplex": 272000009,
  "Wing": 272000010,
  "Yo-Yo": 272000011,
  "Beam": 272000012,
  "Crash": 272000013,
  "Cutter": 272000014,
  "Fire": 272000015,
  "Hammer": 272000016,
  "Ice": 272000017,
  "Mike": 272000018,
  "Parasol": 272000019,
  "Sleep": 272000020,
  "Stone": 272000021,
  "Wheel": 272000022,
}
money_table: dict[str, KSSLocationData] = {
    
}
junk_table: dict[str, KSSLocationData] = {
  "Nothing": 272000007,
}
all_items = {
    **abilities_table,
    **money_table,
    **junk_table,
}
# item group code 
lookup_type_to_names: Dict[str, Set[str]] = {}

item_name_groups = {group: lookup_type_to_names[group] for group in ("Money", "Abilites",
                                                                     "Junk",)}
item_name_groups.update({
    "Abilites": {abilities_table} 
})