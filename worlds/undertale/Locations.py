from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class UndertaleAdvancement(Location):
    game: str = "Undertale"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


advancement_table = {
    "Snowman": AdvData(79100, "Snowdin Forest"),
    "Snowman 2": AdvData(79101, "Snowdin Forest"),
    "Snowman 3": AdvData(79102, "Snowdin Forest"),
    "Nicecream Snowdin": AdvData(79001, "Snowdin Forest"),
    "Nicecream Waterfall": AdvData(79002, "Waterfall"),
    "Nicecream Punch Card": AdvData(79003, "Waterfall"),
    "Quiche Bench": AdvData(79004, "Waterfall"),
    "Tutu Hidden": AdvData(79005, "Waterfall"),
    "Card Reward": AdvData(79006, "Waterfall"),
    "Grass Shoes": AdvData(79007, "Waterfall"),
    "Noodles Fridge": AdvData(79008, "Hotland"),
    "Pan Hidden": AdvData(79009, "Hotland"),
    "Apron Hidden": AdvData(79010, "Hotland"),
    "Trash Burger": AdvData(79011, "Core"),
    "Present Knife": AdvData(79012, "New Home"),
    "Present Locket": AdvData(79013, "New Home"),
    "Candy 1": AdvData(79014, "Ruins"),
    "Candy 2": AdvData(79015, "Ruins"),
    "Candy 3": AdvData(79016, "Ruins"),
    "Candy 4": AdvData(79017, "Ruins"),
    "Donut Sale": AdvData(79018, "Ruins"),
    "Cider Sale": AdvData(79019, "Ruins"),
    "Ribbon Cracks": AdvData(79020, "Ruins"),
    "Toy Knife Edge": AdvData(79021, "Ruins"),
    "B.Scotch Pie Given": AdvData(79022, "Ruins"),
    "Astro 1": AdvData(79023, "Waterfall"),
    "Astro 2": AdvData(79024, "Waterfall"),
    "Dog Sale 1": AdvData(79026, "Hotland"),
    "Cat Sale": AdvData(79027, "Hotland"),
    "Dog Sale 2": AdvData(79028, "Hotland"),
    "Dog Sale 3": AdvData(79029, "Hotland"),
    "Dog Sale 4": AdvData(79030, "Hotland"),
    "Chisps Machine": AdvData(79031, "True Lab"),
    "Hush Trade": AdvData(79032, "Hotland"),
    "Letter Quest": AdvData(79033, "Snowdin Town"),
    "Bunny 1": AdvData(79034, "Snowdin Town"),
    "Bunny 2": AdvData(79035, "Snowdin Town"),
    "Bunny 3": AdvData(79036, "Snowdin Town"),
    "Bunny 4": AdvData(79037, "Snowdin Town"),
    "Gerson 1": AdvData(79038, "Waterfall"),
    "Gerson 2": AdvData(79039, "Waterfall"),
    "Gerson 3": AdvData(79040, "Waterfall"),
    "Gerson 4": AdvData(79041, "Waterfall"),
    "Bratty Catty 1": AdvData(79042, "Hotland"),
    "Bratty Catty 2": AdvData(79043, "Hotland"),
    "Bratty Catty 3": AdvData(79044, "Hotland"),
    "Bratty Catty 4": AdvData(79045, "Hotland"),
    "Burgerpants 1": AdvData(79046, "Hotland"),
    "Burgerpants 2": AdvData(79047, "Hotland"),
    "Burgerpants 3": AdvData(79048, "Hotland"),
    "Burgerpants 4": AdvData(79049, "Hotland"),
    "TemmieShop 1": AdvData(79050, "Waterfall"),
    "TemmieShop 2": AdvData(79051, "Waterfall"),
    "TemmieShop 3": AdvData(79052, "Waterfall"),
    "TemmieShop 4": AdvData(79053, "Waterfall"),
    "Papyrus Plot": AdvData(79056, "Snowdin Town"),
    "Undyne Plot": AdvData(79057, "Waterfall"),
    "Mettaton Plot": AdvData(79062, "Core"),
    "True Lab Plot": AdvData(79063, "Hotland"),
    "Left New Home Key": AdvData(79064, "New Home"),
    "Right New Home Key": AdvData(79065, "New Home"),
    "Starting Key": AdvData(79067, "Hub"),
    "LOVE 2": AdvData(79902, "???"),
    "LOVE 3": AdvData(79903, "???"),
    "LOVE 4": AdvData(79904, "???"),
    "LOVE 5": AdvData(79905, "???"),
    "LOVE 6": AdvData(79906, "???"),
    "LOVE 7": AdvData(79907, "???"),
    "LOVE 8": AdvData(79908, "???"),
    "LOVE 9": AdvData(79909, "???"),
    "LOVE 10": AdvData(79910, "???"),
    "LOVE 11": AdvData(79911, "???"),
    "LOVE 12": AdvData(79912, "???"),
    "LOVE 13": AdvData(79913, "???"),
    "LOVE 14": AdvData(79914, "???"),
    "LOVE 15": AdvData(79915, "???"),
    "LOVE 16": AdvData(79916, "???"),
    "LOVE 17": AdvData(79917, "???"),
    "LOVE 18": AdvData(79918, "???"),
    "LOVE 19": AdvData(79919, "???"),
    "LOVE 20": AdvData(79920, "???"),
    "ATK 2": AdvData(79800, "???"),
    "ATK 3": AdvData(79801, "???"),
    "ATK 4": AdvData(79802, "???"),
    "ATK 5": AdvData(79803, "???"),
    "ATK 6": AdvData(79804, "???"),
    "ATK 7": AdvData(79805, "???"),
    "ATK 8": AdvData(79806, "???"),
    "ATK 9": AdvData(79807, "???"),
    "ATK 10": AdvData(79808, "???"),
    "ATK 11": AdvData(79809, "???"),
    "ATK 12": AdvData(79810, "???"),
    "ATK 13": AdvData(79811, "???"),
    "ATK 14": AdvData(79812, "???"),
    "ATK 15": AdvData(79813, "???"),
    "ATK 16": AdvData(79814, "???"),
    "ATK 17": AdvData(79815, "???"),
    "ATK 18": AdvData(79816, "???"),
    "ATK 19": AdvData(79817, "???"),
    "ATK 20": AdvData(79818, "???"),
    "DEF 5": AdvData(79700, "???"),
    "DEF 9": AdvData(79701, "???"),
    "DEF 13": AdvData(79702, "???"),
    "DEF 17": AdvData(79703, "???"),
    "HP 2": AdvData(79600, "???"),
    "HP 3": AdvData(79601, "???"),
    "HP 4": AdvData(79602, "???"),
    "HP 5": AdvData(79603, "???"),
    "HP 6": AdvData(79604, "???"),
    "HP 7": AdvData(79605, "???"),
    "HP 8": AdvData(79606, "???"),
    "HP 9": AdvData(79607, "???"),
    "HP 10": AdvData(79608, "???"),
    "HP 11": AdvData(79609, "???"),
    "HP 12": AdvData(79610, "???"),
    "HP 13": AdvData(79611, "???"),
    "HP 14": AdvData(79612, "???"),
    "HP 15": AdvData(79613, "???"),
    "HP 16": AdvData(79614, "???"),
    "HP 17": AdvData(79615, "???"),
    "HP 18": AdvData(79616, "???"),
    "HP 19": AdvData(79617, "???"),
    "HP 20": AdvData(79618, "???"),
    "Undyne Date": AdvData(None, "Undyne\"s Home"),
    "Alphys Date": AdvData(None, "Hotland"),
    "Papyrus Date": AdvData(None, "Papyrus\" Home"),
}

exclusion_table = {
    "pacifist": {
        "LOVE 2",
        "LOVE 3",
        "LOVE 4",
        "LOVE 5",
        "LOVE 6",
        "LOVE 7",
        "LOVE 8",
        "LOVE 9",
        "LOVE 10",
        "LOVE 11",
        "LOVE 12",
        "LOVE 13",
        "LOVE 14",
        "LOVE 15",
        "LOVE 16",
        "LOVE 17",
        "LOVE 18",
        "LOVE 19",
        "LOVE 20",
        "ATK 2",
        "ATK 3",
        "ATK 4",
        "ATK 5",
        "ATK 6",
        "ATK 7",
        "ATK 8",
        "ATK 9",
        "ATK 10",
        "ATK 11",
        "ATK 12",
        "ATK 13",
        "ATK 14",
        "ATK 15",
        "ATK 16",
        "ATK 17",
        "ATK 18",
        "ATK 19",
        "ATK 20",
        "DEF 5",
        "DEF 9",
        "DEF 13",
        "DEF 17",
        "HP 2",
        "HP 3",
        "HP 4",
        "HP 5",
        "HP 6",
        "HP 7",
        "HP 8",
        "HP 9",
        "HP 10",
        "HP 11",
        "HP 12",
        "HP 13",
        "HP 14",
        "HP 15",
        "HP 16",
        "HP 17",
        "HP 18",
        "HP 19",
        "HP 20",
        "Snowman 2",
        "Snowman 3",
    },
    "neutral": {
        "Letter Quest",
        "Dog Sale 1",
        "Cat Sale",
        "Dog Sale 2",
        "Dog Sale 3",
        "Dog Sale 4",
        "Chisps Machine",
        "Hush Trade",
        "LOVE 2",
        "LOVE 3",
        "LOVE 4",
        "LOVE 5",
        "LOVE 6",
        "LOVE 7",
        "LOVE 8",
        "LOVE 9",
        "LOVE 10",
        "LOVE 11",
        "LOVE 12",
        "LOVE 13",
        "LOVE 14",
        "LOVE 15",
        "LOVE 16",
        "LOVE 17",
        "LOVE 18",
        "LOVE 19",
        "LOVE 20",
        "Papyrus Plot",
        "Undyne Plot",
        "True Lab Plot",
        "ATK 2",
        "ATK 3",
        "ATK 4",
        "ATK 5",
        "ATK 6",
        "ATK 7",
        "ATK 8",
        "ATK 9",
        "ATK 10",
        "ATK 11",
        "ATK 12",
        "ATK 13",
        "ATK 14",
        "ATK 15",
        "ATK 16",
        "ATK 17",
        "ATK 18",
        "ATK 19",
        "ATK 20",
        "DEF 5",
        "DEF 9",
        "DEF 13",
        "DEF 17",
        "HP 2",
        "HP 3",
        "HP 4",
        "HP 5",
        "HP 6",
        "HP 7",
        "HP 8",
        "HP 9",
        "HP 10",
        "HP 11",
        "HP 12",
        "HP 13",
        "HP 14",
        "HP 15",
        "HP 16",
        "HP 17",
        "HP 18",
        "HP 19",
        "HP 20",
        "Snowman 2",
        "Snowman 3",
    },
    "genocide": {
        "Letter Quest",
        "Dog Sale 1",
        "Cat Sale",
        "Dog Sale 2",
        "Dog Sale 3",
        "Dog Sale 4",
        "Chisps Machine",
        "Nicecream Snowdin",
        "Nicecream Waterfall",
        "Nicecream Punch Card",
        "Card Reward",
        "Apron Hidden",
        "Hush Trade",
        "Papyrus Plot",
        "Undyne Plot",
        "True Lab Plot",
    },
    "NoLove": {
        "LOVE 2",
        "LOVE 3",
        "LOVE 4",
        "LOVE 5",
        "LOVE 6",
        "LOVE 7",
        "LOVE 8",
        "LOVE 9",
        "LOVE 10",
        "LOVE 11",
        "LOVE 12",
        "LOVE 13",
        "LOVE 14",
        "LOVE 15",
        "LOVE 16",
        "LOVE 17",
        "LOVE 18",
        "LOVE 19",
        "LOVE 20",
    },
    "NoStats": {
        "ATK 2",
        "ATK 3",
        "ATK 4",
        "ATK 5",
        "ATK 6",
        "ATK 7",
        "ATK 8",
        "ATK 9",
        "ATK 10",
        "ATK 11",
        "ATK 12",
        "ATK 13",
        "ATK 14",
        "ATK 15",
        "ATK 16",
        "ATK 17",
        "ATK 18",
        "ATK 19",
        "ATK 20",
        "DEF 5",
        "DEF 9",
        "DEF 13",
        "DEF 17",
        "HP 2",
        "HP 3",
        "HP 4",
        "HP 5",
        "HP 6",
        "HP 7",
        "HP 8",
        "HP 9",
        "HP 10",
        "HP 11",
        "HP 12",
        "HP 13",
        "HP 14",
        "HP 15",
        "HP 16",
        "HP 17",
        "HP 18",
        "HP 19",
        "HP 20",
    },
    "all_routes": {
    }
}

events_table = {
}
