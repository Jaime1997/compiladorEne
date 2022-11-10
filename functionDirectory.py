
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
        self.newScope = ""
        # Type of value being parsed.
        self.currentType = ""
        # Helps check argument/parameter number agreement
        self.argC = 0
        self.auxArrId = ""

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
        self.newScope = scope

    def setReturn(self, returnValue):
        self.currentScopeReturn = returnValue

    # Resets entire directory
    def eraseContext(self):
        self.directory = dict()

    # Erases the context of a function
    def eraseScope(self):
        self.directory[self.currentScope][1] = dict()

    # Checks if a table exists for the current context.
    def checkTableCurrentScope(self):
        if not self.currentScope in self.directory:
            self.directory[self.currentScope] = [[self.currentScopeReturn], dict()]
            self.parameterTable[self.currentScope] = []

    def addVariableToContext(self, id, adr):
        if id in self.directory[self.currentScope][1]:
            print("Error: variable already declared.")
        else:
            self.directory[self.currentScope][1][id] = [self.currentType, "value", adr, []]
            # Type, value, address, dimensions

    def addFunction(self, id):
        # If already declared, error
        if id in self.directory:
            print("Error: function already declared")
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
        return self.directory[self.newScope][0][2]

    def addParamTypeToTable(self, paramType):
        self.parameterTable[self.currentScope].append(paramType)

    # Counts number of parameters in a function
    def countParams(self):
        length = len(self.parameterTable[self.currentScope])
        if len(self.directory[self.currentScope][0]) > 1:
            self.directory[self.currentScope][0][1] = length
        else:
            self.directory[self.currentScope][0].append(length)

    def resetArgumentCounter(self):
        self.argC = 0

    def increaseArgumentCounter(self):
        self.argC = self.argC + 1

    def getArgumentCounter(self):
        return self.argC

    def checkArgType(self, argumentType):
        if argumentType == self.parameterTable[self.newScope][self.argC]:
            return True
        else:
            return False

    def checkParamArgumentLength(self):
        if self.argC == len(self.parameterTable[self.newScope]):
            return True
        else:
            return False

    def checkParamArgumentType(self,argumentType):
        if argumentType == self.parameterTable[self.newScope][self.paramC]:
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
            print("Error: variable type not found.")

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