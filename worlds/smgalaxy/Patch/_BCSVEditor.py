from operator import index
import os
import struct
from hashtable import convert_hash_or_name

class BCSVField:
    def __init__(self, data: bytes = b''):
        if data:
            self.set_field(data)
        else:
            self.hash = 0
            self.bitmask = 0
            self.offset = 0
            self.shift = 0
            self.type = 0
            self.name = ''
    
    def set_field(self, data):
        """Sets the field data
        """
        # Check if data length is 12 bytes and set the field attributes based on the data
        if len(data) != 12:
            raise ValueError("Data must be exactly 12 bytes long.")
        self.hash = int.from_bytes(data[0:4], byteorder='big')
        self.bitmask = int.from_bytes(data[4:8], byteorder='big')
        self.offset = int.from_bytes(data[8:10], byteorder='big')
        self.shift = int.from_bytes(data[10:11], byteorder='big')
        self.type = int.from_bytes(data[11:12], byteorder='big')
        self.name = convert_hash_or_name(self.hash)
        return self
    
    def get_field(self):
        """Returns the field data as bytes.
        """
        # Convert the field attributes to bytes and concatenate them to form the field data
        data = self.hash.to_bytes(4, byteorder='big')
        data += self.bitmask.to_bytes(4, byteorder='big')
        data += self.offset.to_bytes(2, byteorder='big')
        data += self.shift.to_bytes(1, byteorder='big')
        data += self.type.to_bytes(1, byteorder='big')
        return data

    def get_type(self):
        """Returns the type of the field as a string.
        """
        # Define the field types based on the type value
        types = {0: 'LONG', 1: 'STRING', 2: 'FLOAT', 3: 'LONG_2', 4: 'SHORT', 5: 'CHAR', 6: 'STRING_OFFSET'}
        return types.get(self.type, 'unknown')
    
    def get_pack_format(self):
        """Returns the struct pack format for the field type.
        """
        # Define the struct pack formats for each field type
        formats = {0: 'I', 1: 'c'*32, 2: 'f', 3: 'I', 4: 'H', 5: 'B', 6: 'I'}
        return formats.get(self.type, '')

    def get_type_size(self):
        """Returns the size of the field type in bytes.
        """
        # Define the sizes for each field type
        sizes = {0: 4, 1: 32, 2: 4, 3: 4, 4: 2, 5: 1, 6: 4}
        return sizes.get(self.type, 0)

    def get_default_value(self):
        """Returns the default value for the field type.
        """
        # Define default values for each field type
        defaults = {0: 0, 1: b'\x00'*32, 2: 0.0, 3: 0, 4: 0, 5: 0, 6: 0}
        return defaults.get(self.type, None)

    def get_order(self):
        """Returns the ordering of this field compared to another field.
        """
        # Define the order of the field types for sorting purposes
        order = ['STRING', 'FLOAT', 'LONG', 'LONG_2', 'SHORT', 'CHAR', 'STRING_OFFSET']
        return order.index(self.get_type())

    def __str__(self):
        return f"Field Name: {self.name}\nHash: {self.hash}\nBitmask: {self.bitmask}\nOffset: {self.offset}\nShift: {self.shift}\nType: {self.get_type()}"

class BCSVEntry:
    def __init__(self, fields: BCSVField = [], data: bytes = b''):
        self.fields = fields
        self.sorted_fields = sorted(self.fields, key=lambda field: field.offset)
        self.values = [field.get_default_value() for field in self.fields]

        if data:
            self.set_entry_values(data)
        return

    def add_field(self, field: BCSVField, index: int = None):
        """Adds a field to the entry.
        """
        # Insert the field at the specified index and sort the fields by their offset
        self.fields.insert(index if index is not None else len(self.fields), field)
        self.sort_fields()
        
        # Find the maximum offset according to the field order
        max_offset = 0
        for sorted_field in self.sorted_fields:
            if field.get_order() >= sorted_field.get_order():
                max_offset = sorted_field.offset + sorted_field.get_type_size()
            else:
                break
        field.offset = max_offset

        # Adjust every offset after the added field
        for sorted_field in self.sorted_fields:
            if sorted_field.get_order() > field.get_order():
                sorted_field.offset += field.get_type_size()

        # Add default value for the new field
        self.values.insert(index if index is not None else len(self.values), field.get_default_value())
        return field

    def remove_field(self, index: int):
        """Removes the field at the specified index.
        """
        self.fields.pop(index) # Remove the field from the fields list

    def sort_fields(self):
        """Sorts the fields by their offset.
        """
        # Sort the fields by their offset and update the sorted_fields list
        self.sorted_fields = self.fields.copy()
        self.sorted_fields.sort(key=lambda field: field.offset)
        return self.sorted_fields
    
    def get_name(self):
        """Returns the name of the entry.
        """
        # Search for the field with the name 'name' and return its value
        for i, field in enumerate(self.fields):
            if field.name == 'name':
                return self.values[i]
        raise ValueError("No Field with name could be found.")

    def set_value(self, field_name: str, value):
        """Sets the value of a field in the entry.
        """
        # Search for the field with the given name and set its value
        for i, field in enumerate(self.fields):
            if field.name == field_name:
                self.values[i] = value
                return
        raise ValueError(f"Field with name '{field_name}' not found.")

    def set_entry_values(self, data):
        """Sets the entry values from the given data bytes.
        """
        # Iterate through the fields and extract the corresponding value from the data based on the field type
        for i, field in enumerate(self.fields):
            value = data[field.offset:field.offset + field.get_type_size()]
            if field.type == 0 or field.type == 3 or field.type == 6:  # LONG, LONG_2, STRING_OFFSET
                self.values[i] = int.from_bytes(value, byteorder='big', signed=True) # Convert to signed integer
            elif field.type == 1:  # STRING
                self.values[i] = value.rstrip(b'\x00').decode('utf-8')  # Remove padding null bytes and decode to string
            elif field.type == 2:  # FLOAT
                self.values[i] = struct.unpack('>f', value)[0]  # Big-endian float
            elif field.type == 4:  # SHORT
                self.values[i] = int.from_bytes(value, byteorder='big', signed=True) # Convert to signed short
            elif field.type == 5:  # CHAR
                self.values[i] = int.from_bytes(value, byteorder='big', signed=True) # Convert to signed char
        return
    
    def get_entry(self):
        """Returns the entry data as bytes.
        """
        # Build the struct pack format string and convert the field values to bytes based on their types for packing
        pack_format = ''
        for i, field in enumerate(self.sorted_fields):
            pack_format += field.get_pack_format() # Build the struct pack format string based on the field types
            
            # Convert signed to unsigned for packing
            if field.type in [0, 3, 4, 5]:  # LONG, LONG_2, SHORT, CHAR
                if self.values[i] < 0:
                    self.values[i] = int.to_bytes(self.values[i], field.get_type_size(), 'big', signed=True) # Convert to bytes and back to int to get the unsigned value
                else:
                    self.values[i] = int.to_bytes(self.values[i], field.get_type_size(), 'big', signed=False) # Convert to bytes for packing
            elif field.type == 1:  # STRING
                self.values[i] = self.values[i].encode('utf-8') + b'\x00' * (32 - len(self.values[i]))  # Encode to bytes and add padding null bytes
            elif field.type == 2:  # FLOAT
                self.values[i] = struct.pack('>f', self.values[i])  # Pack as big-endian float
            elif field.type == 6:  # STRING_OFFSET
                self.values[i] = int.to_bytes(self.values[i], 4, byteorder='big', signed=False)  # Convert to bytes for packing
        
        # Convert back into unsigned integers for packing
        for i in range(len(self.values)):
            self.values[i] = int.from_bytes(self.values[i], byteorder='big', signed=False)
        return struct.pack(pack_format, *self.values)

    def __str__(self):
        # Calculate the maximum length for each field value and name for formatting
        max_lengths = [max(len(str(self.values[i])), len(field.name)) for i, field in enumerate(self.fields)]

        # Create the header row with field names, the separator row, and the value row
        out = ' | '.join(f"{self.fields[i].name:<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'
        out += '-|-'.join('-' * max_lengths[i] for i in range(len(self.fields))) + '\n'
        out += ' | '.join(f"{str(self.values[i]):<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'
        return out

class BCSVFile:
    def __init__(self, file: str = ''):
        self.entries = []
        self.fields = []
        self.strings = []
        self.string_offsets = []

        if file:
            self.load_from_file(file)
        else:
            self.entry_count = 0
            self.field_count = 0
            self.offset = 0
            self.entry_size = 0

    def add_field(self, data: bytes):
        """Adds a field to the BCSV file.
        """
        # Check if data length is 12 bytes and add the field to the fields list
        if len(data) != 12:
            raise ValueError("Data must be exactly 12 bytes long.")
        field = BCSVField(data)
        self.fields.append(field)

        # Update offset based on newly added field
        self.offset += field.get_type_size() * len(self.entries)

        # Add the new field to all existing entries
        for entry in self.entries:
            entry.add_field(field)
        return field

    def remove_field(self, index: int):
        """Removes the field at the specified index.
        """
        # Check if index is within bounds
        if index < 0 or index >= len(self.fields):
            raise IndexError("Index out of range.")
        
        # Adjust offset based on removed field
        self.offset -= self.fields[index].get_type_size() * len(self.entries) 
        
        # Remove the field and adjust offsets for remaining fields
        removed_field = self.fields[index]
        self.fields.pop(index)
        for entry in self.entries:
            entry.remove_field(index) # Remove the field from each entry and adjust offsets for remaining fields in the entry
        return removed_field
    
    def get_field_by_index(self, index: int):
        """Returns the field at the specified index.
        """
        # Check if index is within bounds and return the field
        if index < 0 or index >= len(self.fields):
            raise IndexError("Index out of range.")
        return self.fields[index]
    
    def get_field_by_name(self, name: str):
        """Returns the field with the specified name.
        """
        # Search for the field with the given name and return it
        for field in self.fields:
            if field.name == name:
                return field
        raise ValueError(f"Field with name '{name}' not found.")

    def replace_field(self, index: int, field: BCSVField):
        """Replaces the field at the specified index with the given field.
        """
        # Check if index is within bounds and replace the field
        if index < 0 or index >= len(self.fields):
            raise IndexError("Index out of range.")
        self.fields[index] = field
        return field

    def add_entry(self, data: bytes):
        """Adds an entry to the BCSV file.
        """
        # Check if data length matches the expected entry size
        if len(data) != self.entry_size:
            raise ValueError(f"Data must be exactly {self.entry_size} bytes long.")
        
        entry = BCSVEntry(self.fields, data)
        self.entries.append(entry)
        return entry

    def remove_entry(self, index: int):
        """Removes the entry at the specified index.
        """
        # Check if index is within bounds and remove the entry
        if index < 0 or index >= len(self.entries):
            raise IndexError("Index out of range.")
        return self.entries.pop(index)

    def get_entry_by_index(self, index: int):
        """Returns the entry at the specified index.
        """
        # Check if index is within bounds and return the entry
        if index < 0 or index >= len(self.entries):
            raise IndexError("Index out of range.")
        return self.entries[index]

    def get_string_by_offset(self, offset: int):
        """Returns the string at the specified offset.
        """
        # Find the index of the string offset and return the corresponding string
        if offset in self.string_offsets:
            index = self.string_offsets.index(offset)
            return self.strings[index]
        else:
            raise ValueError(f"String with offset '{offset}' not found.")

    def update_strings(self):
        """Updates the strings list based on the current entries and their string offset fields.
        """
        # Clear the current strings list and repopulate it based on the string offset fields in the entries
        self.strings = []
        for entry in self.entries:
            for field in entry.fields:
                if field.type == 6: # STRING_OFFSET
                    index = entry.fields.index(field) # Get index of the field in the entry
                    string_value = entry.values[index] # Get the string value for the field
                    if string_value not in self.strings:
                        self.strings.append(string_value) # Add string to strings list if it's not already there
        return self.strings

    def load_from_file(self, file: str):
        """"Loads a BCSV file from the specified path.
        """
        # Read the file data
        try:
            with open(file, 'rb') as f:
                data = f.read()
        except:
            raise Exception(f"Failed to read file: {file}")
        
        # Check if file size is a multiple of 32 bytes
        if len(data) % 32 != 0:
            raise ValueError("File size must be padded to a multiple of 32 bytes.")

        # Parse header
        header = data[:16]
        self.entry_count = int.from_bytes(header[0:4], byteorder='big')
        self.field_count = int.from_bytes(header[4:8], byteorder='big')
        self.offset = int.from_bytes(header[8:12], byteorder='big')
        self.entry_size = int.from_bytes(header[12:16], byteorder='big')

        # Setup field, entry, and string data
        field_data = data[16:16 + self.field_count * 12]
        entry_data = data[self.offset:self.offset + self.entry_count * self.entry_size]
        strings_data = data[self.offset + self.entry_count * self.entry_size:]

        # Parse fields
        for i in range(self.field_count):
            field_bytes = field_data[i*12:(i+1)*12]
            self.add_field(field_bytes)
        
        # Parse entries
        for i in range(self.entry_count):
            entry_bytes = entry_data[i*self.entry_size:(i+1)*self.entry_size]
            self.add_entry(entry_bytes)

        # Parse strings
        strings = strings_data.split(b'\x00')[:-1]  # Last string is padding
        self.strings = [string.decode('utf-8') for string in strings]

        # Setup string offsets
        self.calculate_string_offsets_and_update_entries()

    def write_to_file(self, file: str, overwrite: bool = False):
        """Writes the BCSV file to the specified path.
        """
        self.update_strings() # Update strings list based on current entries

        out = b''
            # Write header
        out += self.entry_count.to_bytes(4, byteorder='big')
        out += self.field_count.to_bytes(4, byteorder='big')
        out += self.offset.to_bytes(4, byteorder='big')
        out += self.entry_size.to_bytes(4, byteorder='big')

        # Write fields
        for field in self.fields:
            out += field.get_field()

        # Write entries
        for entry in self.entries:
            out += entry.get_entry()

        # Write strings
        for string in self.strings:
            out += string.encode('utf-8') + b'\x00'
        
        # Add padding to make file size a multiple of 32 bytes
        padding = 32 - (len(out) % 32)
        out += b'@' * padding

        # Check if file already exists and handle overwrite option
        if os.path.exists(file) and not overwrite:
            raise Exception(f"File already exists: {file}")
        
        # Write the output to the file
        try:
            with open(file, 'wb') as f:
                f.write(out)
        except:
            raise Exception(f"Failed to write file: {file}")

    def __str__(self):
        # Calculate the maximum length for each field value and name for formatting
        max_lengths = [max(len(str(entry.values[i])) for entry in self.entries) for i in range(len(self.fields))]
        max_lengths = [max(max_lengths[i], len(self.fields[i].name)) for i in range(len(self.fields))]

        # Create the header row with field names, the separator row, and the value rows for each entry
        out = ' | '.join(f"{self.fields[i].name:<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'

        for entry in self.entries:
            out += '-|-'.join('-' * max_lengths[i] for i in range(len(self.fields))) + '\n'
            out += ' | '.join(f"{str(entry.values[i]):<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'
        return out

if __name__ == "__main__":
    bcsv = BCSVFile('a')
    
    entry = bcsv.get_entry_by_index(3)

    entry.set_value('name', 'MiniHoneyBeeKingdomGalaxy')

    bcsv.write_to_file('test')