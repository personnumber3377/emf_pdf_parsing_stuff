
import re
import os

# This code is based on an earlier implementation of a thing.

def gen_python_code(struct_format, fields, name, has_variable):
    fh = open("template.py", "r")
    data = fh.read()
    fh.close()
    # 
    assert fields != "[]" or has_variable
    #assert fields != [] or has_variable
    # STRUCT_FORMAT is struct_format and FIELDS is fields in the template.
    data = data.replace("STRUCT_FORMAT", struct_format)
    data = data.replace("FIELDS", fields)
    data = data.replace("NAME", name)
    data = data.replace("HAS_VARIABLE", has_variable)
    return data

def save_code(code_string):
    fh = open("output.py", "a")
    fh.write(code_string)
    fh.write("\n\n\n") # Add a bit of this.
    fh.close()

def spec_to_python(contents):
    # field_regex = re.compile(r"(\w+)\s+(\w+);")
    record_regex = re.compile(r"^\d+\.\d+\.\d+\.\d+ \S+ Record$")
    bytes_field_regex = re.compile(r'\w+\s\(\d+\sbytes\):') # This is for fixed length fields...
    variable_field_regex = re.compile(r'\w+\s\(variable\):') # This is for fixed length fields...

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
        if line == "3 Structure Examples":
            code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
            save_code(code)
            output += code + "\n\n" # Add a couple of newlines just to be safe
            break
        
        name = None
        # Process the header line by line
        #for line in header.splitlines():

        # match = field_regex.search(line)
        if not in_rec: # Not in record yet. Check if we have encountered a record section:
            if record_regex.search(line): # There exists a match
                print("This line has the thing:"+str(line))
                in_rec = True
                name_of_rec = tok[-2] # Second last.
                print("Name of rec: "+str(name_of_rec))

        else: # In record..., therefore check if the thing has a field in it.
            if record_regex.search(line): # There exists a match
                # We have encountered a new record type. Save the old one as a parser and be done with it.
                print("oof")
                # Save the shit here..
                print("Name of reeeeeeeeeeec: "+str(name_of_rec))
                # assert False
                code = gen_python_code(str(struct_format), str(fields), name_of_rec, str(has_variable))
                output += code + "\n\n" # Add a couple of newlines just to be safe
                print("output shit: "+str(output))
                save_code(code)
                name_of_rec = tok[-2] # Second last.
                struct_format = [] # ""
                fields = []
                has_variable = False
                print("Name of rec: "+str(name_of_rec))

            elif len(line) >= len("2.3.4.2") and line[1] == "." and line[3] == "." and line[5] == ".": # This is to fix the bug in the parser when it encounters "2.3.4.2 EMR_HEADER Record Types"
                in_rec = False
            else:
                # Checks for the type line.
                if bytes_field_regex.search(line):
                    # A fixed length field.
                    
                    length = int(tok[1][1:])
                    print("Length: "+str(length))
                    struct_format.append(str(length)+"b") # b for bytes.
                    print("Here is a field: "+str(tok[0]))
                    fields.append(tok[0])
                elif variable_field_regex.search(line):
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


def gen_parsers(filename: str) -> None:
    fh = open(filename, "r")
    data = fh.read()
    fh.close()
    print(spec_to_python(data))
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
