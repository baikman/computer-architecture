MRI_TABLE = {
    "AND" : 0,
    "ADD" : 1,
    "LDA" : 2,
    "STA" : 3,
    "BUN" : 4,
    "BSA" : 5,
    "ISZ" : 6
}

NON_MRI_TABLE = {
    "CLA": 0x7800,
    "CLE": 0x7400,
    "CMA": 0x7200,
    "CME": 0x7100,
    "CIR": 0x7080,
    "CIL": 0x7040,
    "INC": 0x7020,
    "SPA": 0x7010,
    "SNA": 0x7008,
    "SZA": 0x7004,
    "SZE": 0x7002,
    "HLT": 0x7001,
    "INP": 0xF800,
    "OUT": 0xF400,
    "SKI": 0xF200,
    "SKO": 0xF100,
    "ION": 0xF080,
    "IOF": 0xF040
}

def parseLine(line) :
    if '/' in line:
        line = line[:line.index('/')]

    label = ""
    instruction = ""
    operand = ""
    indirect = False

    if len(line) > 4 and line[3] == ',':
        label = line[0:3].strip()
        line = line[4:]
    
    rLine = line.split()

    if rLine:
        instruction = rLine[0]
    if len(rLine) > 1:
        operand = rLine[1]

    if len(rLine) > 1 and 'I' in rLine[-1]:
        indirect = True

    return {"label" : label, "instruction" : instruction, "operand" : operand, "indirect" : indirect}

def firstPass(source) :
    symbol_table = {}
    location_counter = 0
    for line in source:
        parsed = parseLine(line)
        label = parsed["label"]
        instruction = parsed["instruction"]
        operand = parsed["operand"]

        if label:
            symbol_table[label] = location_counter

        if instruction == "ORG":
            location_counter = int(operand, 16)
        elif instruction == "END":
            return symbol_table
        else :
            location_counter += 1
    
    return symbol_table


def secondPass(source, symbol_table) :
    output = []
    location_counter = 0
    for line in source:
        parsed = parseLine(line)
        instruction = parsed["instruction"]
        operand = parsed["operand"]
        
        if instruction == "ORG":
            location_counter = int(operand, 16)
        elif instruction == "END":
            return output
        elif instruction == "HEX":
            code = int(operand, 16)
            output.append((location_counter, code))
            location_counter += 1
        elif instruction == "DEC":
            code = int(operand) & 0xFFFF
            output.append((location_counter, code))
            location_counter += 1
        elif instruction in MRI_TABLE:
            opcode = MRI_TABLE[instruction] << 12
            address = symbol_table[operand]
            indirect = 0x8000 if parsed["indirect"] else 0
            code = opcode | address | indirect
            output.append((location_counter, code))
            location_counter += 1
        elif instruction in NON_MRI_TABLE:
            code = NON_MRI_TABLE[instruction]
            output.append((location_counter, code))
            location_counter +=  1
    
    return output

def main():
    print("Brandon Aikman - Assembler")
    filename = input("Enter assembly file name: ")
    with open(filename, 'r') as file:
        lines = file.readlines()

    symbol_table = firstPass(lines)
    machine_code = secondPass(lines, symbol_table)

    # Write Symbol Table File
    with open("symbol_table.txt", "w") as file:
        for label, address in symbol_table.items():
            file.write(f"{label} {address:04X}\n")
    
    #Write Bin File
    with open("output.bin", "w") as file:
        for address, code in machine_code:
            file.write(f"{address:04X} {code:04X}\n")

if __name__ == "__main__":
    main()