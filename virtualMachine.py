class VirtualMachine(object):

    def __init__(self, functionDirectoryTable, constantsTable,
                 temporalTable, parametersTable, quadruplesTable,):
        self.pointer = 0
        self.pointerBreadcrumb = []
        self.currentScope = "main"
        self.nextScope = ""
        self.scopeStack = []
        self.scopeReturnType = ""
        self.directory = functionDirectoryTable
        self.consts = constantsTable
        self.temps = temporalTable
        self.quads = quadruplesTable
        self.params = parametersTable
        self.returnValue = None

        self.pointer = 0
        self.isJumping = False

        self.recursionCounter = 0

        # Local pointers
        self.intLpointer = 0
        self.floatLpointer = 0
        self.charLpointer = 0
        self.stringLpointer = 0
        self.dataframeLpointer = 0

        # Local memory
        # int, float, char, string, dataframe
        self.localMem = [[None] * 2500, [None] * 2500, [None] * 2500, [None] * 2500, [None] * 2500]
        self.localMemSize = []
        self.arguments = [[]]
        self.arrDimension = []
        self.arrCalls = []

    def runProgram(self):
        eof = len(self.quads)

        while self.pointer < eof:
            self.isJumping = False
            curQuad = self.quads[self.pointer]
            print(curQuad)

            if curQuad[0] == 'GOTO':
                self.pointer = curQuad[3]
                self.isJumping = True

            elif curQuad[0] == 'GOTOF':
                if self.getValue(curQuad[1]) == False:
                    self.pointer = curQuad[3]
                    self.isJumping = True

            elif curQuad[0] == 'GOSUB':
                self.currentScope = self.nextScope
                self.scopeStack.append(curQuad[1])
                self.addFuncSizeToPointer()
                self.saveArgumentsInLocalMemory()
                self.recursionCounter += 1
                self.arguments.append([])

                self.pointerBreadcrumb.append(self.pointer)
                self.pointer = curQuad[3] - 1

            elif curQuad[0] == 'ERA':
                self.nextScope = curQuad[3]
                self.calcFuncSize(self.currentScope)

            elif curQuad[0] == 'ARGUMENT':
                if curQuad[3] == 'arg0':
                    self.arguments[self.recursionCounter] = []
                self.arguments[self.recursionCounter].append(self.getValue(curQuad[1]))

            elif curQuad[0] == 'NOARGS':
                self.arguments[self.recursionCounter] = []

            elif curQuad[0] == 'ENDFunc':
                self.pointer = self.pointerBreadcrumb.pop()
                self.currentScope = self.scopeStack.pop()
                self.exitFunction()
                self.recursionCounter -= 1
                self.arguments.pop()

            elif curQuad[0] == 'RETURN':
                self.returnValue = self.getValue(curQuad[1])
                self.pointer = self.pointerBreadcrumb.pop()
                self.currentScope = self.scopeStack.pop()
                self.exitFunction()
                self.recursionCounter -= 1
                self.arguments.pop()

            elif curQuad[0] == 'RETURNVALUE':
                self.saveValue(curQuad[3], self.returnValue)

            elif curQuad[0] == 'PRINT':
                print(self.getValue(curQuad[3]))

            elif curQuad[0] == 'WRITE':
                self.write(curQuad[3])

            elif curQuad[0] in ['MINUS']:
                leftOperand = "-1"
                operator = "*"
                rightOperand = self.getValue(curQuad[1])
                result = eval(f'{leftOperand} {operator} {rightOperand}')
                self.saveValue(curQuad[3], result)

            elif curQuad[0] in ['!']:
                result = not self.getValue(curQuad[1])
                self.saveValue(curQuad[3], result)

            elif curQuad[0] in ['+','-','*','/']:
                leftOperand = self.getValue(curQuad[1])
                rightOperand = self.getValue(curQuad[2])
                operator = curQuad[0]
                #print(leftOperand,operator,rightOperand)
                result = eval(f'{leftOperand} {operator} {rightOperand}')
                #print(result)
                self.saveValue(curQuad[3], result)

            elif curQuad[0] in ['<', '>', '<=', '>=', '==', "!=", "and", "or"]:
                leftOperand = self.getValue(curQuad[1])
                rightOperand = self.getValue(curQuad[2])
                operator = curQuad[0]
                #print(leftOperand,operator,rightOperand)
                result = eval(f'{leftOperand} {operator} {rightOperand}')
                self.saveValue(curQuad[3], result)

            elif curQuad[0] == 'VERIFY':
                idxValue = self.getValue(curQuad[1])
                lowerBound = curQuad[2]
                upperBound = curQuad[3]
                result = eval(f'{lowerBound} {"<="} {idxValue} {"<="} {upperBound}')
                if not result:
                    print("Error: out of bounds access")
                    exit()
                else:
                    self.arrDimension.append(idxValue)

            elif curQuad[0] == 'STOREIDX':
                self.arrCalls.append(self.arrDimension)
                self.arrDimension = []

            elif curQuad[0] == 'ARR=':
                indexes = self.arrCalls.pop()
                dimensions = len(indexes)
                idxOffset = 1
                i = 0

                while i < dimensions:
                    idxOffset += int(indexes.pop()) * self.directory[self.currentScope][1][curQuad[3]][3][2][i][2]
                    i += 1

                idxOffset += 1
                self.saveValue(curQuad[3] + idxOffset, self.getValue(curQuad[1]))

            elif curQuad[0] == 'ARRIDX':
                indexes = self.arrCalls.pop()
                dimensions = len(indexes)
                idxOffset = 1
                i = 0

                while i < dimensions:
                    idxOffset += int(indexes.pop()) * self.directory[self.currentScope][1][curQuad[1]][3][2][i][2]
                    i += 1

                idxOffset += 1
                self.saveValue(curQuad[3], self.getValue(curQuad[1] + idxOffset))

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

    def getType(self, adr):
        # If the address is global
        if 0 <= adr < 12500:
            return self.directory['global'][1][adr][0]

        # If the address is local
        elif 12500 <= adr < 25000:
            if 12500 <= adr < 15000:  # int
                return 'int'
            elif 15000 <= adr < 17500:  # float
                return 'float'
            elif 17500 <= adr < 20000:  # char
                return 'char'
            elif 20000 <= adr < 22500:  # string
                return 'string'
            elif 22500 <= adr < 25000:  # dataframe
                return 'dataframe'

        # If the address is temp
        elif 25000 <= adr < 32500:
            # Temp int
            if 25000 <= adr < 27500:
                return 'int'
            # Temp float
            elif 27500 <= adr < 30000:
                return 'float'
            # Temp bool
            else:
                return 'bool'

        # If the address is const
        elif 32500 <= adr < 42500:
            # Const int
            if 32500 <= adr < 35000:
                return 'int'
            # Const float
            elif 35000 <= adr < 37500:
                return 'float'
            # Const char
            elif 37500 <= adr < 40000:
                return 'char'
            # Const string
            else:
                return 'string'
        else:
            print('Error: value does not exist')

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

    def calcFuncSize(self, scope):
        i = self.directory[scope][0][3][0]
        f = self.directory[scope][0][3][1]
        c = self.directory[scope][0][3][2]
        s = self.directory[scope][0][3][3]
        d = self.directory[scope][0][3][4]
        self.localMemSize.append([i, f, c, s, d])

    def addFuncSizeToPointer(self):
        self.intLpointer += self.localMemSize[self.recursionCounter][0]
        self.floatLpointer += self.localMemSize[self.recursionCounter][1]
        self.charLpointer += self.localMemSize[self.recursionCounter][2]
        self.stringLpointer += self.localMemSize[self.recursionCounter][3]
        self.dataframeLpointer += self.localMemSize[self.recursionCounter][4]

    def saveArgumentsInLocalMemory(self):
        i = 0
        for j in self.arguments[self.recursionCounter]:
            if self.params[self.currentScope][i] == 'int':
                self.localMem[0][self.intLpointer + i] = j
            elif self.params[self.currentScope][i] == 'float':
                self.localMem[1][self.floatLpointer + i] = j
            elif self.params[self.currentScope][i] == 'char':
                self.localMem[2][self.charLpointer + i] = j
            elif self.params[self.currentScope][i] == 'string':
                self.localMem[3][self.stringLpointer + i] = j
            elif self.params[self.currentScope][i] == 'dataframe':
                self.localMem[4][self.dataframeLpointer + i] = j
            i += 1

    # Subtract memory size from local pointer
    def exitFunction(self):
        self.intLpointer -= self.localMemSize[-1][0]
        self.floatLpointer -= self.localMemSize[-1][1]
        self.charLpointer -= self.localMemSize[-1][2]
        self.stringLpointer -= self.localMemSize[-1][3]
        self.dataframeLpointer -= self.localMemSize[-1][4]
        self.localMemSize.pop()

    def write(self, adr):
        val = input("input>")
        type = self.getType(adr)
        try:
            if type == 'int':
                val = int(val)
                self.saveValue(adr, val)
            elif type == 'float':
                val = float(val)
                self.saveValue(adr, val)
            elif type == 'char':
                if len(val) > 1:
                    print('Char must be one character')
                    exit()
                self.saveValue(adr, val)
            elif type == 'string':
                self.saveValue(adr, val)
            else:
                print('Invalid input')
        except:
            print('Error: input/variable type mismatch')
            exit()
