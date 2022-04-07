from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class UndertaleItem(Item):
    game: str = "Undertale"


item_table = {
    "Plot": ItemData(66000, True),
    "Monster Candy": ItemData(66001, False),
    "Croquet Roll": ItemData(66002, False),
    "Stick": ItemData(66003, True),
    "Bandage": ItemData(66004, True),
    "Rock Candy": ItemData(66005, False),
    "Pumpkin Rings": ItemData(66006, False),
    "Spider Donut": ItemData(66007, False),
    "Stoic Onion": ItemData(66008, False),
    "Ghost Fruit": ItemData(66009, False),
    "Spider Cider": ItemData(66010, False),
    "Butterscotch Pie": ItemData(66011, False),
    "Faded Ribbon": ItemData(66012, True),
    "Toy Knife": ItemData(66013, True),
    "Tough Glove": ItemData(66014, True),
    "Manly Bandanna": ItemData(66015, True),
    "Snowman Piece": ItemData(66016, False),
    "Nice Cream": ItemData(66017, False),
    "Puppydough Icecream": ItemData(66018, False),
    "Bisicle": ItemData(66019, False),
    "Unisicle": ItemData(66020, False),
    "Cinnamon Bun": ItemData(66021, False),
    "Temmie Flakes": ItemData(66022, False),
    "Abandoned Quiche": ItemData(66023, False),
    "Old Tutu": ItemData(66024, True),
    "Ballet Shoes": ItemData(66025, True),
    "Punch Card": ItemData(66026, False),
    "Annoying Dog": ItemData(66027, False),
    "Dog Salad": ItemData(66028, False),
    "Dog Residue": ItemData(66029, False),
    "Dog Residue": ItemData(66030, False),
    "Dog Residue": ItemData(66031, False),
    "Dog Residue": ItemData(66032, False),
    "Dog Residue": ItemData(66033, False),
    "Dog Residue": ItemData(66034, False),
    "Astronaut Food": ItemData(66035, False),
    "Instant Noodles": ItemData(66036, False),
    "Crab Apple": ItemData(66037, False),
    "Hot Dog...?": ItemData(66038, False),
    "Hot Cat": ItemData(66039, False),
    "Glamburger": ItemData(66040, False),
    "Sea Tea": ItemData(66041, False),
    "Starfait": ItemData(66042, False),
    "Legendary Hero": ItemData(66043, False),
    "Cloudy Glasses": ItemData(66044, True),
    "Torn Notebook": ItemData(66045, True),
    "Stained Apron": ItemData(66046, True),
    "Burnt Pan": ItemData(66047, True),
    "Cowboy Hat": ItemData(66048, True),
    "Empty Gun": ItemData(66049, True),
    "Heart Locket": ItemData(66050, True),
    "Worn Dagger": ItemData(66051, True),
    "Real Knife": ItemData(66052, True),
    "The Locket": ItemData(66053, True),
    "Bad Memory": ItemData(66054, False),
    "Dream": ItemData(66055, False),
    "Undyne's Letter": ItemData(66056, False),
    "Undyne Letter EX": ItemData(66057, True),
    "Popato Chisps": ItemData(66058, False),
    "Junk Food": ItemData(66059, False),
    "Mystery Key": ItemData(66060, False),
    "Face Steak": ItemData(66061, False),
    "Hush Puppy": ItemData(66062, False),
    "Snail Pie": ItemData(66063, False),
    "temy armor": ItemData(66064, True),
}

required_items = {
    "Legendary Hero": 1,
    "Face Steak": 1,
    "Cloudy Glasses": 1,
    "Torn Notebook": 1,
    "Bisicle": 1,
    "Tough Glove": 1,
    "Manly Bandanna": 1,
    "Undyne Letter EX": 1,
    "Snowman Piece": 1,
    "Abandoned Quiche": 1,
    "Old Tutu": 1,
    "Punch Card": 3,
    "Ballet Shoes": 1,
    "Instant Noodles": 1,
    "Burnt Pan": 1,
    "Stained Apron": 1,
    "Worn Dagger": 1,
    "Heart Locket": 1,
    "Faded Ribbon": 1,
    "Toy Knife": 1,
    "Butterscotch Pie": 1,
    "temy armor": 1,
    "Cowboy Hat": 1,
    "Empty Gun": 1,
    "Mystery Key": 1,
    "Hot Cat": 1,
    "Hush Puppy": 1,
}

junk_weights = {
    "Glamburger": 1,
    "Crab Apple": 1,
    "Sea Tea": 1,
    "Nice Cream": 1,
    "Spider Donut": 1,
    "Monster Candy": 1,
    "Popato Chisps": 1,
    "Junk Food": 1,
    "Temmie Flakes": 1,
    "Spider Cider": 1,
    "Hot Dog...?": 1,
    "Cinnamon Bun": 1,
    "Astronaut Food": 1,
    "Starfait": 1,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
