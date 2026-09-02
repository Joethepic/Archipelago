from io import BytesIO

from wiithon.ppc import instructions as PPC
from wiithon.formats.dol import DOL

from worlds.smgalaxy.Patch.extensions import SMGObject, SMGDOLObject, Pointer, CharPointer
from .SMGDolObjects.NameObjFactory import NameObjFactory
from .SMGDolObjects.GalaxyUnlockTable import GalaxyUnlockTable
from ..Constants.patch_constants import *


class AstroDomeModels(SMGDOLObject):
    astro_dome: list[CharPointer]
    astro_dome_sky: list[CharPointer]
    astro_dome_entrance: list[CharPointer]
    astro_star_plate: list[CharPointer]

    def __init__(self):
        self.astro_dome_address: int = ASTRO_DOME_ARRAY_ADDRESS
        self.astro_dome_sky_address: int = ASTRO_DOME_SKY_ARRAY_ADDRESS
        self.astro_dome_entrance_address: int = ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS
        self.astro_star_plate_address: int = ASTRO_STAR_PLATE_ARRAY_ADDRESS

        self.astro_dome = []
        self.astro_dome_sky = []
        self.astro_dome_entrance = []
        self.astro_star_plate = []
        
        for index in range(6):
            offset = index * 0x4
            astro_dome_pointer = CharPointer(self.astro_dome_address + offset)
            astro_dome_sky_pointer = CharPointer(self.astro_dome_sky_address + offset)
            astro_dome_entrance_pointer = CharPointer(self.astro_dome_entrance_address + offset)
            astro_star_plate_pointer = CharPointer(self.astro_star_plate_address + offset)

            self.astro_dome.append(astro_dome_pointer)
            self.astro_dome_sky.append(astro_dome_sky_pointer)
            self.astro_dome_entrance.append(astro_dome_entrance_pointer)
            self.astro_star_plate.append(astro_star_plate_pointer)
    
    def shuffle_list(self, pointer_list: list[CharPointer], shuffle: dict[int, int]):
        assert len(pointer_list) == 6
        
        reverse_shuffle: dict[int, int] = {value: key for key, value in shuffle.items()}
        addresses: list[int] = [pointer_list[i].pointing_address for i in range(6)]

        for index, address in enumerate(addresses):
            new_index = reverse_shuffle[index + 1] - 1
            pointer_list[new_index].pointing_address = address
            pointer_list[new_index].write_pointer()
    
    def update(self, dome_shuffle: dict[int, int], **kwargs):
        self.shuffle_list(self.astro_dome_entrance, dome_shuffle)
        self.shuffle_list(self.astro_dome, dome_shuffle)
        self.shuffle_list(self.astro_dome_sky, dome_shuffle)

class SMGDOL(SMGObject):
    data: BytesIO
    custom_section_size: int = 0x1000
    custom_section_address: int

    objects: dict[str, SMGDOLObject]

    write_pointer: int

    def __init__(self, dol: DOL):
        super().__init__(None)
        self.dol: DOL = dol
        self.data = BytesIO(self.dol.to_bytes())

        Pointer.dol = self.dol
        SMGDOLObject.dol = self.dol

        self.objects = {
            "NameObjectFactory": NameObjFactory(),
            "GalaxyUnlockTable": GalaxyUnlockTable(),
            #"AstroDomeModels": AstroDomeModels()
        }

        self.write_pointer = 0

        size, addrs = self.dol.inject_above_arena([PPC.nop() * int(self.custom_section_size/4)])
        self.custom_section_address = addrs[0]

        extra_space = 0x100

        # Return custom function
        self.write_pointer = self.custom_section_address + self.custom_section_size - 5 * 0x4 - extra_space
        self.write_instruction(PPC.bl(0x80517548, self.write_pointer))
        self.write_instruction(PPC.lwz(0, 0x104, 1))
        self.write_instruction(PPC.mtlr(0))
        self.write_instruction(PPC.addi(1, 1, 0x100))
        self.write_instruction(PPC.blr())

        # Setup custom function
        self.write_instruction(PPC.stwu(1, -0x100, 1), self.custom_section_address)
        self.write_instruction(PPC.mflr(0))
        self.write_instruction(PPC.stw(0, 0x104, 1))
        self.write_instruction(PPC.bl(0x805174fc, self.write_pointer))
        self.write_instruction(PPC.bl(0x80399af0, self.write_pointer))

        self.add_deathlink()

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

    def add_deathlink(self):
        # Load address from 0x80001af0
        self.write_instruction(PPC.lis(31, -0x8000))
        self.write_instruction(PPC.lbz(3, 0x1af0, 31))

        # Skip the function if its zero
        self.write_instruction(PPC.cmpi(0, 3, 0))
        self.write_instruction(PPC.bc(4, 0, self.write_pointer + 4 * 0x4, self.write_pointer))

        # Kill mario and reset
        self.write_instruction(PPC.bl(0x803f1e74, self.write_pointer))
        self.write_instruction(PPC.li(3, 0))
        self.write_instruction(PPC.stb(3, 0x1AF0, 31))

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
        self.write_instruction(PPC.lis(3, -0x8000), 0x803b10fc)

        # Load lower 2 bytes of memory pointer (0x1880), and load the byte at 0x80001880 into r3
        self.write_instruction(PPC.lbz(3, 0x1880, 3))

        # Skip the rest of the normal function
        self.write_instruction(PPC.b(0x803b113c, self.write_pointer))

    def custom_powerstar_colour_loading(self):
        ###################################
        # Custom powerstar colour loading #
        ###################################
        self.write_instruction(PPC.stw(31, 0xC, 1), 0x8020f26c)
        self.write_instruction(PPC.addi(31, 3, -0x1))
        self.write_instruction(PPC.bl(0x803f5ab8, self.write_pointer))
        self.write_instruction(PPC.mr(4, 3))
        self.write_instruction(PPC.bl(0x803b0544, self.write_pointer))
        self.write_instruction(PPC.lwz(3, 0xC, 3))
        self.write_instruction(PPC.bl(0x803b1390, self.write_pointer))
        self.write_instruction(PPC.mulli(3, 3, 0x8))
        self.write_instruction(PPC.lis(4, -0x8000))
        self.write_instruction(PPC.ori(4, 4, 0x1900))
        self.write_instruction(PPC.add(3, 3, 4))
        self.write_instruction(PPC.lbzx(3, 3, 31))
        self.write_instruction(PPC.lwz(31, 0xC, 1))
        self.write_instruction(PPC.lwz(0, 0x14, 1))

    def custom_grandstar_count(self):
        ##################################
        # Custom grandstar count loading #
        ##################################
        self.write_instruction(PPC.lis(3, -0x8000), 0x803b1d08)
        self.write_instruction(PPC.lbz(3, 0x1882, 3))
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

    def hook_to_custom_function(self):
        ####################
        # Custom Functions #
        ####################
        # Jump to custom section
        self.write_pointer = 0x803995c0
        self.write_instruction(PPC.b(self.custom_section_address, self.write_pointer))

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
        self.hook_to_custom_function()

    def update(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination], dome_shuffle: dict[int, int], star_requirements: dict[str, int]):
        for object_name, object in self.objects.items():
            print(f"Updating {object_name}")

            object.update(miniature_galaxy_names=[galaxy.name for galaxy in dome_galaxies],
                          surprised_galaxy_names=[galaxy.name for galaxy in luma_galaxies],
                          dome_shuffle=dome_shuffle,
                          dome_galaxies=dome_galaxies,
                          star_requirements=star_requirements)

        self.update_instructions()
