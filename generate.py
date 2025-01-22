
import re
import os

# This code is based on an earlier implementation of a thing.

has_start = False

def fixup_stuff(struct_format, fields): # This looks at the struct format and fields and sees if there is the Type or Size field and then puts them at the start.
    struct_format = eval(struct_format) # Obvious possible command injection, but idc
    fields = eval(fields) # Same here too.

    assert isinstance(struct_format, list)
    assert isinstance(fields, list)

    assert len(struct_format) == len(fields)
    if "Type" in fields:
        # Remove the Type and the corresponding struct thing
        ind = fields.index("Type")
        # Remove.
        fields.pop(ind)
        struct_format.pop(ind)
    # Do the same for "Size"
    if "Size" in fields:
        # Remove the Type and the corresponding struct thing
        ind = fields.index("Size")
        # Remove.
        fields.pop(ind)
        struct_format.pop(ind)
    


    assert len(struct_format) == len(fields)
    assert "Size" not in fields and "Type" not in fields
    # Now add them to the start, since each record is guaranteed to have these fields at the start.
    fields = ["Type", "Size"] + fields # Add the two stuff.
    struct_format = ["4b", "4b"] + struct_format # Add the two integer fields


    return str(struct_format), str(fields)

def gen_python_code(struct_format, fields, name, has_variable):
    if not name:
        return ""
    # Hardcoded check for the EMR_ string. If it doesn't exist in the name, then something bad happened.
    if "EMR_" not in name:
        print("Invalid class name: "+str(name))
        assert False

    fh = open("template.py", "r")
    data = fh.read()
    fh.close()
    # 
    assert fields != "[]" or has_variable
    #assert fields != [] or has_variable
    # STRUCT_FORMAT is struct_format and FIELDS is fields in the template.

    struct_format, fields = fixup_stuff(struct_format, fields)
    data = data.replace("STRUCT_FORMAT", struct_format)
    data = data.replace("FIELDS", fields)
    data = data.replace("NAME", name)
    data = data.replace("HAS_VARIABLE", has_variable)
    if name == "EMR_COMMENT":
        # print("poopfuck")
        fh = open("poopfuck.txt", "w")
        fh.write(data)
        fh.close()
        assert has_variable
    
    return data

def save_code(code_string):
    fh = open("output.py", "a")
    fh.write(code_string)
    fh.write("\n\n\n") # Add a bit of this.
    fh.close()

def spec_to_python(contents):
    global has_start
    if not has_start:
        fh = open("output.py", "a")
        fh.write('''import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer
''')
        fh.write("\n\n")
        fh.close()
        has_start = True
    # field_regex = re.compile(r"(\w+)\s+(\w+);")
    record_regex = re.compile(r"^\d+\.\d+\.\d+\.\d+ \S+ Record$")
    bytes_field_regex = re.compile(r'\w+\s\(\d+\sbytes\):') # This is for fixed length fields...
    variable_field_regex = re.compile(r'\w+\s\(variable') # This is for fixed length fields...

    lines = contents.splitlines()
    line_ind = 0
    in_rec = False

    has_variable = False # This signifies if the record type has variable field at the end of it...
    name_of_rec = None
    struct_format = [] # ""
    fields = []

    # This part doesn't work for "2.3.4.2 EMR_HEADER Record Types" because reasons...

    output = "" # Final output code...


    while True:


        if line_ind == len(lines):
            code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
            save_code(code)
            output += code + "\n\n" # Add a couple of newlines just to be safe
            break

        line = lines[line_ind]
        tok = line.split(" ")
        
        
        name = None

        if line == "3 Structure Examples":
            code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
            save_code(code)
            output += code + "\n\n" # Add a couple of newlines just to be safe
            break

        
        
        # Process the header line by line
        #for line in header.splitlines():

        # match = field_regex.search(line)
        if not in_rec: # Not in record yet. Check if we have encountered a record section:
            if record_regex.search(line): # There exists a match
                # print("This line has the thing:"+str(line))
                in_rec = True
                name_of_rec = tok[-2] # Second last.
                # print("Name of rec: "+str(name_of_rec))

        else: # In record..., therefore check if the thing has a field in it.
            if record_regex.search(line): # There exists a match
                # We have encountered a new record type. Save the old one as a parser and be done with it.
                # print("oof")
                # Save the shit here..
                # print("Name of reeeeeeeeeeec: "+str(name_of_rec))
                # assert False
                code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
                output += code + "\n\n" # Add a couple of newlines just to be safe
                # print("output shit: "+str(output))
                save_code(code)
                name_of_rec = tok[-2] # Second last.
                struct_format = [] # ""
                fields = []
                has_variable = False
                # print("Name of rec: "+str(name_of_rec))

            elif len(line) >= len("2.3.4.2") and line[1] == "." and line[3] == "." and line[5] == "." and "Record Types" in line: # This is to fix the bug in the parser when it encounters "2.3.4.2 EMR_HEADER Record Types"
                #print("Not in record.")
                #print("Previous record name: "+str(name_of_rec))
                in_rec = False


                # Maybe this bullshit here?????
                code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
                output += code + "\n\n" # Add a couple of newlines just to be safe
                # print("output shit: "+str(output))
                save_code(code)
                name_of_rec = tok[-2] # Second last.
                struct_format = [] # ""
                fields = []
                has_variable = False


            else:
                
                # Checks for the type line.
                # Now check for the thing. This is to fix the situation when there is a description about some other structure before the next record type recorded. Therefore this prevents invalid output...
                if "Type (4 bytes)" in line and struct_format != []:
                    code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
                    output += code + "\n\n" # Add a couple of newlines just to be safe
                    # print("output shit: "+str(output))
                    save_code(code)
                    # name_of_rec = tok[-2] # Second last.
                    name_of_rec = None
                    struct_format = [] # ""
                    fields = []
                    has_variable = False
                    in_rec = False
                    continue

                if bytes_field_regex.search(line):
                    # A fixed length field.
                    
                    length = int(tok[1][1:])
                    # print("Length: "+str(length))
                    struct_format.append(str(length)+"b") # b for bytes.
                    #print("Here is a field: "+str(tok[0]))
                    #print("Line index: "+str(line_ind))
                    fields.append(tok[0])
                elif variable_field_regex.search(line):
                    #print("Line: "+str(line)+" WAS a variable thing")
                    has_variable = True # Add variable stuff.

        '''
        if match:
            c_type, field_name = match.groups()
            if c_type in type_mapping:
                # struct_format += type_mapping[c_type]
                struct_format.append(type_mapping[c_type])
                fields.append(field_name)
            else:
                raise ValueError(f"Unknown type: {c_type}")

        # Generate python code.

        python_code = gen_python_code(str(struct_format), str(fields))
        return python_code
        '''


        # Increment line counter...
        line_ind += 1
    return output


def save_manual_input(): # This function is here because some records aren't documented in the PDF in the format this autogenerator expects. This causes the parser to miss some record types. These types are manually programmed in manual.py
    fh = open("manual.py")
    data = fh.read()
    fh.close()
    save_code(data)
    return


def gen_parsers(filename: str) -> None:
    fh = open(filename, "r")
    data = fh.read()
    fh.close()
    spec_to_python(data)
    # Save the manual shit....
    save_manual_input()
    return


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: "+str(sys.argv[0])+" INPUT_CONTENTS_FILE")
        exit(0)
    # Delete the old stuff.
    os.system("rm output.py")
    gen_parsers(sys.argv[1])
    return 0


import sys

if __name__=="__main__":
    ret = main()

    exit(ret)
