import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer


class EMR_ALPHABLEND:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_ALPHABLEND"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BLENDFUNCTION', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ALPHABLEND {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_BITBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_BITBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_BITBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_MASKBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '2b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_MASKBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'ROP4', 'Reserved', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_MASKBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_PLGBLT:
    format = ['4b', '4b', '16b', '24b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_PLGBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'aptlDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_PLGBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_SETDIBITSTODEVICE:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_SETDIBITSTODEVICE"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'iStartScan', 'cScans'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETDIBITSTODEVICE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_STRETCHBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_STRETCHBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STRETCHBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





class EMR_STRETCHDIBITS:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_STRETCHDIBITS"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'BitBltRasterOperation', 'cxDest', 'cyDest'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...


    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STRETCHDIBITS {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size == len(out)
        return out # Return the output bytes





