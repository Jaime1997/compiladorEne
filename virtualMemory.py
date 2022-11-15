class VirtualMemory(object):

    def __init__(self):
        # Global ranges
        self.intG = 0
        self.floatG = 2500
        self.charG = 5000
        self.stringG = 7500
        self.dataframeG = 10000

        # Local ranges
        self.intL = 12500
        self.floatL = 15000
        self.charL = 17500
        self.stringL = 20000
        self.dataframeL = 22500

        # Temporal ranges
        self.intT = 25000
        self.floatT = 27500
        self.boolT = 30000

        # Constant ranges
        self.intC = 32500
        self.floatC = 35000
        self.charC = 37500
        self.stringC = 40000

    # Increments the counter for stored variables
    # Returns the new variable's address
    def addVar(self, type, scope):
        if scope == 'global':
            if type == 'int':
                self.intG += 1
                return self.intG - 1
            elif type == 'float':
                self.floatG += 1
                return self.floatG - 1
            elif type == 'char':
                self.charG += 1
                return self.charG - 1
            elif type == 'string':
                self.stringG += 1
                return self.stringG - 1

        elif scope == 'local':
            if type == 'int':
                self.intL += 1
                return self.intL - 1
            elif type == 'float':
                self.floatL += 1
                return self.floatL - 1
            elif type == 'char':
                self.charL += 1
                return self.charL - 1
            elif type == 'string':
                self.stringL += 1
                return self.stringL - 1

        elif scope == 'temp':
            if type == 'int':
                self.intT += 1
                return self.intT - 1
            elif type == 'float':
                self.floatT += 1
                return self.floatT - 1
            elif type == 'bool':
                self.boolT += 1
                return self.boolT - 1

        elif scope == 'const':
            if type == 'int':
                self.intC += 1
                return self.intC - 1
            elif type == 'float':
                self.floatC += 1
                return self.floatC - 1
            elif type == 'char':
                self.charC += 1
                return self.charC - 1
            elif type == 'string':
                self.stringC += 1
                return self.stringC - 1

        else:
            return -1

    def addArray(self, type, scope, size):
        if scope == 'global':
            if type == 'int':
                self.intG += size
            elif type == 'float':
                self.floatG += size
            elif type == 'char':
                self.charG += size
            elif type == 'string':
                self.stringG += size

        elif scope == 'local':
            if type == 'int':
                self.intL += size
            elif type == 'float':
                self.floatL += size
            elif type == 'char':
                self.charL += size
            elif type == 'string':
                self.stringL += size

        elif scope == 'temp':
            if type == 'int':
                self.intT += size
            elif type == 'float':
                self.floatT += size
            elif type == 'bool':
                self.boolT += size

        elif scope == 'const':
            if type == 'int':
                self.intC += size
            elif type == 'float':
                self.floatC += size
            elif type == 'char':
                self.charC += size
            elif type == 'string':
                self.stringC += size

        else:
            return -1

    # Resets local memory register
    def resetLocalMemory(self):
        self.intL = 12500
        self.floatL = 15000
        self.charL = 17500
        self.stringL = 20000
        self.dataframeL = 22500