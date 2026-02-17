import struct
from hashtable import hash_to_name

class BCSVField:
    """Represents a field in a BCSV file, containing information about the field's hash, bitmask, offset, shift, and type.
    """
    def __init__(self, data: bytes):
        self.data = data
        self.hash = int.from_bytes(self.data[0:4], byteorder='big')
        self.bitmask = int.from_bytes(self.data[4:8], byteorder='big')
        self.offset = int.from_bytes(self.data[8:10], byteorder='big')
        self.shift = int.from_bytes(self.data[10:11], byteorder='big')
        self.type = int.from_bytes(self.data[11:12], byteorder='big')

        self.name = hash_to_name[int.to_bytes(self.hash, 4, 'big')]

    def get_value_from_bytes(self, byte_value: bytes):
        """Returns the value of the field from the given byte value based on the field type.
        """
        return struct.unpack('>' + self.get_value_format(), byte_value)[0]

    def get_value(self, entry_data: bytes):
        """Returns the value of the field from the given entry data.
        """
        field_data = entry_data[self.offset: self.offset + self.get_value_size()]
        value = (int.from_bytes(field_data, byteorder='big') & self.bitmask) >> self.shift
        byte_value = int.to_bytes(value, self.get_value_size(), byteorder='big')
        return self.get_value_from_bytes(byte_value)

    def get_value_size(self):
        """Returns the size of the value based on the field type.
        """
        if self.type == 0: # LONG
            return 4
        elif self.type == 1: # STRING
            return 32
        elif self.type == 2: # FLOAT
            return 4
        elif self.type == 3: # LONG_2
            return 4
        elif self.type == 4: # SHORT
            return 2
        elif self.type == 5: # CHAR
            return 1
        elif self.type == 6: # STRING_OFFSET
            return 4
        else:
            raise ValueError(f"Unknown field type: {self.type}")
    
    def get_value_format(self):
        """Returns the struct format character for the field type.
        """
        if self.type == 0: # LONG
            return 'i'
        elif self.type == 1: # STRING
            return 'c'*32
        elif self.type == 2: # FLOAT
            return 'f'
        elif self.type == 3: # LONG_2
            return 'i'
        elif self.type == 4: # SHORT
            return 'h'
        elif self.type == 5: # CHAR
            return 'b'
        elif self.type == 6: # STRING_OFFSET
            return 'I'
        else:
            raise ValueError(f"Unknown field type: {self.type}")
    
    def __str__(self):
        return f"Name = {self.name}\nHash = {self.hash}\nBitmask = {self.bitmask}\nOffset = {self.offset}\nShift = {self.shift}\nType = {self.type}"
    
class BCSVEntry:
    """Represents an entry in a BCSV file, containing the entry data and the values of the fields in the entry.
    """
    def __init__(self, data: bytes, fields: BCSVField):
        self.data = data
        self.values = []
        for field in fields:
            value = (int.from_bytes(self.data[field.offset:field.offset + field.get_value_size()], byteorder='big') & field.bitmask) >> field.shift
            self.values.append(value)
    
    def get_value(self, field: BCSVField):
        """Returns the value of the specified field in the entry.
        """
        return field.get_value(self.data)

    def change_value(self, field: BCSVField, field_index: int, new_value: int):
        """Changes the value of the specified field in the entry to the new value.
        """
        self.values[field_index] = new_value
        value = (new_value << field.shift) & field.bitmask
        byte_value = int.to_bytes(value, field.get_value_size(), byteorder='big')
        self.data = self.data[:field.offset] + byte_value + self.data[field.offset + field.get_value_size():]
        return

    def get_field_by_name(self, name: str, fields: BCSVField):
        """Returns the field object with the specified name from the list of fields.
        """
        for field in fields:
            if field.name == name:
                return field
        raise ValueError(f"Field with name '{name}' not found")

    def __str__(self):
        return str(self.values)

class BCSVEditor:
    """A class for editing BCSV files, allowing for reading, modifying, and writing BCSV files.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fields = []
        self.entries = []
        self.offset = 0

        self.strings = []
        self.string_offsets = []

        self.entry_count = 0
        self.field_count = 0
        self.entry_offset = 0
        self.entry_size = 0

        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except:
            raise FileNotFoundError(f"File not found: {file_path}")

        # Parse the header from the data
        self.set_header(data[0:16])

        # Parse the fields from the data
        for i in range(self.field_count):
            field_data = data[16 + i * 12 : 16 + (i + 1) * 12]
            self.add_field(field_data)

        # Parse the entries from the data        
        for i in range(self.entry_count):
            entry_data = data[self.entry_offset + i * self.entry_size : self.entry_offset + (i + 1) * self.entry_size]
            self.add_entry(entry_data)
        
        # Parse the strings from the data
        strings = data[self.entry_offset + self.entry_count * self.entry_size :]
        self.strings = [string.decode('utf-8') for string in strings.split(b'\x00')[:-1]]
        self.get_new_string_offsets()

    def set_header(self, header: bytes):
        """Sets the header information for the BCSV file based on the provided header data.
        """
        self.entry_count = int.from_bytes(header[0:4], byteorder='big')
        self.field_count = int.from_bytes(header[4:8], byteorder='big')
        self.entry_offset = int.from_bytes(header[8:12], byteorder='big')
        self.entry_size = int.from_bytes(header[12:16], byteorder='big')
        return
    
    def add_field(self, data: bytes, index: int = None):
        """Adds a field to the BCSV file based on the provided field data and optional index.
        If index is not provided, the field will be added at the end of the fields list.
        """
        field = BCSVField(data)
        if index is not None:
            self.fields.insert(index, field)
        else:
            self.fields.append(field)
        return

    def add_entry(self, data: bytes, index: int = None):
        """Adds an entry to the BCSV file based on the provided entry data and optional index.
        If index is not provided, the entry will be added at the end of the entries list.
        """
        entry = BCSVEntry(data, self.fields)
        if index is not None:
            self.entries.insert(index, entry)
        else:
            self.entries.append(entry)
        return

    def get_new_string_offsets(self):
        """Updates the string offsets based on the current list of strings.
        """
        self.string_offsets = [0]
        for string in self.strings:
            self.string_offsets.append(self.string_offsets[-1] + len(string) + 1)
        return

    def update_entry_string_offsets(self):
        """Updates the string offsets in the entry data for all entries based on the current list of strings and string offsets.
        """
        for entry in self.entries:
            for field in self.fields:
                if field.type == 6: # STRING_OFFSET
                    value = entry.get_value(field)
                    if value in self.string_offsets:
                        string_index = self.string_offsets.index(value)
                        new_offset = self.string_offsets[string_index]
                        entry.change_value(field, self.fields.index(field), new_offset)
        return

    def replace_entry_name_by_index(self, index: int, new_name: str):
        """Replaces the name of an entry at the specified index with a new name.
        """
        if 0 <= index < len(self.entries):
            entry = self.entries[index]
            field = entry.get_field_by_name('name', self.fields)
            old_name_offset = field.get_value(entry.data)
            
            if new_name not in self.strings:
                self.strings.append(new_name)
                self.string_offsets.append(self.string_offsets[-1] + len(new_name) + 1)
            string_index = self.strings.index(new_name)
            entry.change_value(field, self.fields.index(field), self.string_offsets[string_index])
            """
            if old_name_offset not in [field.get_value(entry.data) for field in self.fields]: # If the old name is not used by any other field, remove it from the strings list 
                old_string_index = self.string_offsets.index(old_name_offset)
                del self.strings[old_string_index]
                old_offsets = self.string_offsets.copy()
                self.get_new_string_offsets()
                new_offsets = self.string_offsets
                self.update_entry_string_offsets(old_offsets, new_offsets)
            """
        else:
            raise IndexError("Index out of bounds")

    def update_entry_string_offsets(self, old_offsets: list, new_offsets: list):
        """Updates the string offsets in the entry data for all entries based on the old and new string offsets.
        """
        for entry in self.entries:
            for i, field in enumerate(self.fields):
                if field.type == 6: # STRING_OFFSET
                    value = entry.get_value(field)
                    if value in old_offsets:
                        old_index = old_offsets.index(value)
                        if old_index < len(new_offsets):
                            entry.change_value(field, i, new_offsets[old_index])
        return

    def get_string(self, entry: BCSVEntry, field: BCSVField):
        """Returns the string value of the specified field in the entry.
        """
        offset = entry.get_value(field)
        if offset in self.string_offsets:
            string_index = self.string_offsets.index(offset)
            return self.strings[string_index]
        else:
            return None

    def write_to_file(self, file_path: str):
        """Writes the BCSV file to the specified file path.
        """
        with open(file_path, 'wb') as f:
            # Write header
            f.write(int.to_bytes(self.entry_count, 4, byteorder='big'))
            f.write(int.to_bytes(self.field_count, 4, byteorder='big'))
            f.write(int.to_bytes(self.entry_offset, 4, byteorder='big'))
            f.write(int.to_bytes(self.entry_size, 4, byteorder='big'))

            # Write fields
            for field in self.fields:
                f.write(int.to_bytes(field.hash, 4, byteorder='big'))
                f.write(int.to_bytes(field.bitmask, 4, byteorder='big'))
                f.write(int.to_bytes(field.offset, 2, byteorder='big'))
                f.write(int.to_bytes(field.shift, 1, byteorder='big'))
                f.write(int.to_bytes(field.type, 1, byteorder='big'))

            # Write entries
            for entry in self.entries:
                f.write(entry.data)

            # Write strings
            for string in self.strings:
                f.write(string.encode('utf-8') + b'\x00')
            
            padding = 32 - f.tell() % 32
            f.write(b'@' * padding)
        return

    def __str__(self):
        values = [[field.name for field in self.fields]]
        for entry in self.entries:
            values.append([])
            for field in self.fields:
                if field.type == 6: # STRING_OFFSET
                    index = self.string_offsets.index(entry.get_value(field))
                    values[-1].append(self.strings[index])
                else:
                    values[-1].append(entry.get_value(field))
        
        max_lengths = [max(len(str(value)) for value in column) for column in zip(*values)]
        out = ''
        for row in values:
            out += '-+-'.join('-' * max_lengths[i] for i in range(len(row))) + '\n'
            out += ' | '.join(str(value).ljust(max_lengths[i]) for i, value in enumerate(row)) + '\n'
        return out

if __name__ == "__main__":
    bcsv = BCSVEditor('layera/objinfo')
    
    bcsv.replace_entry_name_by_index(3, 'MiniSkullSharkGalaxy')

    bcsv.write_to_file('test')