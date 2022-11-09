
class FunctionDirectory(object):

    def __init__(self):
        # Global scope and functions
        # Format: directory[scope][1(id array)][id(dictionary)][type,value,address,dimensions]
        self.directory = dict()
        # Int, float, char, string
        self.constTable = [dict(), dict(), dict(), dict()]
        # Int, float, bool
        self.tempTable = [dict(), dict(), dict()]
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
        self.paramC = 0
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

        for i in self.directory:
            exportTable[i] = [self.directory[i][0], dict()]
            for j in self.directory[i][1]:
                exportTable[i][1][self.getAddressVar(j)] = self.directory[i][1][j]

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