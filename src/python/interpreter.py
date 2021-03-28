import sys

tableSize = 256
table = [0] * tableSize
functions = [0] * 64
pointer = 0
inQuotes = False
saved = 0
charNum = 0
loopChar = 0
statementSize = 0
code = "++." # in case something fails
statement = ">+.<-"
showRegisters = False

def main():
    global tableSize
    global table
    global pointer
    global inQuotes
    global saved
    global code
    global charNum
    global loopChar 
    global statementSize
    global showRegisters

    keys = {
        "+": "inc", # Increment
        "-": "dec", # Decrement
        "*": "lsh", # Left shift
        "/": "rsh", # Right shift
        ">": "gor", # Go right one cell
        "<": "gol", # Go left one cell
        ".": "out", # Print
        "{": "whl", # Start while
        "}": "jwl", # Jump to top while if last cell (loop cell) is not 0 or parameterized number
        "[": "dfn", # Define cell with value between []
        "?": "eif", # Execute if (would look like this: ?(12)//---;. for "if cell is 12, divide by 4 and subtract 3, then print")
        "@": "get", # Goto cell at next val (e.g. $@(0)?(32)@$-;. which means "save current cell, go to cell 0, if cell 0 = 32, go to cell save, decrement cell, then print")
        "$": "sav", # Save cell location for quick return. Note: Doing this again overwrites; i.e. only one cell can be saved.
        "&": "asc", # Print ascii value
        "=": "mov", # Move current value to cell given (i.e. $@(0)=($) which will save the current cell, go to cell 0, then move cell 0's value to the saved cell)
        "%": "mod", # Set cell to itself mod 2
        ":": "fnc", # function define (:(0)<+>;)
        "^": "run",
        "_": "nwl"
    }

    def getCommand(char):
        if char in keys:
            return keys[char]
        else:
            return False

    def inc():
        global pointer
        global table
        table[pointer] += 1

    def dec():
        global pointer
        global table
        table[pointer] -= 1

    def lsh():
        global pointer
        global table
        table[pointer] *= 2

    def rsh():
        global pointer
        global table
        table[pointer] //= 2

    def mod():
        global pointer
        global table
        table[pointer] = table[pointer] % 2    

    def out():
        global pointer
        global table
        print(table[pointer], end="")

    def nwl():
        global pointer
        global table
        print("\n", end="")

    def gol():
        global pointer
        if (pointer - 1) < 0:
            pointer = 0
            return
        pointer -= 1

    def gor():
        global pointer
        if (pointer + 1) >= tableSize:
            pointer = tableSize-1
            return
        pointer += 1

    def whl():
        global charNum
        global loopChar
        global pointer
        global table
        global code
        global saved
        global statementSize
        global statement
        loopChar = charNum
        statement = code[charNum+1 : code.find("}", charNum+1)]
        # print(statement)
        statementSize = code.find("}", charNum+1) - charNum

    def jwl():
        global charNum
        global loopChar
        global pointer
        global table
        global code
        global saved
        global statement
        condition = 0
        if charNum+1 < len(code) and code[charNum+1] == "(":
            if charNum+1 < len(code) and code[charNum+2] == "$":
                condition = table[saved]
                charNum += 2 # we now need to skip that save
            else:
                condition = int(code[charNum + 2:code.find(")", charNum+1)])
        elif charNum+1 < len(code) and code[charNum+1] == "$":
            condition = table[saved]

        stopCounter = 0
        while(table[pointer] != condition):
            if stopCounter > 8192:
                sys.exit("! fatal error: loop is infinite")
            # print("statement="+statement)
            charNum = loopChar
            i = charNum
            for char in statement:
                if i != charNum:
                    i+=1
                    continue
                comm = runCommand(getCommand(char))
                if comm:
                    comm()
                charNum += 1
                i += 1
            stopCounter += 1

        charNum = code.find("}", charNum+1)
        statement = ""

    def dfn():
        global pointer
        global charNum
        global table
        global code
        table[pointer] = int(code[charNum+1 : code.find("]", charNum+1)])

    def eif():
        global charNum
        global pointer
        global table
        global code
        global saved
        condition = 0
        if charNum+1 < len(code) and code[charNum+1] == "(":
            if charNum+1 < len(code) and code[charNum+2] == "$":
                condition = table[saved]
                charNum += 2 # we now need to skip that save
            else:
                condition = int(code[charNum + 2:code.find(")", charNum+1)])
        elif charNum+1 < len(code) and code[charNum+1] == "$":
            condition = table[saved]

        if table[pointer] != condition:
            charNum = code.find(";", charNum+1)
        

    def get():
        global charNum
        global pointer
        global table
        global code
        global saved
        if charNum+1 < len(code) and code[charNum+1] == "(":
            if charNum+1 < len(code) and code[charNum+2] == "$":
                pointer = saved
                charNum += 2 # we now need to skip that save
            else:
                pointer = int(code[charNum + 2:code.find(")", charNum+1)])
        elif charNum+1 < len(code) and code[charNum+1] == "$":
            pointer = saved

    def sav():
        global saved
        global pointer
        saved = pointer
    
    def asc():
        global pointer
        global table
        print(chr(table[pointer]), end="")

    def mov():
        global pointer
        global table
        global code
        global charNum
        global saved
        if charNum+1 < len(code) and code[charNum+1] == "(":
            if charNum+2 < len(code) and code[charNum+2] == "$":
                table[pointer] = table[saved]
                charNum += 2 # we now need to skip that save
            else:
                table[pointer] = table[int(code[charNum+2:code.find(")", charNum+1)])]
        elif charNum+1 < len(code) and code[charNum+1] == "$":
            table[pointer] = [saved]

    def fnc():
        global charNum
        global loopChar
        global pointer
        global table
        global code
        global saved
        global statementSize
        global statement
        if charNum+2 < len(code) and code[charNum+1] == "(":
            funccode = code[code.find(")", charNum+1)+1 : code.find(";", charNum+1)]
            # print(funccode)
            functions[int(code[charNum+2:code.find(")", charNum+1)])] = funccode
        charNum = code.find(";", charNum+1)

    def run():
        global charNum
        global loopChar
        global pointer
        global table
        global code
        global saved
        global statementSize
        global statement
        if charNum+2 < len(code) and code[charNum+1] == "(":
            funccode = functions[int(code[charNum+2:code.find(")", charNum+1)])]
        # print(funccode)
        temp = charNum
        i = charNum
        for char in funccode:
            if i != charNum:
                i+=1
                continue
            comm = runCommand(getCommand(char))
            if comm:
                comm()
            charNum += 1
            i += 1

        charNum = temp
        statement = ""

    coms = {
        "inc": inc, # Increment
        "dec": dec, # Decrement
        "lsh": lsh, # Left shift
        "rsh": rsh, # Right shift
        "gor": gor, # Go right one cell
        "gol": gol, # Go left one cell
        "out": out, # Print
        "whl": whl, # Start while
        "jwl": jwl, # Jump to top while if last cell (loop cell) is not 0
        "dfn": dfn, # Define cell with value between []
        "eif": eif, # Execute if (would look like this: ?(12)//---;. for "if cell is 12, divide by 4 and subtract 3, then print")
        "get": get, # Goto cell at next val (e.g. $@(0)?(32)@$-;. which means "save current cell, go to cell 0, if cell 0 = 32, go to cell save, decrement cell, then print")
        "sav": sav, # Save cell location for quick return. Note: Doing this again overwrites; i.e. only one cell can be saved.
        "asc": asc, # print ascii val of cell
        "mov": mov, # Move current value to cell given (i.e. $@(0)=($) which will save the current cell, go to cell 0, then move cell 0's value to the saved cell)
        "mod": mod,
        "fnc": fnc,
        "run": run,
        "nwl": nwl
    }

    def runCommand(command):
        if command:
            return coms[command]
        else:
            return False

    def parseFlags(args):
        global showRegisters
        for i in range(0, len(args)):
            if args[i] == "-m" or args[i] == "--malloc":
                if i + 1 < len(args):
                    tableSize = args[i + 1] if int(args[i + 1]) else 256
                    print(tableSize)
                    table = [0] * tableSize
            if args[i] == "-sr" or args[i] == "--show-registers":
                showRegisters = True
        return args

    args = sys.argv
    args = args[1:]
    
    inFile = None
    try:
        if len(args) > 0:
            inFile = open(args[0], 'r')
            code = inFile.read()
        else:
            code = input(" ~ ")
    except FileNotFoundError:
        code = input(" ~ ")
    
        

    
    if len(args) > 0:
        parseFlags(args)

    if code[0] == "[":
            # malloc
            tableSize = int(code[1:code.index("]")])
            print("! allocated "+str(tableSize)+ " cells")
            table = [0] * tableSize
            code = code[code.index("]"):]
    i = 0
    for char in code:
        if i != charNum:
            i+=1
            continue
        comm = runCommand(getCommand(char))
        if comm:
            comm()
        charNum += 1
        i += 1
    if showRegisters:
        print(table)
    input("Press enter to close...")

if __name__ == '__main__':
    main()
    