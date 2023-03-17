
from BaseClasses import Location
from typing import NamedTuple, Optional, Dict

class KSSLocation(Location):
    game: str = "Super Mario Galaxy"

class KSSLocationData(NamedTuple):
    category: str
    code: Optional[int] = None

loc_table = {
    **{f"Chest {i+1}":                          KSSLocationData("Chests",  272_000_000 + i) for i in range(0, 30)}
}
