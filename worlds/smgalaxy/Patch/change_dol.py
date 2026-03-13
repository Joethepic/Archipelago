from gclib.dol import DOL
from gclib import fs_helpers as fs
from io import BytesIO

def replace_instruction(dol: DOL, address: int, old_instruction: bytes, new_instruction: bytes, verbose: bool = True):
    if len(old_instruction) != 4 or len(new_instruction) != 4:
        raise ValueError(f"Instructions must be of length 4. Old instruction: {old_instruction.hex()}, new instruction: {new_instruction.hex()}")
    
    instruction = read_from_dol(dol, address, 4)
    if old_instruction != instruction:
        raise ValueError(f"Old instruction does not match instruction at address 0x{hex(address)}. Old instruction: {old_instruction.hex()}, instruction at address: {instruction.hex()}")

    write_to_dol(dol, address, new_instruction, verbose)

def read_from_dol(dol: DOL, address: int, size: int):
    return dol.read_data(read_callback, address, size)

def read_pointer_from_dol(dol: DOL, address: int):
    pointer = int.from_bytes(read_from_dol(dol, address, 4))
    if not is_pointer(dol, pointer):
        raise TypeError(f"Pointer could not be found at address: {int.to_bytes(address).hex()}")
    return pointer

def read_string_from_dol(dol: DOL, address: int):
    offset = dol.convert_address_to_offset(address)
    return fs.read_str_until_null_character(dol.data, offset)

def read_string_from_pointer(dol: DOL, address: int):
    pointer = read_pointer_from_dol(dol, address)
    return read_string_from_dol(dol, pointer)

def read_callback(data: BytesIO, offset: int, size: int):
    return fs.read_bytes(data, offset, size)

def write_to_dol(dol: DOL, address: int, write_bytes: bytes, verbose: bool = True):
    if verbose:
        print(f"Replaced at address 0x{int.to_bytes(address,4).hex()}: " + read_from_dol(dol, address, len(write_bytes)).hex(), end='')
    
    dol.write_data(write_callback, address, write_bytes)
    
    if verbose:
        print(" with " + read_from_dol(dol, address, len(write_bytes)).hex())

def write_pointer_to_dol(dol: DOL, address: int, pointer: int, verbose: bool = True):
    bytes_pointer = int.to_bytes(pointer, 4)
    if not is_pointer(dol, pointer):
        raise TypeError(f"Not a valid pointer: 0x{bytes_pointer.hex()}")
    
    write_to_dol(dol, address, bytes_pointer, verbose)

def write_string_to_dol(dol: DOL, address: int, string: str, verbose: bool = True):
    write_to_dol(dol, address, string.encode('shift-jis'), verbose)

def write_callback(data: BytesIO, offset: int, write_bytes: bytes):
    fs.write_bytes(data, offset, write_bytes)

def is_pointer(dol: DOL, pointer: int):
    try:
        dol.convert_address_to_offset(pointer)
        return True
    except:
        return False

def get_dol(dol_path: str):
    dol = DOL()
    dol_file = open(dol_path, 'rb+')
    dol.read(dol_file)
    return dol

if __name__ == "__main__":
    dol_path = r"temp/DATA/sys/main.dol"
    dol = get_dol(dol_path)
    
    #replace_instruction(dol, 0x801ffc44, b'\x80\x03\x00\x8c', b'\x38\x00\x00\x02')
    replace_instruction(dol, 0x805380a4, b'\x80\x59\x81\x9a', b'\x80\x59\x84\x3d')