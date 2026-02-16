from hashtable import convert_hash_or_name
import struct

class BCSVField:
    def __init__(self, data: bytes):
        # Ensure the data is exactly 12 bytes long
        if len(data) != 12:
            raise ValueError("Data must be exactly 12 bytes long.")

        self.HASH = int.from_bytes(data[0:4], byteorder='big')
        self.BITMASK = int.from_bytes(data[4:8], byteorder='big')
        self.OFFSET = int.from_bytes(data[8:10], byteorder='big')
        self.SHIFT = int.from_bytes(data[10:11], byteorder='big')
        self.TYPE = int.from_bytes(data[11:12], byteorder='big')

        self.name = convert_hash_or_name(self.HASH)
    
    def get_field(self):
        """Returns the field as a 12-byte bytes object.
        """
        out = b''
        out += self.HASH.to_bytes(4, byteorder='big')
        out += self.BITMASK.to_bytes(4, byteorder='big')
        out += self.OFFSET.to_bytes(2, byteorder='big')
        out += self.SHIFT.to_bytes(1, byteorder='big')
        out += self.TYPE.to_bytes(1, byteorder='big')
        return out

    def get_type(self):
        """Returns the type of the field as a string.
        """
        if self.TYPE == 0:
            return 'LONG'
        elif self.TYPE == 1:
            return 'STRING'
        elif self.TYPE == 2:
            return 'FLOAT'
        elif self.TYPE == 3:
            return 'LONG_2'
        elif self.TYPE == 4:
            return 'SHORT'
        elif self.TYPE == 5:
            return 'CHAR'
        elif self.TYPE == 6:
            return 'STRING_OFFSET'
        raise ValueError(f"Unknown type: {self.TYPE}")

    def get_type_size(self):
        """Returns the size of the field type in bytes.
        """
        if self.TYPE == 0: # LONG
            return 4
        elif self.TYPE == 1: # STRING
            return 32
        elif self.TYPE == 2: # FLOAT
            return 4
        elif self.TYPE == 3: # LONG_2
            return 4
        elif self.TYPE == 4: # SHORT
            return 2
        elif self.TYPE == 5: # CHAR
            return 1
        elif self.TYPE == 6: # STRING_OFFSET
            return 4
        raise ValueError(f"Unknown type: {self.TYPE}")

    def get_type_format(self):
        """Returns the struct format character for the field type.
        """
        if self.TYPE == 0: # LONG
            return 'i'
        elif self.TYPE == 1: # STRING
            return 'c'*32
        elif self.TYPE == 2: # FLOAT
            return 'f'
        elif self.TYPE == 3: # LONG_2
            return 'i'
        elif self.TYPE == 4: # SHORT
            return 'h'
        elif self.TYPE == 5: # CHAR
            return 'b'
        elif self.TYPE == 6: # STRING_OFFSET
            return 'I'
        raise ValueError(f"Unknown type: {self.TYPE}")

    def get_value(self, entry_data: bytes):
        """Returns the value of the field from the given entry data.
        """
        field_data = entry_data[self.OFFSET: self.OFFSET + self.get_type_size()]
        value = (int.from_bytes(field_data, byteorder='big') & self.BITMASK) >> self.SHIFT
        return int.to_bytes(value, self.get_type_size(), byteorder='big')

    def __str__(self):
        return f"Field Name: {self.name}\nHash: {self.HASH}\nBitmask: {int.to_bytes(self.BITMASK, 4, byteorder='big')}\nOffset: {self.OFFSET}\nShift: {self.SHIFT}\nType: {self.get_type()}"

class BCSVEntry:
    def __init__(self, data: bytes, fields: list, strings: list, string_offsets: list):
        self.VALUES = []
        self.fields = fields

        self.strings = strings
        self.string_offsets = string_offsets

        # Extract values for each field from the entry data
        self.VALUES = [field.get_value(data) for field in self.fields]

    def get_value_by_field(self, field):
        """Returns the value of the specified field.
        """
        index = self.fields.index(field)
        return self.VALUES[index]

    def get_entry(self):
        """Returns the entry as a bytes object.
        """
        out = b''
        for field in self.fields:
            out += self.get_value_by_field(field)
        return out

    def get_output_string(self, field):
        """Returns the value of the field as a string.
        """
        index = self.fields.index(field)
        type_format = '>' + field.get_type_format()
        print(field.get_type_format())
        print(self.VALUES[index])
        value = struct.unpack(type_format, self.VALUES[index])[0]
        print(value)
        if field.TYPE == 1: # STRING
            return value.decode('utf-8').rstrip('\x00')
        return str(value)

    def __str__(self):
        field_names = []
        value_strings = []
        max_lengths = []
        for i, field in enumerate(self.fields):
            field_names.append(field.name)
            value_strings.append(self.get_output_string(field))
            max_lengths.append(max(len(field.name), len(value_strings[-1])))
        
        out = ""
        out = ' | '.join(f"{field_names[i]:<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'
        out += '-|-'.join('-' * max_lengths[i] for i in range(len(self.fields))) + '\n'
        out += ' | '.join(f"{value_strings[i]:<{max_lengths[i]}}" for i in range(len(self.fields))) + '\n'
        return out

class BCSVTable:
    def __init__(self, file_path: str = ''):
        if not file_path:
            raise ValueError("File path cannot be empty.")
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except:
            raise IOError(f"Could not read file: {file_path}")
        
        self.FIELDS = []
        self.ENTRIES = []
        

        
        # Read header information
        self.ENTRY_COUNT = int.from_bytes(data[0:4], byteorder='big')
        self.FIELD_COUNT = int.from_bytes(data[4:8], byteorder='big')
        self.ENTRY_OFFSET = int.from_bytes(data[8:12], byteorder='big')
        self.ENTRY_SIZE = int.from_bytes(data[12:16], byteorder='big')

        # Extract strings from the data
        strings = data[self.ENTRY_OFFSET + self.ENTRY_COUNT * self.ENTRY_SIZE:]
        self.strings = strings.split(b'\x00')[:-1]
        self.string_offsets = []

        # Calculate string offsets
        offset = 0
        for string in self.strings:
            self.string_offsets.append(offset)
            offset += len(string) + 1

        data = data[16:] # Remove the header from the data
        data = data[:self.ENTRY_OFFSET + self.ENTRY_COUNT * self.ENTRY_SIZE] # Remove the strings from the data
 
        # Read fields and entries
        for i in range(self.FIELD_COUNT):
            field_data = data[:12] # Get the first 12 bytes for the field data
            field = BCSVField(field_data)
            self.FIELDS.append(field)
            data = data[12:] # Remove the field data from the data
            
        for i in range(self.ENTRY_COUNT):
            entry_data = data[:self.ENTRY_SIZE] # Get the bytes for the entry data
            entry = BCSVEntry(entry_data, self.FIELDS, self.strings, self.string_offsets)
            self.ENTRIES.append(entry)
            data = data[self.ENTRY_SIZE:] # Remove the entry data from the data
        print(len(data))
            
        # Validate entry and field counts
        if self.ENTRY_COUNT != len(self.ENTRIES):
            raise ValueError("Entry count does not match the number of entries read.")
        if self.FIELD_COUNT != len(self.FIELDS):
            raise ValueError("Field count does not match the number of fields read.")

    def get_field_by_index(self, index: int):
        """Returns the field at the specified index.
        """
        return self.FIELDS[index]

    def get_entry_by_index(self, index: int):
        """Returns the entry at the specified index.
        """
        return self.ENTRIES[index]
    
    def add_entry(self, entry_data: bytes):
        """Adds a new entry to the table with the given entry data.
        """
        if len(entry_data) != self.ENTRY_SIZE:
            raise ValueError(f"Entry data must be exactly {self.ENTRY_SIZE} bytes long.")
        
        # Create a new entry and add it to the entries list
        entry = BCSVEntry(entry_data, self.FIELDS, self.strings, self.string_offsets)
        self.ENTRIES.append(entry)
        self.ENTRY_COUNT += 1
        return entry
    
    def remove_entry(self, index: int):
        """Removes an entry from the table at the specified index.
        """
        if index < 0 or index >= self.ENTRY_COUNT:
            raise IndexError("Index out of bounds.")
        self.ENTRIES.pop(index)
        self.ENTRY_COUNT -= 1

    def update_strings(self, new_strings: list):
        """Updates the strings in the table with the given list of new strings.
        """
        self.strings = new_strings
        self.string_offsets = []
        offset = 0
        for string in self.strings:
            self.string_offsets.append(offset)
            offset += len(string) + 1
        return self.strings, self.string_offsets

    def write_to_file(self, file_path: str):
        """Writes the table data to a file.
        """
        out = b''
        out += self.ENTRY_COUNT.to_bytes(4, byteorder='big')
        out += self.FIELD_COUNT.to_bytes(4, byteorder='big')
        out += self.ENTRY_OFFSET.to_bytes(4, byteorder='big')
        out += self.ENTRY_SIZE.to_bytes(4, byteorder='big')

        for field in self.FIELDS:
            out += field.get_field()
        
        count = 1
        for entry in self.ENTRIES:
            out += int.to_bytes(count*5, 1, byteorder='big')
            count += 1
            out += entry.get_entry()
        
        for string in self.strings:
            out += string + b'\x00'
        
        padding = 32 - len(out) % 32
        out += b'@' * padding
        
        try:
            with open(file_path, 'wb') as f:
                f.write(out)
        except:
            raise IOError(f"Could not write to file: {file_path}")
        return self

    def __str__(self):
        """Returns a string representation of the table with field names and entry values formatted in a table-like structure.
        """
        value_strings = [[]]
        for field in self.FIELDS:
            value_strings[-1].append(field.name)
        for entry in self.ENTRIES:
            value_strings.append([])
            for field in self.FIELDS:
                value_strings[-1].append(entry.get_output_string(field))
                
        # Calculate the maximum length for each field value and name for formatting
        max_lengths = [max(len(value_strings[j][i]) for j in range(len(value_strings))) for i in range(len(value_strings[0]))]

        # Create the header row with field names, the separator row, and the value rows for each entry
        out = ' | '.join(f"{value_strings[0][i]:<{max_lengths[i]}}" for i in range(len(self.FIELDS))) + '\n'

        for i in range(1, len(value_strings)):
            out += '-|-'.join('-' * max_lengths[j] for j in range(len(self.FIELDS))) + '\n'
            out += ' | '.join(f"{value_strings[i][j]:<{max_lengths[j]}}" for j in range(len(self.FIELDS))) + '\n'
        return out

if __name__ == "__main__":
    bcsv = BCSVTable(r'layerc/objinfo')

    bcsv.write_to_file(r'test')

    print(bcsv.get_entry_by_index(2))

    newbcsv = BCSVTable(r'test')

    print(newbcsv.get_entry_by_index(2))