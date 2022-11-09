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
    @_('globalVars MAIN setScopeToMain "(" ")" block eof')
    def programBody(self, p):
        return p

    # Don't declare variables nor functions and go to main function
    @_('MAIN setScopeToMain "(" ")" block eof')
    def programBody(self, p):
        return p

    # Sets scope to main
    @_('')
    def setScopeToMain(self, p):
        directory.setScope("main")
        quadruples.setMainGotoAddress()
        return p

    # Declare global variables like normal variables.
    @_('var')
    def globalVars(self, p):
        return p

    # Just declare functions.
    @_('declareFunctions')
    def globalVars(self, p):
        return p

    # Optionally declare functions after global variables.
    @_('var declareFunctions')
    def globalVars(self, p):
        return p

    # Variable declaration
    @_('initScopeTable typeDeclaration')
    def var(self, p):
        return p

    # Checks if there's a table for the current scope
    # If not, create one.
    @_('')
    def initScopeTable(self, p):
        directory.checkTableCurrentScope()
        return p

    # Declare a single id
    @_('type addVarToContext ";"')
    def typeDeclaration(self, p):
        return p

    # Declare multiple ids of a single type
    @_('type addVarToContext "," multiVar')
    def typeDeclaration(self, p):
        return p

    # Single id of one type, begin declaring ids of another type
    @_('type addVarToContext ";" typeDeclaration')
    def typeDeclaration(self, p):
        return p

    # End same type declaration loop
    @_('addVarToContext ";"')
    def multiVar(self, p):
        return p

    # Same type declaration loop
    @_('addVarToContext "," multiVar')
    def multiVar(self, p):
        return p

    # End same type declaration loop
    # and begin declaring another type
    @_('addVarToContext ";" typeDeclaration')
    def multiVar(self, p):
        return p

    @_('ID')
    def addVarToContext(self, p):
        directory.addVariableToContext(p[0],
                                       memory.addVar(directory.getCurrentType(), directory.getScope()))
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
        # Set scope
        # Set return type
        # Add func to directory
        return p

    # Function with parameters
    @_('"(" param ")" countparam block endFunc')
    def parameterDeclaration(self, p):
        # Set scope
        # Set return type
        # Add func to directory
        return p

    # No parameter function
    @_('"(" ")" countparam block endFunc')
    def parameterDeclaration(self, p):
        return p

    # Count parameters
    @_('')
    def countparam(self, p):
        return p

    @_('paramDeclaration "," param')
    def param(self, p):
        return p

    @_('paramDeclaration')
    def param(self, p):
        return p

    @_('type ID')
    def paramDeclaration(self, p):
        # Add params to scope
        return p

    # End function
    @_('')
    def endFunc(self, p):
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

    @_('RETURN expression ";"')
    def returnStatement(self, p):
        return p

    @_('exp')
    def expression(self, p):
        return p

    @_('exp ">" exp')
    def expression(self, p):
        return p

    @_('exp "<" exp')
    def expression(self, p):
        return p

    @_('')
    def binaryOp1(self, p):
        print(quadruples.operatorStack)
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
                quadruples.pushTempStack(quadruples.resultCounter())
                adr = memory.addVar(resultType,'temp')
                directory.addTemp(quadruples.resultCounter(), resultType, adr)
                # Create new quadruple with operation
                quadruples.pushQuadruple(operator,
                                         directory.getAddress(leftOperand,leftType),
                                         directory.getAddress(rightOperand,rightType),
                                         adr)
                # Push temp to operands/type stacks
                quadruples.pushOperandStack(quadruples.resultCounter())
                quadruples.pushTypeStack(resultType)
                # Increase temporal index variable
                quadruples.resultAdd()
            else:
                print("Error: Operand types not compatible")
        return p

    @_('')
    def binaryOp2(self, p):
        print(quadruples.operatorStack)
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
                quadruples.pushTempStack(quadruples.resultCounter())
                adr = memory.addVar(resultType, 'temp')
                directory.addTemp(quadruples.resultCounter(), resultType, adr)
                # Create new quadruple with operation
                quadruples.pushQuadruple(operator,
                                         directory.getAddress(leftOperand, leftType),
                                         directory.getAddress(rightOperand, rightType),
                                         adr)
                # Push temp to operands/type stacks
                quadruples.pushOperandStack(quadruples.resultCounter())
                quadruples.pushTypeStack(resultType)
                # Increase temporal index variable
                quadruples.resultAdd()
            else:
                print("Error: Operand types not compatible")
        return p

    @_('functionCall')
    def exp(self, p):
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

    @_('ID "(" ")"')
    def functionCall(self, p):
        return p

    @_('ID "(" paramInput')
    def functionCall(self, p):
        return p

    @_('expression "," paramInput')
    def paramInput(self, p):
        return p

    @_('expression ")"')
    def paramInput(self, p):
        return p

    @_('ID')
    def varcte(self, p):
        quadruples.pushOperandStack(p[0])
        quadruples.pushTypeStack(directory.getVariableType(p[0]))
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
        return p

    @_('CTECHAR')
    def varcte(self, p):
        return p

    @_('CTESTRING')
    def varcte(self, p):
        return p

    @_('IF "(" expression ")" block')
    def condition(self, p):
        return p

    @_('IF "(" expression ")" block ELSE block')
    def condition(self, p):
        return p

    @_('')
    def eof(self, p):
        print("Valid")
        #print(quadruples.printQuadrupleList())
        return p