from sly import Parser
from lexer import *

from functionDirectory import *
from quadrupleManager import *
from virtualMemory import *
from virtualMachine import *

directory = FunctionDirectory()
quadruples = QuadrupleManager()
memory = VirtualMemory()

class EneParser(Parser):
    # Import tokens from lexer
    tokens = EneLexer.tokens

    # We operate from left to right,
    # multiplication has higher precedence than addition.
    precedence = (
        ('left','+','-'),
        ('left','*','/'),
    )

    # Grammar rules

    # Last node to be parsed
    @_('programDeclaration ";" programBody')
    def program(self, p):
        # Init virtual machine.
        virtualMachine = VirtualMachine(directory.exportVariables(),
                                        directory.exportConsts(),
                                        directory.exportTemps(),
                                        directory.exportParams(),
                                        quadruples.getQuadrupleList())

        # Pass quadruples onto virtual machine and run it
        virtualMachine.runProgram()
        return p

    # Program init
    @_('PROGRAM ID')
    def programDeclaration(self, p):
        # Initializes directory
        directory.addProgram(p[1])
        # Add goto main instruction
        quadruples.pushQuadruple("GOTO","","","main")
        return p

    # Optionally declare global variables
    @_('globalVars MAIN setScopeToMain "(" ")" block countMain eof')
    def programBody(self, p):
        return p

    # Don't declare variables nor functions and go to main function
    @_('MAIN setScopeToMain "(" ")" block countMain eof')
    def programBody(self, p):
        return p

    # Sets scope to main
    @_('')
    def setScopeToMain(self, p):
        directory.setScope("main")
        quadruples.setMainGotoAddress()
        directory.setQuadCounter(quadruples.quadCount())
        return p

    @_('')
    def countMain(self, p):
        directory.countLocalVar()
        return p

    # Optionally declare functions after global variables.
    @_('var declareFunctions')
    def globalVars(self, p):
        return p

    # Declare global variables like normal variables.
    @_('var')
    def globalVars(self, p):
        return p

    # Just declare functions.
    @_('declareFunctions')
    def globalVars(self, p):
        return p

    # Variable declaration
    @_('typeDeclaration')
    def var(self, p):
        return p

    # Declare a single id
    @_('type addVarToContext ";"')
    def typeDeclaration(self, p):
        return p

    @_('type addArray ";"')
    def typeDeclaration(self, p):
        return p

    # Declare multiple ids of a single type
    @_('type addVarToContext "," multiVar')
    def typeDeclaration(self, p):
        return p

    @_('type addArray "," multiVar')
    def typeDeclaration(self, p):
        return p

    # Single id of one type, begin declaring ids of another type
    @_('type addVarToContext ";" typeDeclaration')
    def typeDeclaration(self, p):
        return p

    @_('type addArray ";" typeDeclaration')
    def typeDeclaration(self, p):
        return p

    # End same type declaration loop
    @_('addVarToContext ";"')
    def multiVar(self, p):
        return p

    @_('addArray ";"')
    def multiVar(self, p):
        return p

    # Same type declaration loop
    @_('addVarToContext "," multiVar')
    def multiVar(self, p):
        return p

    @_('addArray "," multiVar')
    def multiVar(self, p):
        return p

    # End same type declaration loop
    # and begin declaring another type
    @_('addVarToContext ";" typeDeclaration')
    def multiVar(self, p):
        return p

    @_('addArray ";" typeDeclaration')
    def multiVar(self, p):
        return p

    @_('ID')
    def addVarToContext(self, p):
        directory.addVariableToContext(p[0],
                                       memory.addVar(directory.getCurrentType(), directory.getScope()))
        return p

    @_('addVarToContext addDimensions')
    def addArray(self, p):
        directory.initArray(p[0][1])
        memory.addArray(directory.getCurrentType(), directory.getScope(), directory.getArraySize(p[0][1]))
        return p

    @_('"[" CTEINT "]"')
    def addDimensions(self, p):
        if int(p[1]) < 1:
            print("Error: Dimensions must be 1 or higher.")
            exit()
        else:
            directory.pushDimensionStack(int(p[1]))
        return p

    @_('"[" CTEINT "]" addDimensions')
    def addDimensions(self, p):
        if int(p[1]) < 1:
            print("Error: Dimensions must be 1 or higher.")
            exit()
        else:
            directory.pushDimensionStack(int(p[1]))
        return p

    @_('INT')
    def type(self, p):
        directory.setType("int")
        return p

    @_('FLOAT')
    def type(self, p):
        directory.setType("float")
        return p

    @_('CHAR')
    def type(self, p):
        directory.setType("char")
        return p

    @_('STRING')
    def type(self, p):
        directory.setType("string")
        return p

    @_('DATAFRAME')
    def type(self, p):
        directory.setType("dataframe")
        return p

    # Optionally declare many functions
    @_('functions declareFunctions')
    def declareFunctions(self, p):
        return p

    # Declare function
    @_('functions')
    def declareFunctions(self, p):
        return p

    # Declare function and parameters
    @_('functionDeclaration parameterDeclaration')
    def functions(self, p):
        return p

    # Declare function
    @_('FUNC type ID')
    def functionDeclaration(self, p):
        directory.setScope(p[2])
        directory.setReturn(directory.getCurrentType())
        directory.addFunction(p[2])
        return p

    # Function with parameters
    @_('"(" param ")" countparam block endFunc')
    def parameterDeclaration(self, p):
        return p

    # No parameter function
    @_('"(" ")" countparam block endFunc')
    def parameterDeclaration(self, p):
        return p

    # Count parameters
    @_('')
    def countparam(self, p):
        directory.countParams()
        directory.setQuadCounter(quadruples.quadCount())
        return p

    @_('paramDeclaration "," param')
    def param(self, p):
        return p

    @_('paramDeclaration')
    def param(self, p):
        return p

    @_('type ID')
    def paramDeclaration(self, p):
        directory.addVariableToContext(
            p[1],
            memory.addVar(directory.getCurrentType(), directory.getScope()))
        directory.addParamTypeToTable(directory.getCurrentType())
        return p

    # End function
    @_('')
    def endFunc(self, p):
        quadruples.pushQuadruple("ENDFunc", "", "", "")
        directory.countLocalVar()
        memory.resetLocalMemory()
        return p

    @_('"{" "}"')
    def block(self, p):
        return p

    @_('"{" block "}"')
    def block(self, p):
        return p

    @_('"{" blockCont')
    def block(self, p):
        return p

    @_('statement blockCont')
    def blockCont(self, p):
        return p

    @_('statement "}"')
    def blockCont(self, p):
        return p

    @_('var')
    def statement(self, p):
        return p

    @_('assignation')
    def statement(self, p):
        return p

    @_('condition')
    def statement(self, p):
        return p

    @_('whileStatement')
    def statement(self, p):
        return p

    @_('forStatement')
    def statement(self, p):
        return p

    @_('printStatement')
    def statement(self, p):
        return p

    @_('writeStatement')
    def statement(self, p):
        return p

    @_('loadStatement')
    def statement(self, p):
        return p

    @_('medianCalc')
    def statement(self, p):
        return p

    @_('correlationCalc')
    def statement(self, p):
        return p

    @_('returnStatement')
    def statement(self, p):
        return p

    @_('ID "=" expression ";"')
    def assignation(self, p):

        # Gets expression operand
        expOperand = quadruples.popOperandStack()
        # Gets expression type
        expType = quadruples.popTypeStack()
        # Gets id type
        idType = directory.getVariableType(p[0])

        # If the operands are of the same type, assign id's address to
        # the expression's address
        if quadruples.verifyOperatorValidity('=',(expType,idType)):
            quadruples.pushQuadruple(
                '=',directory.getAddress(expOperand,expType),
                "",directory.getAddressVar(p[0]))
        else:
            print("Type mismatch.")
        return p

    @_('arrayId arrayIndexes saveArrIdx "=" expression ";"')
    def assignation(self, p):

        if directory.getArrayDimensions(directory.auxArrId[-1]) != len(directory.arrIndexes[-1]):
            print("Error: incorrect indexing")
            exit()

        baseAdr = directory.getArrayBaseDir()

        expOperand = quadruples.popOperandStack()
        expType = quadruples.popTypeStack()

        if quadruples.verifyOperatorValidity('=',(expType,directory.auxArrType[-1])):
            quadruples.pushQuadruple(
                'ARR=',
                directory.getAddress(expOperand,expType),
                "",
                baseAdr)
        else:
            print("Type mismatch.")
            exit()

        directory.arrIndexes.pop()
        directory.auxArrId.pop()
        directory.auxArrType.pop()
        return p

    @_('ID')
    def arrayId(self, p):
        if not directory.isIdArray(p[0]):
            print("Error: variable " + p[0] + " is not dimensioned")
            exit()

        directory.setAuxArr(p[0], directory.getVariableType(p[0]))
        return p

    @_('')
    def saveArrIdx(self, p):
        quadruples.pushQuadruple('STOREIDX',"","","")
        return p

    @_('"[" exp "]"')
    def arrayIndexes(self, p):
        indexType = quadruples.popTypeStack()
        if indexType == 'int':
            indexValue = quadruples.popOperandStack()
            directory.pushIndexStack(indexValue)
            quadruples.pushQuadruple(
                'VERIFY',
                directory.getAddress(indexValue, indexType),
                "0",
                directory.getArrayUpperBound(directory.auxArrId[-1], len(directory.arrIndexes[-1])))
        else:
            print("Error: array indexes must be integers.")
            exit()
        return p

    @_('"[" exp "]" arrayIndexes')
    def arrayIndexes(self, p):
        indexType = quadruples.popTypeStack()
        if indexType == 'int':
            indexValue = quadruples.popOperandStack()
            directory.pushIndexStack(indexValue)
            quadruples.pushQuadruple(
                'VERIFY',
                directory.getAddress(indexValue, indexType),
                "0",
                directory.getArrayUpperBound(directory.auxArrId[-1], len(directory.arrIndexes[-1])))
        else:
            print("Error: array indexes must be integers.")
            exit()
        return p

    @_('PRINT "(" printExpressions')
    def printStatement(self, p):
        return p

    @_('printExp "," printExpressions')
    def printExpressions(self, p):
        return p

    @_('printExp ")" ";"')
    def printExpressions(self, p):
        return p

    @_('expression')
    def printExp(self, p):
        id = quadruples.popOperandStack()
        type = quadruples.popTypeStack()
        directory.getAddress(id, type)

        quadruples.pushQuadruple("PRINT", "", "", directory.getAddress(id, type))
        return p

    @_('WRITE "(" inputIds')
    def writeStatement(self, p):
        return p

    @_('inputId "," inputIds')
    def inputIds(self, p):
        return p

    @_('inputId ")" ";"')
    def inputIds(self, p):
        return p

    @_('ID')
    def inputId(self, p):
        if directory.variableExists(p[0]):
            quadruples.pushQuadruple('WRITE', "", "", directory.getAddressVar(p[0]))
        return p

    @_('LOAD "(" ID "," CTESTRING "," CTEINT "," CTEINT ")" ";"')
    def loadStatement(self, p):
        if directory.getVariableType(p[2]) != 'dataframe':
            print("Error: files must be loaded onto a dataframe type variable")
            exit()

        maxVars = int(p[6])
        maxLines = int(p[8])

        if maxVars < 1 or maxLines < 1:
            print("Error: maxlines/maxvars can not be less than 1")
            exit()

        quadruples.pushQuadruple('LOAD', p[4].replace('"', ''), "", directory.getAddressVar(p[2]))
        quadruples.pushQuadruple('READF', maxVars, maxLines, directory.getAddressVar(p[2]))
        size = (maxVars+1) * maxLines
        directory.initDataframe(p[2],maxVars,maxLines)
        memory.addArray("dataframe", directory.getScope(), size)
        return p

    @_('MEDIAN "(" ID ")" ";"')
    def medianCalc(self, p):
        if directory.getVariableType(p[2]) != 'dataframe':
            print("Error: statistical analysis can only be done on a dataframe variable")
            exit()

        quadruples.pushQuadruple('MEDIAN',
                                 directory.getDataframeLimits(p[2]),
                                 "",
                                 directory.getAddressVar(p[2]))
        return p

    @_('CORRELATE "(" ID "," listVariables ")" ";"')
    def correlationCalc(self, p):
        if directory.getVariableType(p[2]) != 'dataframe':
            print("Error: statistical analysis can only be done on a dataframe variable")
            exit()

        quadruples.pushQuadruple('CORRELATE',
                                 directory.getDataframeLimits(p[2]),
                                 quadruples.operandStack,
                                 directory.getAddressVar(p[2]))
        quadruples.operandStack = []
        return p

    @_('CTEINT "," listVariables')
    def listVariables(self, p):
        quadruples.pushOperandStack(int(p[0]))
        return p

    @_('CTEINT')
    def listVariables(self, p):
        quadruples.pushOperandStack(int(p[0]))
        return p

    @_('CORRELATE "(" ID ")" ";"')
    def correlationCalc(self, p):
        if directory.getVariableType(p[2]) != 'dataframe':
            print("Error: statistical analysis can only be done on a dataframe variable")
            exit()

        quadruples.pushQuadruple('CORRELATE',
                                 directory.getDataframeLimits(p[2]),
                                 [],
                                 directory.getAddressVar(p[2]))
        return p

    @_('RETURN expression ";"')
    def returnStatement(self, p):
        returnValue = quadruples.popOperandStack()
        returnType = quadruples.popTypeStack()
        quadruples.pushQuadruple("RETURN",directory.getAddress(returnValue, returnType),'','')
        return p

    @_('exp')
    def expression(self, p):
        return p

    @_('compExp')
    def expression(self, p):
        return p

    @_('compExp AND compExp')
    def compExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('and', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('and', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('and', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('compExp OR compExp')
    def compExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('or', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('or', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('or', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('"!" exp comparisonExp')
    def compExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('!', (rightType)):
            resultType = quadruples.getOperationResultType('!', (rightType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('!',
                                     directory.getAddress(rightOperand, rightType),
                                     "",
                                     adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('exp comparisonExp')
    def compExp(self, p):
        return p

    @_('">" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('>', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('>', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('>', directory.getAddress(leftOperand, leftType), directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('">" "=" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('>=', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('>=', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('>=', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('"<" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('<', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('<', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('<', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('"<" "=" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('<=', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('<=', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('<=', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('"=" "=" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('==', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('==', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('==', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('"!" "=" exp')
    def comparisonExp(self, p):
        rightOperand = quadruples.popOperandStack()
        rightType = quadruples.popTypeStack()
        leftOperand = quadruples.popOperandStack()
        leftType = quadruples.popTypeStack()
        if quadruples.verifyOperatorValidity('!=', (rightType, leftType)):
            resultType = quadruples.getOperationResultType('!=', (rightType, leftType))
            adr = memory.addVar(resultType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), resultType, adr)
            quadruples.pushQuadruple('!=', directory.getAddress(leftOperand, leftType),
                                     directory.getAddress(rightOperand, rightType), adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.pushTypeStack(resultType)
            quadruples.increaseTempCount()
        return p

    @_('')
    def unaryOp(self, p):
        # If we're doing addition or subtraction
        if quadruples.topOperatorStack() == '-':
            # We take the left, right values, and the operator
            rightOperand = quadruples.popOperandStack()
            rightType = quadruples.popTypeStack()
            operator = quadruples.popOperatorStack()

            # If operation exists in semantic cube
            if quadruples.verifyOperatorValidity(operator, rightType):
                # Get result type and add it to temporal variables
                resultType = quadruples.getOperationResultType(operator, rightType)
                adr = memory.addVar(resultType, 'temp')
                directory.addTemp(quadruples.temporalCounter(), resultType, adr)
                # Create new quadruple with operation
                quadruples.pushQuadruple("MINUS",
                                         directory.getAddress(rightOperand, rightType),
                                         "",
                                         adr)
                # Push temp to operands/type stacks
                quadruples.pushOperandStack(quadruples.temporalCounter())
                quadruples.pushTypeStack(resultType)
                # Increase temporal index variable
                quadruples.increaseTempCount()
            else:
                print("Error: Operand types not compatible")
        return p

    @_('')
    def binaryOp1(self, p):
        # If we're doing addition or subtraction
        if quadruples.topOperatorStack() == '+' or quadruples.topOperatorStack() == '-':
            # We take the left, right values, and the operator
            rightOperand = quadruples.popOperandStack()
            rightType = quadruples.popTypeStack()
            leftOperand = quadruples.popOperandStack()
            leftType = quadruples.popTypeStack()
            operator = quadruples.popOperatorStack()

            # If operation exists in semantic cube
            if quadruples.verifyOperatorValidity(operator,(rightType,leftType)):
                # Get result type and add it to temporal variables
                resultType = quadruples.getOperationResultType(operator,(rightType,leftType))
                adr = memory.addVar(resultType,'temp')
                directory.addTemp(quadruples.temporalCounter(), resultType, adr)
                # Create new quadruple with operation
                quadruples.pushQuadruple(operator,
                                         directory.getAddress(leftOperand,leftType),
                                         directory.getAddress(rightOperand,rightType),
                                         adr)
                # Push temp to operands/type stacks
                quadruples.pushOperandStack(quadruples.temporalCounter())
                quadruples.pushTypeStack(resultType)
                # Increase temporal index variable
                quadruples.increaseTempCount()
            else:
                print("Error: Operand types not compatible")
        return p

    @_('')
    def binaryOp2(self, p):
        # If we're doing multiplication or division
        if quadruples.topOperatorStack() == '*' or quadruples.topOperatorStack() == '/':
            # We take the left, right values, and the operator
            rightOperand = quadruples.popOperandStack()
            rightType = quadruples.popTypeStack()
            leftOperand = quadruples.popOperandStack()
            leftType = quadruples.popTypeStack()
            operator = quadruples.popOperatorStack()

            # If operation exists in semantic cube
            if quadruples.verifyOperatorValidity(operator, (rightType, leftType)):
                # Get result type and add it to temporal variables
                resultType = quadruples.getOperationResultType(operator, (rightType, leftType))
                adr = memory.addVar(resultType, 'temp')
                directory.addTemp(quadruples.temporalCounter(), resultType, adr)
                # Create new quadruple with operation
                quadruples.pushQuadruple(operator,
                                         directory.getAddress(leftOperand, leftType),
                                         directory.getAddress(rightOperand, rightType),
                                         adr)
                # Push temp to operands/type stacks
                quadruples.pushOperandStack(quadruples.temporalCounter())
                quadruples.pushTypeStack(resultType)
                # Increase temporal index variable
                quadruples.increaseTempCount()
            else:
                print("Error: Operand types not compatible")
        return p

    @_('term binaryOp1')
    def exp(self, p):
        return p

    @_('sumOp exp')
    def exp(self, p):
        return p

    @_('term binaryOp1 "+"')
    def sumOp(self, p):
        quadruples.pushOperatorStack(p[2])
        return p

    @_('subOp exp')
    def exp(self, p):
        return p

    @_('term binaryOp1 "-"')
    def subOp(self, p):
        quadruples.pushOperatorStack(p[2])
        return p

    @_('factor binaryOp2')
    def term(self, p):
        return p

    @_('multOp term')
    def term(self, p):
        return p

    @_('factor binaryOp2 "*"')
    def multOp(self, p):
        quadruples.pushOperatorStack(p[2])
        return p

    @_('divOp term')
    def term(self, p):
        return p

    @_('factor binaryOp2 "/"')
    def divOp(self, p):
        quadruples.pushOperatorStack(p[2])
        return p

    @_('negOp unaryOp')
    def factor(self, p):
        return p

    @_('"-" factor')
    def negOp(self, p):
        quadruples.pushOperatorStack(p[0])
        return p

    @_('functionCall')
    def factor(self, p):
        return p

    @_('pushFakeBottom "(" expression ")" popFakeBottom')
    def factor(self, p):
        return p

    @_('')
    def pushFakeBottom(self, p):
        quadruples.pushOperatorStack('(')
        return p

    @_('')
    def popFakeBottom(self, p):
        quadruples.popOperatorStack()
        return p

    @_('varcte')
    def factor(self, p):
        return p

    @_('functionId "(" ")" noArgs validateParamSize')
    def functionCall(self, p):
        return p

    @_('functionId "(" argumentInput')
    def functionCall(self, p):
        return p

    @_('ID')
    def functionId(self, p):
        if directory.functionExists(p[0]):
            directory.increaseFunctionCallCounter()
            directory.initArgumentCounter()
            directory.setNewScope(p[0])

            funcType = directory.getFunctionType(p[0])
            quadruples.pushTypeStack(funcType)

            adr = memory.addVar(funcType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), funcType, adr)
            quadruples.pushOperandStack(quadruples.temporalCounter())
            quadruples.increaseTempCount()

            quadruples.pushQuadruple("ERA","","",p[0])
        else:
            print("Error: function does not exist.")
        return p

    @_('expression addArgument "," argumentInput')
    def argumentInput(self, p):
        return p

    @_('expression addArgument ")" validateParamSize')
    def argumentInput(self, p):
        return p

    @_('')
    def addArgument(self, p):
        argOperand = quadruples.popOperandStack()
        argType = quadruples.popTypeStack()
        if directory.checkArgType(argType):
            quadruples.pushQuadruple("ARGUMENT",
                                     directory.getAddress(argOperand, argType),
                                     "",
                                     "arg" + str(directory.getArgumentCounter()))
        directory.increaseArgumentCounter()
        return p

    @_('')
    def noArgs(self, p):
        quadruples.pushQuadruple("NOARGS","","","")
        return p

    @_('')
    def validateParamSize(self, p):
        if directory.checkParamArgumentLength():
            returnOperand = quadruples.popOperandStack()
            returnType = quadruples.popTypeStack()
            quadruples.pushQuadruple("GOSUB", directory.currentScope, "", directory.getFunctionStartNumber())
            quadruples.pushQuadruple('RETURNVALUE', "", "", directory.getAddress(returnOperand,returnType))
            quadruples.pushOperandStack(returnOperand)
            quadruples.pushTypeStack(returnType)

            directory.popArgumentCounter()
            directory.popScopeStack()
            directory.decreaseFunctionCallCounter()
        else:
            print("Error: number of arguments and parameters don't match")
        return p

    @_('ID')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack(directory.getVariableType(p[0]))
        return p

    @_('arrayId pushFakeBottom arrayIndexes popFakeBottom saveArrIdx')
    def varcte(self, p):
        if directory.getArrayDimensions(directory.auxArrId[-1]) != len(directory.arrIndexes[-1]):
            print("Error: incorrect indexing")
            exit()

        baseAdr = directory.getArrayBaseDir()

        adr = memory.addVar(directory.auxArrType[-1], 'temp')
        directory.addTemp(quadruples.temporalCounter(), directory.auxArrType[-1], adr)
        quadruples.pushQuadruple('ARRIDX', baseAdr, "", adr)
        quadruples.pushOperandStack(quadruples.temporalCounter())
        quadruples.pushTypeStack(directory.auxArrType[-1])
        quadruples.increaseTempCount()

        directory.arrIndexes.pop()
        directory.auxArrId.pop()
        directory.auxArrType.pop()
        return p

    @_('CTEINT')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack("int")
        if not directory.isConst(p[0], 'int'):
            directory.addConst(p[0], 'int', memory.addVar('int','const'))
        return p

    @_('CTEFLOAT')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack("float")
        if not directory.isConst(p[0], 'float'):
            directory.addConst(p[0], 'float', memory.addVar('float', 'const'))
        return p

    @_('CTECHAR')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack("char")
        if not directory.isConst(p[0], 'char'):
            directory.addConst(p[0], 'char', memory.addVar('char', 'const'))
        return p

    @_('CTESTRING')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack("string")
        if not directory.isConst(p[0], 'string'):
            directory.addConst(p[0], 'string', memory.addVar('string', 'const'))
        return p

    @_('decision block')
    def condition(self, p):
        end = quadruples.popJumpStack()
        cont = quadruples.quadCount()
        quadruples.fill(end, cont)
        return p

    @_('decision block writeElseQuad ELSE block')
    def condition(self, p):
        end = quadruples.popJumpStack()
        cont = quadruples.quadCount()
        quadruples.fill(end, cont)
        return p

    @_('decision block writeElseQuad ELSE condition')
    def condition(self, p):
        end = quadruples.popJumpStack()
        cont = quadruples.quadCount()
        quadruples.fill(end, cont)
        return p

    @_('IF "(" expression ")"')
    def decision(self, p):
        type = quadruples.popTypeStack()
        if type != "bool":
            print("Conditional statements must be boolean")
            exit()
        else:
            exp = quadruples.popOperandStack()
            quadruples.pushQuadruple("GOTOF", directory.getAddress(exp, type), "", "")
            curQuad = quadruples.quadCount()
            quadruples.pushJumpStack(curQuad - 1)
        return p

    @_('')
    def writeElseQuad(self, p):
        quadruples.pushQuadruple("GOTO", "", "", "_")
        false = quadruples.popJumpStack()
        cont = quadruples.quadCount()
        quadruples.pushJumpStack(cont - 1)
        quadruples.fill(false, cont)
        return p

    @_('WHILE whilePushJump "(" expression ")" checkWhileExp block fillWhileGoto')
    def whileStatement(self, p):
        return p

    @_('DO whilePushJump block WHILE "(" expression ")" checkWhileExp fillWhileGoto')
    def whileStatement(self, p):
        return p

    @_('')
    def whilePushJump(self, p):
        quadruples.pushJumpStack(quadruples.quadCount())
        return p

    @_('')
    def checkWhileExp(self, p):
        expressionType = quadruples.popTypeStack()
        if expressionType == "bool":
            result = quadruples.popOperandStack()
            quadruples.pushQuadruple("GOTOF", directory.getAddress(result, expressionType), "", "")
            quadruples.pushJumpStack(quadruples.quadCount() - 1)
        else:
            print("Error: while conditional must be boolean")
            exit()
        return p

    @_('')
    def fillWhileGoto(self, p):
        end = quadruples.popJumpStack()
        ret = quadruples.popJumpStack()
        quadruples.pushQuadruple("GOTO", '', '', ret)
        quadruples.fill(end, quadruples.quadCount())
        return p

    @_('FOR "(" type declareIdx "=" exp assignIdx ";" expression forCondition ";" step ")" block loopFor')
    def forStatement(self, p):
        directory.removeVariableToContext(p[3][1])
        return p

    @_('ID')
    def declareIdx(self, p):
        type = directory.getCurrentType()
        if type == 'int' or type == 'float':
            directory.addVariableToContext(p[0],
                                           memory.addVar(directory.getCurrentType(), directory.getScope()))
            quadruples.pushOperandStack(p[0])
            quadruples.pushTypeStack(type)
        else:
            print("Error: can only iterate int or floats")
            exit()
        return p

    @_('')
    def assignIdx(self, p):
        expType = quadruples.popTypeStack()
        if expType == 'int' or expType == 'float':
            expOperand = quadruples.popOperandStack()
            vControl = quadruples.topOperandStack()
            adr = memory.addVar(quadruples.topTypeStack(), 'temp')

            directory.addTemp(quadruples.temporalCounter(), quadruples.topTypeStack(), adr)
            quadruples.increaseTempCount()
            quadruples.pushControlStack(adr)
            if quadruples.verifyOperatorValidity('=', (expType, quadruples.topTypeStack())):
                quadruples.pushQuadruple('=',
                                         directory.getAddress(expOperand, expType),'',
                                         directory.getAddress(vControl, quadruples.topTypeStack()))
                quadruples.pushQuadruple('=',
                                         directory.getAddress(expOperand, expType), '', adr)
                quadruples.pushJumpStack(quadruples.quadCount())
            else:
                print("Error: Type mismatch")
                exit()
        return p

    @_('')
    def forCondition(self, p):
        expType = quadruples.popTypeStack()
        if expType == "bool":
            result = quadruples.popOperandStack()
            quadruples.pushQuadruple("GOTOF", directory.getAddress(result, expType), "", "")
            quadruples.pushJumpStack(quadruples.quadCount() - 1)
        else:
            print("Error: for conditional must be boolean")
            exit()
        return p

    @_('exp')
    def step(self, p):

        stepOperand = quadruples.popOperandStack()
        stepType = quadruples.popTypeStack()

        if stepType == 'int' or stepType == 'float':
            vControl = quadruples.popControlStack()
            adrBool = memory.addVar(stepType, 'temp')
            directory.addTemp(quadruples.temporalCounter(), stepType, adrBool)
            quadruples.increaseTempCount()
            quadruples.pushQuadruple('=', adrBool, '', vControl)
            quadruples.pushQuadruple('=', adrBool, '',
                                     directory.getAddress(quadruples.popOperandStack(),
                                                          quadruples.popTypeStack()))
            quadruples.pushQuadruple('+', vControl, directory.getAddress(stepOperand, stepType), adrBool)
        else:
            print("Error: for step value must be int or float")
            exit()
        return p

    @_('')
    def loopFor(self, p):
        end = quadruples.popJumpStack()
        ret = quadruples.popJumpStack()
        quadruples.pushQuadruple('GOTO', '', '', ret)
        quadruples.fill(end, quadruples.quadCount())
        return p

    @_('')
    def eof(self, p):
        #print("Valid")
        #directory.printDirectory()
        print(quadruples.printQuadrupleList())
        return p