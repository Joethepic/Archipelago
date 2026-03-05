import struct
from hashtable import hash_to_name, name_to_hash
import os

class BCSVEditor:
    def __init__(self, file_path: str):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except:
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.data = data

        # Initialize and set header values
        self.entry_count = 0
        self.field_count = 0
        self.entry_offset = 0
        self.entry_size = 0
        self._read_header_from_data()

        # Initialize and set fields
        self.fields = []
        self._read_fields_from_data()

        # Initialize and set entries
        self.entries = []
        self._read_entries_from_data()

        # Initalize and set strings
        self.strings = []
        self.string_offsets = []
        self._read_strings_from_data()
        self._read_string_offsets_from_data()

        self._replace_string_offsets_with_strings()
        return

    def _read_header_from_data(self):
        """Reads the header of the data and sets the entry count, field count, entry offset, and entry size.
        """
        header_data = self.data[:16]

        self.entry_count = int.from_bytes(header_data[0:4], byteorder='big')
        self.field_count = int.from_bytes(header_data[4:8], byteorder='big')
        self.entry_offset = int.from_bytes(header_data[8:12], byteorder='big')
        self.entry_size = int.from_bytes(header_data[12:16], byteorder='big')
        return

    def _read_field_from_data_by_index(self, index: int):
        """Reads the field data from the data for the specified index and adds it to the fields list.
        """
        # Each field is 12 bytes long and starts at offset 16 in the file
        field_data_offset = 16 + index*12
        field_data = self.data[field_data_offset:field_data_offset+12]

        # Convert the field data to a dictionary and return it
        field = {}
        field['name'] = hash_to_name[field_data[0:4]]
        field['bitmask'] = int.from_bytes(field_data[4:8], byteorder='big')
        field['offset'] = int.from_bytes(field_data[8:10], byteorder='big')
        field['shift'] = int.from_bytes(field_data[10:11], byteorder='big')
        field['type'] = int.from_bytes(field_data[11:12], byteorder='big')
        return field

    def _read_fields_from_data(self):
        """Reads the field data from the data and sets the fields list.
        """
        for i in range(self.field_count):
            field = self._read_field_from_data_by_index(i)
            self.fields.append(field)
        return

    def _read_entry_from_data_by_index(self, index: int):
        """Reads the entry data from the data for the specified index and returns it as a dictionary.
        """
        entry_data_offset = self.entry_offset + index*self.entry_size
        entry_data = self.data[entry_data_offset:entry_data_offset+self.entry_size]

        # Convert the entry data to a list of values based on the fields and return it
        entry = []
        for field in self.fields:
            data_format = self._get_data_format_from_field(field)
            data_length = self._get_data_length_from_field(field)
            offset = field['offset']
            
            data = entry_data[offset:offset+data_length]
            value = struct.unpack('>' + data_format, data)[0]
            entry.append(value)
        return entry
    
    def _read_entries_from_data(self):
        """Reads the entry data from the data and returns it as a list of dictionaries.
        """
        for i in range(self.entry_count):
            entry = self._read_entry_from_data_by_index(i)
            self.entries.append(entry)
        return
    
    def _read_strings_from_data(self):
        """Reads the string data from the data and sets the strings list.
        """
        # The string data starts at the end of the entry data and continues until the end of the file
        string_data_offset = self.entry_offset + self.entry_count*self.entry_size
        string_data = self.data[string_data_offset:]

        # Each string is null-terminated, so we can split the string data by null bytes to get the individual strings
        strings = string_data.split(b'\x00')
        self.strings = [string.decode('utf-8') for string in strings if b'@' not in string]
        return

    def _read_string_offsets_from_data(self):
        """Reads the string offsets from the data and sets the string_offsets list.
        """
        # The string data starts at the end of the entry data and continues until the end of the file
        string_data_offset = self.entry_offset + self.entry_count*self.entry_size
        string_data = self.data[string_data_offset:]

        # Each string is null-terminated, so we can split the string data by null bytes to get the individual strings and their offsets
        self.string_offsets = [0]
        for i, char in enumerate(string_data):
            char = bytes([char])
            if char == b'\x00' and i < len(string_data):
                if char != b'@':
                    self.string_offsets.append(i+1)
        return

    def _replace_string_offsets_with_strings(self):
        """Replaces the string offsets in the entries with the actual strings from the strings list.
        """
        for entry in self.entries:
            for i, field in enumerate(self.fields):
                if field['type'] == 6: # STRING_OFFSET
                    string_offset = entry[i]
                    string_index = self.string_offsets.index(string_offset)
                    string = self.strings[string_index]
                    entry[i] = string
        return

    def _replace_strings_with_string_offsets(self):
        for entry in self.entries:
            for i, field in enumerate(self.fields):
                if field['type'] == 6: # STRING_OFFSET
                    string = entry[i]
                    string_offset_index = self.strings.index(string)
                    string_offset = self.string_offsets[string_offset_index]
                    entry[i] = string_offset
        return

    def _get_column_from_index(self, index: int):
        """Returns a list of values for the specified column index from the entries.
        """
        column = []

        # Loop through each entry and get the value at the specified index and add it to the column list
        for entry in self.entries:
            column.append(entry[index])
        return column

    def _get_data_format_from_field(self, field: dict):
        """Returns the data format string for the specified field based on its type.
        """
        data_type = field['type']
        if data_type == 0: # LONG
            return 'i'
        elif data_type == 1: # STRING
            return 'c'*32
        elif data_type == 2: # FLOAT
            return 'f'
        elif data_type == 3: # LONG_2
            return 'i'
        elif data_type == 4: # SHORT
            return 'h'
        elif data_type == 5: # CHAR
            return 'b'
        elif data_type == 6: # STRING_OFFSET
            return 'I'
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def _get_data_length_from_field(self, field: dict):
        """Returns the data length in bytes for the specified field based on its type.
        """
        data_type = field['type']
        if data_type == 0: # LONG
            return 4
        elif data_type == 1: # STRING
            return 32
        elif data_type == 2: # FLOAT
            return 4
        elif data_type == 3: # LONG_2
            return 4
        elif data_type == 4: # SHORT
            return 2
        elif data_type == 5: # CHAR
            return 1
        elif data_type == 6: # STRING_OFFSET
            return 4
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def get_entry_name_by_index(self, index: int):
        entry = self.entries[index]
        return entry[0]

    def rename_entry_by_index(self, index: int, new_name: str):
        entry = self.entries[index]
        entry[0] = new_name
        if new_name not in self.strings:
            self.strings.append(new_name)
            self.string_offsets.append(self.string_offsets[-1] + len(new_name) + 1)
        return

    def write_to_file(self, file_path: str, overwrite = True):
        if os.path.isfile(file_path) and not overwrite:
            raise FileExistsError(f"File already exists: {file_path}")
        
        self._write_header_to_data()
        self._write_fields_to_data()
        self._write_entries_to_data()
        self._write_strings_to_data()
        self._write_string_offsets_to_data()

        # Pad file to 32 bytes
        if len(self.data) % 32 != 0:
            padding = 32 - len(self.data) % 32
            self.data += b'@' * padding

        try:
            with open(file_path, 'wb') as f:
                f.write(self.data)
        except:
            raise FileExistsError(f"File not found: {file_path}")

    def _write_header_to_data(self):
        """Writes the header values to the data.
        """
        header_data = b''
        header_data += self.entry_count.to_bytes(4, byteorder='big')
        header_data += self.field_count.to_bytes(4, byteorder='big')
        header_data += self.entry_offset.to_bytes(4, byteorder='big')
        header_data += self.entry_size.to_bytes(4, byteorder='big')
        self.data = header_data + self.data[16:]
        return

    def _write_field_to_data_by_index(self, index: int):
        """Writes the field data to the data for the specified index.
        """
        # Each field is 12 bytes long and starts at offset 16 in the file
        field_data_offset = 16 + index*12
        field = self.fields[index]
        field_data = b''

        # Convert the field dictionary to bytes
        field_data += name_to_hash[self.fields[index]['name']]
        field_data += field['bitmask'].to_bytes(4, byteorder='big')
        field_data += field['offset'].to_bytes(2, byteorder='big')
        field_data += field['shift'].to_bytes(1, byteorder='big')
        field_data += field['type'].to_bytes(1, byteorder='big')
        self.data = self.data[:field_data_offset] + field_data + self.data[field_data_offset+12:]
        return

    def _write_fields_to_data(self):
        """Writes the field data to the data.
        """
        for i in range(self.field_count):
            self._write_field_to_data_by_index(i)
        return

    def _write_entry_to_data_by_index(self, index: int):
        """Write the entry data from the data for the specified index and returns it as a dictionary.
        """
        # Each entry is entry_size bytes long and starts at entry_offset in the file
        entry_data_offset = self.entry_offset + index*self.entry_size
        entry_data = b'\x00' * self.entry_size

        entry = self.entries[index]

        # Convert the entry list of values to bytes based on the fields and write it to the data
        for field in self.fields:
            data_length = self._get_data_length_from_field(field)
            data_format = self._get_data_format_from_field(field)
            offset = field['offset']
            index = self.fields.index(field)
            
            if field['type'] == 6: # STRING_OFFSET
                string = entry[index]
                string_offset_index = self.strings.index(string)
                string_offset = self.string_offsets[string_offset_index]
                entry[index] = string_offset
                
            value_bytes = struct.pack('>' + data_format, entry[index])
            entry_data = entry_data[:offset] + value_bytes + entry_data[offset+data_length:]
        self.data = self.data[:entry_data_offset] + entry_data + self.data[entry_data_offset+self.entry_size:]
        return

    def _write_entries_to_data(self):
        """Writes the entry data to the data from the entries list.
        """
        for i in range(self.entry_count):
            self._write_entry_to_data_by_index(i)
        return
    
    def _write_strings_to_data(self):
        """Writes the strings list to the data.
        """
        # The string data starts at the end of the entry data and continues until the end of the file
        string_offset = self.entry_offset + self.entry_count*self.entry_size
        string_data = b''
        for string in self.strings:
            string_data += string.encode('utf-8') + b'\x00'

        self.data = self.data[:string_offset] + string_data

        self._read_string_offsets_from_data()
        return

    def _write_string_offsets_to_data(self):
        """Writes the string offsets to the data.
        """
        for i, entry in enumerate(self.entries):
            for j, field in enumerate(self.fields):
                if field['type'] == 6: # STRING_OFFSET
                    string_offset = entry[j]
                    if string_offset not in self.string_offsets:
                        raise ValueError(f"String offset not found in string offset list: {string_offset}")
                    
                    string_offset_data = string_offset.to_bytes(4, byteorder='big')

                    string_offset_data_offset = self.entry_offset + i*self.entry_size + field['offset']

                    # Replace the string offset in the data with the actual string offset value
                    self.data = self.data[:string_offset_data_offset] + string_offset_data + self.data[string_offset_data_offset+4:]
        return

    def __str__(self):
        """Create a nice table representation of the BCSV data and return it as a string.
        """
        out = ''
        # Get max lengths for spacing
        max_lengths = [max(len(field['name']), max(len(str(val)) for val in self._get_column_from_index(i))) for i, field in enumerate(self.fields)]
        
        # Add the field names to the output string with proper spacing
        out  += ' | '.join(field['name'].ljust(max_lengths[i]) for i, field in enumerate(self.fields)) + '\n'
        out  += '-+-'.join('-' * max_lengths[i] for i in range(len(self.fields))) + '\n'
        
        # Loop through each entry and add it to the output string with proper spacing
        for entry in self.entries:
            out += ' | '.join(str(val).ljust(max_lengths[i]) for i, val in enumerate(entry)) + '\n'
        return out


def main():
    bcsv = BCSVEditor('layera/objinfo')

    for i in range(len(bcsv.entries)):
        if 'MiniEgg' in bcsv.get_entry_name_by_index(i):
            bcsv.rename_entry_by_index(i, 'test')

    print(bcsv)

    bcsv.write_to_file('test')

if __name__ == "__main__":
    main()