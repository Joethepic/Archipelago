import zipfile, json

from worlds.Files import APPlayerContainer
from NetUtils import convert_to_base_types

from ..Constants.constants import GAME_NAME

class SMGPlayerContainer(APPlayerContainer):
    game = GAME_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsmg"

    def __init__(self, player_choices: dict, input_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(input_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.json", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)