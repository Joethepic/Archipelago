from io import BytesIO

from wiithon.ppc import instructions as PPC
from wiithon.formats.dol import DOL


from .extensions import SMGObject, SMGDOLObject, Pointer
from .SMGDolObjects.NameObjFactory import NameObjFactory
from .SMGDolObjects.GalaxyUnlockTable import GalaxyUnlockTable
from .SMGDolObjects.GameEventFlagTable import GameEventFlagTable
from ..Constants.Names.item_names import POWER, GRAND, GREEN
from ..Constants.patch_constants import *
from ..Constants.ram_constants import STARCOLOUR, DEATHLINK, STATIC_VARIABLE_OFFSETS, STATIC_VARIABLES_POINTER
from ..locations import location_table
from ..regions import region_list, galaxies_list

class SMGDOL(SMGObject):
    data: BytesIO
    custom_section_size: int = 0x1000
    custom_section_address: int

    objects: dict[str, SMGDOLObject]

    write_pointer: int

    def __init__(self, dol: DOL):
        super().__init__(None)
        self.dol: DOL = dol

        # Necessary for wiithon
        #self.data = BytesIO(self.dol.to_bytes())

        Pointer.dol = self.dol
        SMGDOLObject.dol = self.dol

        self.objects = {
            "NameObjectFactory": NameObjFactory(),
            "GalaxyUnlockTable": GalaxyUnlockTable(),
            "GameEventFlagTable": GameEventFlagTable()
        }

        size, addrs = self.dol.inject_above_arena([PPC.nop() * int(self.custom_section_size/4)])
        self.custom_section_address = addrs[0]

        print(f"Injected custom section at: {hex(self.custom_section_address)}")

        self.dol.write_at(STATIC_VARIABLES_POINTER, self.custom_section_address.to_bytes(4))

        # Align to 4 bytes
        variable_space = (STATIC_VARIABLE_OFFSETS["End"] + 0x3) & ~0x3

        # Clear out the space
        self.dol.write_at(self.custom_section_address, bytes(variable_space))

        print(f"Functions starting at: {hex(self.custom_section_address + variable_space)}")

        # Hook to custom function
        self.write_pointer = 0x803995c0
        self.write_instruction(PPC.b(self.custom_section_address + variable_space, self.write_pointer))

        # Setup custom function
        self.write_pointer = self.custom_section_address + variable_space
        self.write_instruction(PPC.stwu(1, -0x100, 1))
        self.write_instruction(PPC.mflr(0))
        self.write_instruction(PPC.stw(0, 0x104, 1))
        self.write_instruction(PPC.bl(0x805174fc, self.write_pointer))
        self.write_instruction(PPC.bl(0x80399af0, self.write_pointer))

        self.add_deathlink()
        
        # Return from custom function
        self.write_pointer = self.custom_section_address + self.custom_section_size - 5 * 0x4 - variable_space
        self.write_instruction(PPC.bl(0x80517548, self.write_pointer))
        self.write_instruction(PPC.lwz(0, 0x104, 1))
        self.write_instruction(PPC.mtlr(0))
        self.write_instruction(PPC.addi(1, 1, 0x100))
        self.write_instruction(PPC.blr())

    @staticmethod
    def rlwinm(rA: int, rS: int, sh: int, mb: int, me: int) -> bytes:
        """rlwinm rA, rS, SH, MB, ME  - rotate rS left by SH bits, AND with mask(MB, ME), store in rA"""
        return PPC._fmt_m(21, rS, rA, sh, mb, me)

    def write_instruction(self, instruction_bytes: bytes, address: int = None) -> None:
        if address is not None:
            self.write_pointer = address

        self.dol.write_at(self.write_pointer, instruction_bytes)
        self.write_pointer += 4

    def write_nop(self, count: int) -> None:
        for _ in range(count):
            self.write_instruction(PPC.nop())

    def get_upper_and_lower_unsigned(self, address: int) -> list[int, int]:
        return (address & 0xFFFF0000) >> 16, address & 0x0000FFFF

    def get_upper_and_lower_signed(self, address: int) -> list[int, int]:
        if address & 0x0000FFFF >= 0x8000:
            return ((address & 0xFFFF0000) >> 16) + 1, (address & 0x0000FFFF) - 0x10000
        return (address & 0xFFFF0000) >> 16, address & 0x0000FFFF

    def add_deathlink(self):
        upper, lower = self.get_upper_and_lower_signed(self.custom_section_address + STATIC_VARIABLE_OFFSETS[DEATHLINK])
        self.write_instruction(PPC.lis(31, upper))
        self.write_instruction(PPC.lbz(3, lower, 31))

        # Skip the function if its less than 1
        self.write_instruction(PPC.cmpi(0, 3, 1))
        self.write_instruction(PPC.bc(12, 0, self.write_pointer + 4 * 0x4, self.write_pointer))

        # Kill mario and reset
        self.write_instruction(PPC.bl(0x803f1e74, self.write_pointer))
        self.write_instruction(PPC.li(3, 0))
        self.write_instruction(PPC.stb(3, lower, 31))

    def skip_opening(self):
        #######################################################
        # Skip opening cutscene and go immediately to gateway #
        #######################################################
        # Let powerstarlist load all galaxies (to avoid crash)
        self.write_instruction(PPC.nop(), 0x80379248)

        # Properly calculate the observatory scenario
        self.write_instruction(PPC.li(3, 6), 0x803bbb2c)
        self.write_instruction(PPC.bl(0x803af884, self.write_pointer))

        self.write_instruction(PPC.li(3, 2), 0x803bbb78)
        self.write_instruction(PPC.bl(0x803af884, self.write_pointer))
        self.write_instruction(PPC.cmpi(0, 3, 1))

        # Overwrite flag type 5
        self.write_instruction(PPC.lbz(3, 0x6, 30), 0x803b38cc)
        self.write_instruction(PPC.bl(0x803af884, self.write_pointer))
        self.write_nop(1)

        # TEMPORARY
        # Set flag conditions for "SpecialGrandStar[i]"
        address = 0x8053bb40
        for i in range(7):
            self.dol.write_at(address + i * 0x14 + 4, b'\x05')
            self.dol.write_at(address + i * 0x14 + 6, i.to_bytes())

    def set_swing_permission(self):
        ########################
        # Set swing permission #
        ########################
        self.write_instruction(PPC.li(3, 1), 0x803b55b0)

    def manipulate_miniature_orbit(self):
        #######################################
        # Miniature galaxy orbit manipulation #
        #######################################
        # Get obj_arg0 from miniature galaxy
        self.write_instruction(PPC.lwz(3, 0x8C, 31), 0x80200758)
        self.write_instruction(self.rlwinm(3, 3, 16, 0x10, 0x1F))

    def manipulate_arg0_loading(self):
        self.write_instruction(PPC.lhz(0, 0x8E, 3), 0x801feda8)
        self.write_instruction(PPC.lhz(30, 0x10, 1), 0x801feedc)
        self.write_instruction(PPC.lhz(0, 0x8E, 3), 0x801ff338)
        self.write_instruction(PPC.lhz(0, 0x8E, 31), 0x801ff4c8)
        self.write_instruction(PPC.lhz(0, 0x8E, 29), 0x801ff8d8)
        self.write_instruction(PPC.lhz(0, 0x8E, 29), 0x801ff940)
        self.write_instruction(PPC.lhz(0, 0x8E, 31), 0x801ff9b0)
        self.write_instruction(PPC.lhz(0, 0x8E, 31), 0x801ffa60)
        self.write_instruction(PPC.lhz(0, 0x8E, 3), 0x801ffc44)

    def manipulate_star_loading(self):
        ################################
        # Scenario select star loading #
        ################################
        # Keep loading regular stars even if they're not available yet
        self.write_instruction(PPC.li(3, 1), 0x8037d9ec)

        # Calculate all secret/comet stars, including possibly normally unavailable ones
        self.write_instruction(PPC.li(3, 1), 0x8037da44)

        # Show secret/comet stars as calculated above
        self.write_instruction(PPC.li(3, 1), 0x8037db54)

        # Set visibility to 1 (not collected) if appearing as collected has failed (ensuring it shows up even if not available)
        self.write_instruction(PPC.li(6, 1), 0x8037db18)

        # Always show up and appear correctly as collected/not collected
        self.write_instruction(PPC.li(6, 1), 0x8037db74)

    def read_star_count(self):
        #######################################
        # Read star count from memory address #
        #######################################
        # Load upper 2 bytes of memory pointer (0x8000)
        upper, lower = self.get_upper_and_lower_signed(self.custom_section_address + STATIC_VARIABLE_OFFSETS[POWER])
        self.write_instruction(PPC.lis(3, upper), 0x803b10fc)

        # Load lower 2 bytes of memory pointer (0x1880), and load the byte at 0x80001880 into r3
        self.write_instruction(PPC.lbz(3, lower, 3))

        # Skip the rest of the normal function
        self.write_instruction(PPC.b(0x803b113c, self.write_pointer))

    def custom_powerstar_colour_loading(self):
        ###################################
        # Custom powerstar colour loading #
        ###################################
        upper, lower = self.get_upper_and_lower_unsigned(self.custom_section_address + STATIC_VARIABLE_OFFSETS[STARCOLOUR])
        self.write_instruction(PPC.stw(31, 0xC, 1), 0x8020f26c)
        self.write_instruction(PPC.addi(31, 3, -0x1))
        self.write_instruction(PPC.bl(0x803f5ab8, self.write_pointer))
        self.write_instruction(PPC.mr(4, 3))
        self.write_instruction(PPC.bl(0x803b0544, self.write_pointer))
        self.write_instruction(PPC.lwz(3, 0xC, 3))
        self.write_instruction(PPC.bl(0x803b1390, self.write_pointer))
        self.write_instruction(PPC.mulli(3, 3, 0x8))
        self.write_instruction(PPC.lis(4, upper))
        self.write_instruction(PPC.ori(4, 4, lower))
        self.write_instruction(PPC.add(3, 3, 4))
        self.write_instruction(PPC.lbzx(3, 3, 31))
        self.write_instruction(PPC.lwz(31, 0xC, 1))
        self.write_instruction(PPC.lwz(0, 0x14, 1))

    def custom_grandstar_count(self):
        ##################################
        # Custom grandstar count loading #
        ##################################
        upper, lower = self.get_upper_and_lower_signed(self.custom_section_address + STATIC_VARIABLE_OFFSETS[GRAND])
        self.write_instruction(PPC.lis(3, upper), 0x803b1d08)
        self.write_instruction(PPC.lbz(3, lower, 3))
        self.write_instruction(PPC.addi(4, 4, -0x1))
        self.write_instruction(PPC.cmp(0, 3, 4))
        self.write_instruction(PPC.bc(12, 0, self.write_pointer + 3 * 0x4, self.write_pointer))
        self.write_instruction(PPC.li(3, 1))
        self.write_instruction(PPC.b(self.write_pointer + 2 * 0x4, self.write_pointer))
        self.write_instruction(PPC.li(3, 0))
        self.write_nop(11)

    def skip_wii_strap(self):
        #########################
        # Skip wii strap screen #
        #########################
        self.write_instruction(PPC.addi(4, 13, -0x3080), 0x80340408)
        self.write_instruction(PPC.li(4, 1), 0x803406ac)
        self.write_instruction(PPC.li(4, 2), 0x803406d0)

    def show_bros_button(self):
        #################################################
        # Show the bros button to select Mario or Luigi #
        #################################################
        self.write_instruction(PPC.li(3, 1), 0x8017cd70)

    def custom_green_star_count(self):
        upper, lower = self.get_upper_and_lower_signed(self.custom_section_address + STATIC_VARIABLE_OFFSETS[GREEN])
        self.write_instruction(PPC.lis(3, upper), 0x803ccaa0)
        self.write_instruction(PPC.lbz(3, lower, 3))

    def initialise_star_colours(self, locations: dict):
        star_colour_address = self.custom_section_address + STATIC_VARIABLE_OFFSETS[STARCOLOUR]

        for location, data in locations.items():
            scenario = location_table[location].game_address

            if scenario == None:
                continue

            in_game_name = region_list[location_table[location].region].in_game_name

            for galaxy in galaxies_list:
                region = region_list[galaxy]
                if in_game_name == region.in_game_name:
                    galaxy_offset = region.region_offset * 2
                    break

            classification = ItemClassification[data["classification"]]
            self.dol.write_at(star_colour_address + galaxy_offset + scenario, FILL_TYPE_TO_COLOUR_INDEX[classification].to_bytes())

    def update_instructions(self):
        self.skip_opening()
        self.set_swing_permission()
        self.manipulate_miniature_orbit()
        self.manipulate_arg0_loading()
        self.manipulate_star_loading()
        self.read_star_count()
        self.custom_powerstar_colour_loading()
        self.custom_grandstar_count()
        self.skip_wii_strap()
        self.show_bros_button()

    def show_galaxy_star_counter(self):
        self.write_instruction(PPC.cmpi(0, 3, 4), 0x801ff4cc)

    def hide_galaxy_star_counter(self):
        self.write_pointer = 0x801ff4cc
        self.write_instruction(PPC.b(self.write_pointer + 85 * 0x4, self.write_pointer))

    def update(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination], dome_shuffle: dict[int, int], star_requirements: dict[str, int], locations: dict, show_galaxies: int):
        for object_name, object in self.objects.items():
            print(f"Updating {object_name}")

            object.update(miniature_galaxy_names=[galaxy.name for galaxy in dome_galaxies],
                          surprised_galaxy_names=[galaxy.name for galaxy in luma_galaxies],
                          dome_shuffle=dome_shuffle,
                          dome_galaxies=dome_galaxies,
                          star_requirements=star_requirements)

        self.initialise_star_colours(locations)

        self.update_instructions()

        if show_galaxies == 0:
            self.show_galaxy_star_counter()
        elif show_galaxies == 2:
            self.hide_galaxy_star_counter()
