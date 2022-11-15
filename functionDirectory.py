
class FunctionDirectory(object):

    def __init__(self):
        # Global scope and functions
        # Format: directory[scope][1(id array)][id(dictionary)][type,value,address,dimensions]
        self.directory = dict()
        # Int, float, char, string
        self.constTable = [dict(), dict(), dict(), dict()]
        # Int, float, bool
        self.tempTable = [dict(), dict(), dict()]
        # Parameter table
        #self.parameterTable = dict()
        # Name of currently running program
        self.programName = ""
        # Global or local scope
        self.currentScope = ""
        # Function return value
        self.currentScopeReturn = ""
        # Scope to be created
        self.newScope = []
        # Type of value being parsed.
        self.currentType = ""
        # Helps check argument/parameter number agreement
        self.funcC = -1
        self.argC = []
        # Helps initialize dimensioned variables.
        self.arrDimensions = []
        self.auxArrId = ""
        self.auxArrType = ""

    def addProgram(self, id):
        self.programName = id
        self.directory["global"] = [["void", 0], dict()]
        self.directory["main"] = [["void", 0], dict()]
        self.parameterTable = dict()
        self.currentScope = "global"

    def getCurrentType(self):
        return self.currentType

    def setType(self, type):
        self.currentType = type

    def getScope(self):
        if self.currentScope == 'global':
            return 'global'
        else:
            return 'local'

    def setScope(self, scope):
        self.currentScope = scope

    def setNewScope(self, scope):
        self.newScope.append(scope)

    def setReturn(self, returnValue):
        self.currentScopeReturn = returnValue

    # Resets entire directory
    def eraseContext(self):
        self.directory = dict()

    # Erases the context of a function
    def eraseScope(self):
        self.directory[self.currentScope][1] = dict()


    def addVariableToContext(self, id, adr):
        if id in self.directory[self.currentScope][1]:
            print("Error: variable already declared.")
            exit()
        else:
            self.directory[self.currentScope][1][id] = [self.currentType, "value", adr, []]
            # Type, value, address, dimensions

    def removeVariableToContext(self, id):
        if id in self.directory[self.currentScope][1]:
            del self.directory[self.currentScope][1][id]
        else:
            print("Error: variable doesn't exist.")
            exit()

    def addFunction(self, id):
        # If already declared, error
        if id in self.directory:
            print("Error: function already declared")
            exit()
        # If not declared, add to directory
        else:
            self.directory[id] = [[self.currentScopeReturn], dict()]
            self.parameterTable[self.currentScope] = []

    def functionExists(self, id):
        if id in self.directory:
            return True
        else:
            return False

    def countLocalVar(self):
        int = 0
        float = 0
        char = 0
        string = 0
        dataframe = 0
        for i in self.directory[self.currentScope][1]:
            if self.directory[self.currentScope][1][i][0] == 'int':
                int += 1
            elif self.directory[self.currentScope][1][i][0] == 'float':
                float += 1
            elif self.directory[self.currentScope][1][i][0] == 'char':
                char += 1
            elif self.directory[self.currentScope][1][i][0] == 'string':
                string += 1
            elif self.directory[self.currentScope][1][i][0] == 'dataframe':
                dataframe += 1

        if len(self.directory[self.currentScope][0]) > 3:
            print('error: el indice del arreglo esta mal')
        else:
            self.directory[self.currentScope][0].append([int, float, char, string, dataframe])

    def setQuadCounter(self, count):
        if len(self.directory[self.currentScope][0]) > 3:
            self.directory[self.currentScope][0][3] = count
        else:
            self.directory[self.currentScope][0].append(count)

    def getFunctionStartNumber(self):
        return self.directory[self.newScope[self.funcC]][0][2]

    def addParamTypeToTable(self, paramType):
        self.parameterTable[self.currentScope].append(paramType)

    # Counts number of parameters in a function
    def countParams(self):
        length = len(self.parameterTable[self.currentScope])
        if len(self.directory[self.currentScope][0]) > 1:
            self.directory[self.currentScope][0][1] = length
        else:
            self.directory[self.currentScope][0].append(length)

    def popArgumentCounter(self):
        self.argC.pop()

    def popScopeStack(self):
        self.newScope.pop()

    def initArgumentCounter(self):
        self.argC.append(0)

    def pushDimensionStack(self, dimension):
        self.arrDimensions.append(dimension)

    def popDimensionStack(self):
        return self.arrDimensions.pop()

    def initArray(self, id):
        numDimensions = len(self.arrDimensions)
        size = 1

        # Init array
        self.directory[self.currentScope][1][id][3] = [0, 1, []] # dim, r, [lim inf, lim sup, m/k]
        self.directory[self.currentScope][1][id][3][0] = numDimensions # List number of dimensions

        # Add table for each dimension
        while self.arrDimensions:
            upperLimit = self.arrDimensions.pop()
            self.directory[self.currentScope][1][id][3][2].append([0, upperLimit - 1, size])
            size *= upperLimit

        self.directory[self.currentScope][1][id][3][1] = size

    def getArrayIdxId(self):

        i = 0
        baseAdr = self.directory[self.currentScope][1][self.auxArrId][2]

        while self.arrDimensions:
            idx = self.arrDimensions.pop()
            baseAdr += self.directory[self.currentScope][1][self.auxArrId][3][2][i][2] * int(idx)
            i += 1

        baseAdr += 1
        return baseAdr

    def getArraySize(self, id):
        return self.directory[self.currentScope][1][id][3][1]

    def getArrayDimensions(self, id):
        return self.directory[self.currentScope][1][id][3][0]

    def getArrayUpperBound(self, id, dimensionNum):
        return self.directory[self.currentScope][1][id][3][2][dimensionNum-1][1]

    def isIdArray(self, id):
        if self.directory[self.currentScope][1][id][3]:
            return True
        else:
            return False

    def setAuxArr(self, id, type):
        self.auxArrId = id
        self.auxArrType = type

    def increaseFunctionCallCounter(self):
        self.funcC = self.funcC + 1

    def decreaseFunctionCallCounter(self):
        self.funcC = self.funcC - 1

    def increaseArgumentCounter(self):
        self.argC[self.funcC] = self.argC[self.funcC] + 1

    def getArgumentCounter(self):
        return self.argC[self.funcC]

    def checkArgType(self, argumentType):
        if argumentType == self.parameterTable[self.newScope[self.funcC]][self.argC[self.funcC]]:
            return True
        else:
            return False

    def checkParamArgumentLength(self):
        if self.argC[self.funcC] == len(self.parameterTable[self.newScope[self.funcC]]):
            return True
        else:
            return False

    def checkParamArgumentType(self,argumentType):
        if argumentType == self.parameterTable[self.newScope[self.funcC]][self.paramC]:
            return True
        else:
            print("Error: parameter/argument type mismatch")
            return False

    def addConst(self, id, type, adr):
        if type == 'int':
            self.constTable[0][id] = adr
        elif type == 'float':
            self.constTable[1][id] = adr
        elif type == 'char':
            self.constTable[2][id] = adr
        elif type == 'string':
            self.constTable[3][id] = adr

    def addTemp(self, id, type, adr):
        if type == 'int':
            self.tempTable[0][id] = adr
        elif type == 'float':
            self.tempTable[1][id] = adr
        elif type == 'bool':
            self.tempTable[2][id] = adr
        else:
            print("Error: unable to save value type " + type)

    def getVariableType(self, id):
        # Checks if it exists in the current scope
        if id in self.directory[self.currentScope][1]:
            return self.directory[self.currentScope][1][id][0]
        # Checks if it exists in the global context
        elif id in self.directory["global"][1]:
            return self.directory["global"][1][id][0]
        else:
            print("Error: variable doesn't exist")
            exit()

    def getFunctionType(self, id):
        # Checks if it exists in the current scope
        if id in self.directory:
            return self.directory[id][0][0]
        else:
            print("Error: function type not found.")

    # Checks if a variable exists
    def variableExists(self, id):
        # Checks in current scope
        if id in self.directory[self.currentScope][1]:
            return True
        # Checks in global scope
        elif id in self.directory["global"][1]:
            return True
        # Doesn't exist
        else:
            return False

    # Gets the address of variables. Depending on the variable's type
    # it calls a different function
    def getAddress(self, id, type):
        if self.variableExists(id):
            return self.getAddressVar(id)
        elif self.isTemp(id, type):
            return self.getAddressTemp(id, type)
        elif self.isConst(id, type):
            return self.getAddressConst(id, type)
        else:
            print("Error: variable " + id + " not found")

    # Returns the memory address of a variable
    def getAddressVar(self, id):
        # Checks in current scope
        if id in self.directory[self.currentScope][1]:
            return self.directory[self.currentScope][1][id][2]
        # Checks in global scope
        elif id in self.directory["global"][1]:
            return self.directory["global"][1][id][2]
        else:
            print("Error: variable address not found.")

    # Gets the address of a constant
    def getAddressConst(self, id, type):
        if type == 'int':
            return self.constTable[0][id]
        elif type == 'float':
            return self.constTable[1][id]
        elif type == 'char':
            return self.constTable[2][id]
        elif type == 'string':
            return self.constTable[3][id]
        else:
            return -1

    # Gets the address of a temporal variable
    def getAddressTemp(self, id, type):
        if type == 'int':
            return self.tempTable[0][id]
        elif type == 'float':
            return self.tempTable[1][id]
        elif type == 'bool':
            return self.tempTable[2][id]
        else:
            print("Error: temporal variable not found")

    # Checks if a variable is constant
    def isConst(self, id, type):
        if type == 'int':
            if id in self.constTable[0]:
                return True
        elif type == 'float':
            if id in self.constTable[1]:
                return True
        elif type == 'char':
            if id in self.constTable[2]:
                return True
        elif type == 'string':
            if id in self.constTable[3]:
                return True
        return False

    # Checks if a variable is temporal
    def isTemp(self, id, type):
        if type == 'int':
            if id in self.tempTable[0]:
                return True
        elif type == 'float':
            if id in self.tempTable[1]:
                return True
        elif type == 'bool':
            if id in self.tempTable[2]:
                return True
        return False

    # Exports
    def exportVariables(self):
        exportTable = dict()

        for scope in self.directory:
            exportTable[scope] = [self.directory[scope][0], dict()]
            self.setScope(scope)
            for vars in self.directory[scope][1]:
                exportTable[scope][1][self.getAddressVar(vars)] = self.directory[scope][1][vars]

        return exportTable

    def exportConsts(self):
        export = [dict(), dict(), dict(), dict()]
        for i in self.constTable[0]:  # int
            export[0][self.constTable[0][i]] = i
        for i in self.constTable[1]:  # float
            export[1][self.constTable[1][i]] = i
        for i in self.constTable[2]:  # char
            export[2][self.constTable[2][i]] = i
        for i in self.constTable[3]:  # string
            export[3][self.constTable[3][i]] = i
        return export

    def exportTemps(self):
        export = [dict(), dict(), dict()]
        for i in self.tempTable[0]:  # int
            export[0][self.tempTable[0][i]] = 0
        for i in self.tempTable[1]:  # float
            export[1][self.tempTable[1][i]] = 0.0
        for i in self.tempTable[2]:  # bool
            export[2][self.tempTable[2][i]] = True
        return export

    def exportParams(self):
        return self.parameterTable

    def printDirectory(self):  # imprime funDir

        for key, value in self.directory.items():
            print("------------------------")
            print(key)
            print('return: ', end='')
            print(value[0])
            for i in value[1]:
                print(i, end=': ')
                print(self.directory[key][1][i])