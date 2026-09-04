from __future__ import annotations
import asyncio
from enum import Enum
import os
from enum import Enum
from pathlib import Path
import time
import struct
import sys
from typing import NamedTuple, Optional
import copy
import random

import Utils
from CommonClient import CommonContext, ClientCommandProcessor, logger, server_loop, gui_enabled, get_base_parser
from worlds.smgalaxy.Patch.Patch import SuperMarioGalaxyRandomiser

from .locations import SMGLocationData, location_table
from .regions import SMGRegionData, region_list
from .Constants.constants import *
from .Constants.Names.item_names import *
from .Constants.ram_constants import *

import dolphin_memory_engine as dme

class TypeTuple(NamedTuple):
    format: str
    size: int

class ValueType(Enum):
    BOOL = TypeTuple(">B", 1)
    u8 = TypeTuple(">B", 1)
    u16 = TypeTuple(">H", 2)
    u32 = TypeTuple(">I", 4)
    s8 = TypeTuple(">b", 1)
    s16 = TypeTuple(">h", 2)
    s32 = TypeTuple(">i", 4)
    string32 = TypeTuple(">32s", 32)

class Pointer:
    address: int
    offsets: list[int]
    value_type: ValueType
    base: int

    def __init__(self, offsets: list[int], value_type: ValueType, base: int = GAMESYSTEM):
        self.address = -1
        self.offsets = offsets
        self.value_type = value_type
        self.base = base

    async def recalculate(self) -> None:
        """Recalculates the address of the offset chain."""
        if self.offsets is not None:
            self.address = dme.follow_pointers(self.base, self.offsets)
        else:
            self.address = self.base

    async def get_value(self) -> int | str:
        """Gets the value of the pointer at its address. Raises a ValueError if not properly initialised.
        
        Returns:
            int: The value at the address.
            str: The value at the address.
        """
        if self.address == -1:
            raise ValueError("Address of pointer is not initialised")

        value = dme.read_bytes(self.address, self.value_type.value.size)
        unpack_val = struct.unpack(self.value_type.value.format, value)[0]
        if self.value_type == ValueType.string32:
            unpack_val = unpack_val.decode("ascii").split("\x00")[0]
        return unpack_val

    def write_value(self, value: int | str) -> None:
        """Write a value at the addresss of the pointer.
        
        Args:
            value (int | str): Value to write at the pointed address.
        """
        value = struct.pack(self.value_type.value.format, value)
        dme.write_bytes(self.address, value)

class GalaxyCommand(ClientCommandProcessor):
    def _cmd_dolphin(self) -> None:
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, GalaxyContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self) -> None:
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, GalaxyContext):
            Utils.async_start(self.ctx.update_death_link(not "DeathLink" in self.ctx.tags))

class StarColor(NamedTuple):
    name: str
    pointer: Pointer

class StarColorHandler:
    pointers: dict[str, Pointer]
    star_colors: list[StarColor] = []
    initialised: bool

    def __init__(self, pointers: dict[str, Pointer]):
        self.star_colors = []
        self.pointers = pointers
        self.initialised = False

    def set_star_colors(self, galaxyName: str, starNum: int):
        for star in self.star_colors:
            if star.name == galaxyName + "Colours" + str(starNum):
                star.pointer.write_value(PowerStarColorEnum.BLUE)

    def init_all_star_colors(self):
        if self.initialised == True:
            return 
        
        self.star_colors = []
        for location in location_table.values():
            starname = self.get_pointer_name(location)
            star_color = StarColor(starname, self.pointers[starname])
            self.star_colors.append(star_color)
        
        self.initialised = True

    def get_pointer_name(self, location: SMGLocationData):
        return location.in_game_galaxy_name + "Colours" + str(location.game_address)
        
class GalaxyContext(CommonContext):
    password_required: bool = False
    rom_loaded: bool = False
    command_processor = GalaxyCommand
    game: str = GAME_NAME
    items_handling = 0b111

    runloop: Optional[asyncio.Task[None]] = None
    dolphin_status: str = CONNECTION_INITIAL_STATUS

    last_galaxy: str = ""

    needs_recalculating: bool = True
    pointers: dict[str, Pointer] = {}

    highest_processed_item_index: int

    lives: int

    starcolorhandler: StarColorHandler

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for SMG Client.

        Returns:
            kvui.GameManager: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = f"Archipelago | {CLIENT_NAME}"
        return ui
    
    def __init__(self, server_address, password):
        """
        Initialize the SMG context.

        Args:
            server_address: Address of the Archipelago server.
            password: Password for server authentication.
        """
        super().__init__(server_address, password)

        # Create pointer dictionary for all the galaxy star flags
        star_count_flag_pointers = {value.in_game_name: Pointer(GALAXY_DATA_POINTER_LIST +
            [value.region_offset, STAR_BIT_FLAG_OFFSET], ValueType.u16) for value in region_list.values() if
            value.region_offset is not None}

        star_colour_pointers = {value.in_game_name + "Colours" + str(index): 
                                Pointer([STATIC_VARIABLE_OFFSETS[STARCOLOUR] + value.region_offset * 2 + index], ValueType.u8, STATIC_VARIABLES_POINTER)
                                for value in region_list.values() if value.region_offset is not None for index in range(8)}

        self.pointers = {**star_count_flag_pointers,
                         **star_colour_pointers,
                         "Scene Name": Pointer(CURRENT_SCENE_POINTER_LIST, ValueType.string32),
                         "Galaxy Name": Pointer(CURRENT_GALAXY_POINTER_LIST, ValueType.string32),
                         "Lives": Pointer(ONEUP_POINTER_LIST, ValueType.u16),
                         POWER: Pointer([STATIC_VARIABLE_OFFSETS[POWER]], ValueType.u8, STATIC_VARIABLES_POINTER),
                         GRAND: Pointer([STATIC_VARIABLE_OFFSETS[GRAND]], ValueType.u8, STATIC_VARIABLES_POINTER),
                         DEATHLINK: Pointer([STATIC_VARIABLE_OFFSETS[DEATHLINK]], ValueType.BOOL, STATIC_VARIABLES_POINTER),
                         GREEN: Pointer([STATIC_VARIABLE_OFFSETS[GREEN]], ValueType.u8, STATIC_VARIABLES_POINTER)}
                         #"Index": Pointer(LAST_RECEIVED_ITEM_POINTER_LIST, ValueType.u32)}
                         #"Swing": Pointer(SWING_PERMISSION_POINTER_LIST, ValueType.u16)}

        # Setup the handler for managing the star colours in scenario select
        self.starcolorhandler = StarColorHandler(star_colour_pointers)

    async def disconnect(self, msg: str = '') -> None:
        """Disconnect from the server, unhook from Dolphin Memory Engine and set flags.
        
        Args:
            msg (str): Error message to send to the client.
        """
        super().disconnect()
        dme.un_hook()

        if msg:
            logger.error(msg)

        self.set_dolphin_status(CONNECTION_LOST_STATUS)
        
        self.rom_loaded = False
        self.needs_recalculating = True
        
    async def check_ingame(self) -> bool:
        """Checks to see if Mario/Luigi is in game and not at file select.
        
        Returns:
            bool: Player in game.
        """
        game_status: str = await self.pointers["Scene Name"].get_value()
        curr_galaxy: str = await self.current_galaxy()
        
        return game_status == "Game" and curr_galaxy != "FileSelect"

    async def current_galaxy(self) -> str:
        """
        Updates what Galaxy the user is currently on, but for some weird reason also tracks if you are in FileSelect.
        Everything else including Domes, the Observatory Ship and even the intro planet has a galaxy name.
        
        Returns:
            str: The current galaxy (stage) name.
        """
        return await self.pointers["Galaxy Name"].get_value()
    
    async def last_visited_galaxy(self) -> None:
        """Update the last galaxy we were in and recalculate pointers if necessary."""
        if not await self.check_ingame():
            return
        curr_galaxy: str = await self.current_galaxy()

        if curr_galaxy != self.last_galaxy:
            self.needs_recalculating = True

        if curr_galaxy in ["AstroDome", "AstroGalaxy"]:
            return

        self.last_galaxy = curr_galaxy
    
    async def smg_locs_checker(self) -> None:
        """Checks the various location within SMG to see if the player has completed any appropriate actions."""
        if not await self.check_ingame():
            return
        
        local_missing_locs = copy.deepcopy(self.missing_locations) # Deepcopy to prevent list changing while iterating.

        for loc_id in local_missing_locs:
            local_loc: SMGLocationData = location_table[self.location_names.lookup_in_game(loc_id)]
            region_data: SMGRegionData = region_list[local_loc.region]

            if local_loc.game_address is None:
                continue

            star_bit_flag: int = await self.pointers[region_data.in_game_name].get_value()
            if await self.current_galaxy() == "AstroDome" or await self.current_galaxy() == "AstroGalaxy":
                if (star_bit_flag & (1 << local_loc.game_address)) > 0:
                    self.locations_checked.add(loc_id)

        for location_id in self.checked_locations:
            for key, location in location_table.items():
                if key != self.location_names.lookup_in_game(location_id):
                    continue
                
                self.starcolorhandler.set_star_colors(location.in_game_galaxy_name, location.game_address)
                    
        await self.check_locations(self.locations_checked)
    
    async def smg_recv_items(self) -> None:
        """Modify the items we have received to change things in game."""
        if not await self.check_ingame():
            return
        # currently errors on using pointer
        #logger.info(self.pointers["Index"].address)
        #self.highest_processed_item_index = await self.pointers["Index"].get_value()
        # Note: will resend items upon reconnection
        for item_id in self.items_received[self.highest_processed_item_index:]:
            # TODO: change to constants and probably a NamedTuple aswell
            match item_id.item:
                case 170000007:
                    self.lives = await self.pointers["Lives"].get_value() + 1
                    self.pointers["Lives"].write_value(self.lives)

                case 170000004:
                    logger.info("Power Star Received")
                    powerstars = await self.pointers[POWER].get_value() + 1
                    self.pointers[POWER].write_value(powerstars)

                case 170000005:
                    logger.debug("Grand Star Received")
                    powerstars = await self.pointers[POWER].get_value() + 1
                    self.pointers[POWER].write_value(powerstars)
                    grandstars = await self.pointers[GRAND].get_value() + 1
                    self.pointers[GRAND].write_value(grandstars)

                case 170000006:
                    # TODO: FIGURE OUT HOW TO GIVE GREEN STARS IN GAME
                    logger.debug("Green Star Received")
                    powerstars = await self.pointers[POWER].get_value() + 1
                    self.pointers[POWER].write_value(powerstars)
                    greenstars = await self.pointers[POWER].get_value() + 1
                    self.pointers[GREEN].write_value(greenstars)
            
            self.highest_processed_item_index += 1
            #await self.pointers["Index"].write_value(self.highest_processed_item_index)
    async def recalculate_pointers(self) -> None:
        """Recalculate the chain of offsets for each pointer as to avoid stale memory reading."""
        if not self.needs_recalculating:
            return
        
        for pointer in self.pointers.values():
            await pointer.recalculate()

        self.starcolorhandler.init_all_star_colors()

        self.needs_recalculating = False
    
    async def try_hook(self) -> bool:
        """Try to hook the Dolphin Memory Engine process into dolphin.
        
        Returns:
            bool: Dolphin Memory Engine able to hook into dolphin.
        """
        dme.hook()

        if dme.get_status() == dme.get_status().noEmu or dme.get_status() == dme.get_status().notRunning:
            dme.un_hook()

            self.set_dolphin_status(CONNECTION_INITIAL_STATUS)

            await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
            return False
        
        return True

    async def check_death(self) -> None:
        """Checking if we need to send a deathlink."""
        if "DeathLink" not in self.tags:
            return
        
        if not await self.check_ingame():
            return
        await asyncio.sleep(WAIT_TIMER_LONG_TIMEOUT)

        lives = await self.pointers["Lives"].get_value()

        if lives < self.lives and time.time() >= float(self.last_death_link + DEATH_LINK_TIMEOUT):
            await self.send_death(self.player_names[self.slot] + random.choice(DEATH_MESSAGES))

        self.lives = lives

    def set_dolphin_status(self, status: str) -> None:
        """
        Set the dolphin status and log it to the client.
        
        Args:
            status (str): The status that should be set and logged.
        """
        self.dolphin_status = status
        logger.info(self.dolphin_status)

    async def dme_loop(self) -> None:
        """Main loop that checks in game values using Dolphin Memory Engine."""
        try:
            # If DME is not already hooked or connected in any way
            if not dme.is_hooked() and not await self.try_hook():
                return
                
            if not self.dolphin_status == CONNECTION_CONNECTED_STATUS:
                #checks the id of the game as a string
                romgameid: bytes = dme.read_bytes(0x80000000,6)
                if romgameid.decode() != EXPECTED_GAME_ID:
                    dme.un_hook()

                    self.set_dolphin_status(DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY)

                    await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    return

                if not self.auth:
                    await self.get_username()
                    
                # Inform the player we are ready and waiting for them to connect.
                if not self.rom_loaded:
                    self.set_dolphin_status(CONNECTION_VERIFY_SERVER)
                    self.rom_loaded = True

                    await self.server_auth(self.password_required)

                if not self.slot:
                    await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    return

            await self.recalculate_pointers()
            self.lives = await self.pointers["Lives"].get_value()
            # Currently verified connected to AP and dolphin is properly loaded
            await self.last_visited_galaxy()
            await self.smg_locs_checker()
            await self.smg_recv_items()
            await self.check_death()
            
        except Exception as dmeEx:
            await self.disconnect("Unable to connect to SMG. Details: " + str(dmeEx))
            await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)

    async def dolphin_loop(self) -> None:
        """Continuously check and communicate with Dolphin until the user disconnects."""
        logger.info("Starting Dolphin connector. Use /dolphin for status information.")
        while not self.exit_event.is_set():
            try:
                await self.dme_loop()
                await wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)

            except Exception as dolphinEx:
                logger.error("Something went wrong when connecting to Dolphin Memory Engine. Details:" + str(dolphinEx))
    
    def on_package(self, cmd, args) -> None:
        """Processes and handles packets from the server."""
        super().on_package(cmd, args) # Required for UT

        match cmd:
            case "RoomInfo":
                self.password_required = bool(args["password"])
            
            case "Connected":
                self.highest_processed_item_index = 0
                
            #case "Bounced":
            #    if args["source"] != self.player_names[self.slot]:
            #        pass # handle (death) links

            case "ConnectionRefused":
                self.set_dolphin_status(AP_REFUSED_STATUS)

    def on_deathlink(self, data: dict) -> None:
        """
        Handle a DeathLink event.

        Args:
            data (dict): The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        Utils.async_start(self.kill_player(), "SMG - Kill Player")

    async def kill_player(self) -> None:
        """Kill the player in game."""
        if not await self.check_ingame():
            return

        self.pointers[DEATHLINK].write_value(True)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server. This function will be called as part of the init RoomInfo call
        in CommonClient, however we will exit if the rom is not loaded yet.

        Args:
            password_requested (bool): Whether the server requires a password. Defaults to `False`.
        """
        if not self.rom_loaded:
            logger.info("ROM is not loaded yet, waiting for dolphin to be connected before trying again.")
            return

        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()

        await self.send_connect()

async def _main(connect, password):
    try:
        ctx = GalaxyContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="SMG - ServerLoop")

        if gui_enabled:
            ctx.run_gui()

        ctx.run_cli()
        await wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)

        ctx.runloop = asyncio.create_task(ctx.dolphin_loop(), name="SMG - DolphinSync")

        await ctx.exit_event.wait()
        await ctx.shutdown()

        if ctx.runloop:
            await ctx.runloop

    except Exception as clientEx:
        client_msg: str = (f"An unknown error occurred while running {CLIENT_NAME}.\n" +
            f"Additional details:\n{str(clientEx)}")
        logger.error(client_msg)
        Utils.messagebox(f"Main Client Issue {CLIENT_NAME}", client_msg, True)
        raise clientEx
    
# launches/starts everything we need
def launch(*launch_args: str):
    import colorama
    Utils.init_logging(CLIENT_NAME)
    logger.info(f"Starting {CLIENT_NAME}")
    
    parser = get_base_parser()
    parser.add_argument("apsmg_file", default="", type=str, nargs="?", help="Path to an AP SMG file")
    args = parser.parse_args(launch_args)

    if args.apsmg_file:
        output_directory = Path(args.apsmg_file).parent
        iso_name = ''.join(os.path.basename(args.apsmg_file).split('.')[:-1])
        iso_path = os.path.join(output_directory, iso_name + '.iso')

        SuperMarioGalaxyRandomiser(args.apsmg_file).patch(iso_path)

    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()

async def wait_for_next_loop(time_to_wait: float) -> None:
    await asyncio.sleep(time_to_wait)

if __name__ == "__main__":
    launch(*sys.argv[1:])
