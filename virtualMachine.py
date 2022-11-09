class VirtualMachine(object):

    def __init__(self, functionDirectoryTable, constantsTable,
                 temporalTable, parametersTable, quadruplesTable,):
        self.pointer = 0
        self.currentScope = ""
        self.nextScope = ""
        self.scopeReturnType = ""
        self.directory = functionDirectoryTable
        self.consts = constantsTable
        self.temps = temporalTable
        self.quads = quadruplesTable
        self.params = parametersTable

        self.pointer = 0
        self.isJumping = False

        # Local pointers
        self.intLpointer = 0
        self.floatLpointer = 0
        self.charLpointer = 0
        self.stringLpointer = 0
        self.dataframeLpointer = 0

        # Local memory
        # int, float, char, string, dataframe
        self.localMem = [[None] * 2500, [None] * 2500, [None] * 2500, [None] * 2500, [None] * 2500]

    def runProgram(self):
        eof = len(self.quads)

        while self.pointer < eof:
            self.isJumping = False
            curQuad = self.quads[self.pointer]
            print(curQuad)

            if curQuad[0] == 'GOTO':
                self.pointer = curQuad[3]
                self.isJumping = True

            elif curQuad[0] in ['+','-','*','/']:
                leftOperand = self.getValue(curQuad[1])
                rightOperand = self.getValue(curQuad[2])
                operator = curQuad[0]
                result = eval(f'{leftOperand} {operator} {rightOperand}')
                print(result)
                self.saveValue(curQuad[3], result)

            elif curQuad[0] == '=':
                self.saveValue(curQuad[3], self.getValue(curQuad[1]))

            if not self.isJumping:
                self.pointer += 1

    def getValue(self, adr):
        # If the address is global
        if 0 <= adr < 12500:
            return self.directory['global'][1][adr][1]

        # If the address is local
        elif 12500 <= adr < 25000:
            return self.getLocalValue(adr)

        # If the address is temp
        elif 25000 <= adr < 32500:
            # Temp int
            if 25000 <= adr < 27500:
                return self.temps[0][adr]
            # Temp float
            elif 27500 <= adr < 30000:
                return self.temps[1][adr]
            # Temp bool
            else:
                return self.temps[2][adr]

        # If the address is const
        elif 32500 <= adr < 42500:
            # Const int
            if 32500 <= adr < 35000:
                return self.consts[0][adr]
            # Const float
            elif 35000 <= adr < 37500:
                return self.consts[1][adr]
            # Const char
            elif 37500 <= adr < 40000:
                return self.consts[2][adr]
            # Const string
            else:
                return self.consts[3][adr]
        else:
            print('Error: value does not exist')
            return -1

    def saveValue(self, adr, value):
        # If it is global
        if 0 <= adr < 12500:
            self.directory['global'][1][adr][1] = value

        # If it is local
        elif 12500 <= adr < 25000:
            self.saveLocalValue(adr, value)

        # If it is temporary
        elif 25000 <= adr < 32500:
            # Temp int
            if 25000 <= adr < 27500:
                self.temps[0][adr] = value
            # Temp float
            elif 27500 <= adr < 30000:
                self.temps[1][adr] = value
            # Temp bool
            else:
                self.temps[2][adr] = value

        # If it is constant
        elif 32500 <= adr < 42500:
            # Const int
            if 32500 <= adr < 35000:
                self.consts[0][adr] = value
            # Const float
            elif 35000 <= adr < 37500:
                self.consts[1][adr] = value
            # Const char
            elif 37500 <= adr < 40000:
                self.consts[2][adr] = value
            # Const string
            else:
                self.consts[3][adr] = value
        else:
            print('Error: value could not be saved')

    def getLocalValue(self, adr):
        # If it is int
        if 12500 <= adr < 15000:
            adr -= 12500
            adr += self.intLpointer
            return self.localMem[0][adr]

        # If it is float
        elif 15000 <= adr < 17500:
            adr -= 15000
            adr += self.floatLpointer
            return self.localMem[1][adr]

        # If it is char
        elif 17500 <= adr < 20000:
            adr -= 17500
            adr += self.charLpointer
            return self.localMem[2][adr]

        # If it is string
        elif 20000 <= adr < 22500:
            adr -= 20000
            adr += self.stringLpointer
            return self.localMem[3][adr]

        # If it is a dataframe
        elif 22500 <= adr < 25000:
            print('dataframe')

    def saveLocalValue(self, adr, value):
        # If it is int
        if 12500 <= adr < 15000:
            adr -= 12500
            adr += self.intLpointer
            self.localMem[0][adr] = value

        # If it is float
        elif 15000 <= adr < 17500:
            adr -= 15000
            adr += self.floatLpointer
            self.localMem[1][adr] = value

        # If it is char
        elif 17500 <= adr < 20000:
            adr -= 17500
            adr += self.charLpointer
            self.localMem[2][adr] = value

        # If it is string
        elif 20000 <= adr < 22500:
            adr -= 20000
            adr += self.stringLpointer
            self.localMem[3][adr] = value

        # If it is a dataframe
        elif 22500 <= adr < 25000:
            print('dataframe')
