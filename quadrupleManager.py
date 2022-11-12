class QuadrupleManager(object):

    def __init__(self):
        self.operandStack = []
        self.typeStack = []
        self.operatorStack = []
        self.jumpStack = []
        self.controlStack = []
        self.temporalIdx = 0

        # Quadruples come in the following format:
        # Operator, operand address, operand address, result address.
        self.quadrupleList = []

        self.semanticCube = {
            '=':{('int','int'):'int', ('float','float'):'float', ('char','char'):'char', ('string','string'):'string',},
            '-': {('int', 'int'): 'int', ('float', 'float'): 'float', ('int', 'float'): 'float',
                  ('float', 'int'): 'float'},
            '+': {('int', 'int'): 'int', ('float', 'float'): 'float', ('int', 'float'): 'float',
                  ('float', 'int'): 'float'},
            '/': {('int', 'int'): 'float', ('float', 'float'): 'float', ('int', 'float'): 'float',
                  ('float', 'int'): 'float'},
            '*': {('int', 'int'): 'int', ('float', 'float'): 'float', ('int', 'float'): 'float',
                  ('float', 'int'): 'float'},
            '<': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                  ('float', 'int'): 'bool'},
            '>': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                  ('float', 'int'): 'bool'},
            '<=': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                   ('float', 'int'): 'bool'},
            '>=': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                   ('float', 'int'): 'bool'},
            '!=': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                   ('float', 'int'): 'bool', ('char', 'char'): 'bool', ('string', 'string'): 'bool'},
            '==': {('int', 'int'): 'bool', ('float', 'float'): 'bool', ('int', 'float'): 'bool',
                   ('float', 'int'): 'bool', ('char', 'char'): 'bool', ('string', 'string'): 'bool'},
            '&&': {('bool', 'bool'): 'bool'},
            '||': {('bool', 'bool'): 'bool'},
            '!': {('bool'): 'bool'}
        }

    # Checks if an operation exists in the semantic cube.
    def verifyOperatorValidity(self, op, pair):
        if op in self.semanticCube:
            if pair in self.semanticCube[op]:
                return True
        return False

    # Returns the resulting value type of the operation
    # between a specific type pair.
    def getOperationResultType(self, op, pair):
        return self.semanticCube[op][pair]

    # Push to operand stack.
    def pushOperandStack(self, operand):
        self.operandStack.append(operand)

    # Pop operand stack.
    def popOperandStack(self):
        if self.operandStack:
            return self.operandStack.pop()
        else:
            print("Operand stack empty.")

    # Push to type stack.
    def pushTypeStack(self, type):
        self.typeStack.append(type)

    # Pop type stack.
    def popTypeStack(self):
        if self.typeStack:
            return self.typeStack.pop()
        else:
            print("Type stack empty.")

    # Push to operator stack.
    def pushOperatorStack(self, operator):
        self.operatorStack.append(operator)

    # Pop operator stack.
    def popOperatorStack(self):
        if self.operatorStack:
            return self.operatorStack.pop()
        else:
            print("Operator stack empty.")

    # Gets top operator in operator stack without popping.
    def topOperatorStack(self):
        if self.operatorStack:
            return self.operatorStack[-1]

    # Push to control stack.
    def pushControlStack(self, x):
        self.controlStack.append(x)

    # Pop control stack.
    def popControlStack(self):
        if self.controlStack:
            return self.controlStack.pop()

    # Push to jump stack.
    def pushJumpStack(self, jump):
        self.jumpStack.append(jump)

    # Pop jump stack.
    def popJumpStack(self):
        if self.jumpStack:
            return self.jumpStack.pop()
        else:
            print("Jump stack is empty.")

    # Prints result index.
    def temporalCounter(self):
        return "t" + str(self.temporalIdx)

    # Adds 1 to the result index.
    def increaseTempCount(self):
        self.temporalIdx = self.temporalIdx + 1

    # Push quadruple to list.
    def pushQuadruple(self, op, left, right, result):
        self.quadrupleList.append([op, left, right, result])

    # Returns size of quadruple list.
    def quadCount(self):
        return len(self.quadrupleList)

    # Fills missing jump information in quadruples
    def fill(self, end, cont):
        self.quadrupleList[end][3] = cont

    # Finds program start and sets initial goto.
    def setMainGotoAddress(self):
        self.quadrupleList[0][3] = self.quadCount()

    # Gets quadruple list.
    def getQuadrupleList(self):
        return self.quadrupleList

    # Prints quadruple list.
    def printQuadrupleList(self):
        x = 0
        for i in self.quadrupleList:
            print("------------------------")
            print(x, end='| ')
            print(i[0], end=' |')
            print(i[1], end=' |')
            print(i[2], end=' |')
            print(i[3])
            x = x + 1
        print("------------------------")
