# Division by 0 code snippet generator
import random
import string

dataTypes = ['int', 'unsigned int', 'short int', 'short', 'unsigned short int', 'unsigned short', 'long', 'unsigned long', 'long long', 'unsigned long long', 'char', 'unsigned char']
dataTypesFloat = ['float', 'double', 'long double']
allDataTypes = dataTypes + dataTypesFloat
indents = [' ', '  ', '    ', "\t"]

#Generating random VALID c++ identifier
def generateName():
    name = random.choice(string.letters)
    nameLen = range(random.randint(3, 9))
    for i in nameLen:
        choice = random.randint(0, 19)
        if choice < 13:
            name = name + random.choice(string.letters)
        elif choice < 19:
            name = name + random.choice('0123456789')
        else:
            name = name + '_'
    return name

#Generating variable declaration and initialization
def generateSingleVariable(value, inlineSet = True):
    if value == 0:
        varType = random.choice(dataTypes)
    else:
        varType = random.choice(allDataTypes)
    varName = generateName()
    indent = random.choice(indents)
    lines = []
    if inlineSet:
        lines.append(''.join([indent,varType,indent,varName,indent,'=',indent,str(value),';']))
    else:
        lines.append(''.join([indent,varType,indent,varName,';']))
        lines.append(''.join([indent,varName,indent,'=',indent,str(value),';']))
    return (varName, lines, value, varType)

def generateManyVariables(noOfVars, values, inlineSet = True):
    if 0 in values:
        varType = random.choice(dataTypes)
    else:
        varType = random.choice(allDataTypes)
    varDecls = []
    varNames = []
    lines = []
    indent = random.choice(indents)
    for i in range(noOfVars):
        varName = generateName()
        if inlineSet:
            varDecls.append(''.join([indent,varName,indent,'=',indent,str(values[i])]))
        else:
            varDecls.append(''.join([indent,varName]))
            lines.append(''.join([indent,varName,indent,'=',indent,str(values[i]),';']))
        varNames.append(varName)
    lines.insert(0, ''.join([indent,varType,','.join(varDecls),';']))
    return (varNames, lines, values, varType)

def generateManyVariablesSingleValue(noOfVars, value):
    if value == 0:
        varType = random.choice(dataTypes)
    else:
        varType = random.choice(allDataTypes)
    varDecls = []
    varDefs = []
    varNames = []
    varValues = [value]*noOfVars
    indent = random.choice(indents)
    for i in range(noOfVars):
        varName = generateName()
        varDecls.append(''.join([indent,varName]))
        varDefs.append(''.join([indent,varName,indent,'=']))
        varNames.append(varName)
    lines = [''.join([indent,varType,','.join(varDecls),';'])]
    lines.append(''.join([indent,''.join(varDefs),indent,str(value),';']))
    return (varNames, lines, varValues, varType)

def generateDefine(value):
    varName = generateName()
    indent = random.choice(indents)
    lines = [''.join(['#define', indent, varName, indent, '(',str(value),')'])]
    return (varName, lines, value)

#Generating dummy function
def generateFunction(noOfParams, returnValue):
    varType = random.choice(dataTypes)
    varName = generateName()
    indent = random.choice(indents)
    parameters = []
    lines = []
    for i in range(noOfParams):
        paramType = random.choice(dataTypes)
        paramName = generateName()
        parameters.append(''.join([paramType,indent,paramName]))
    javaStyleBrackets = random.choice([True, False])
    if javaStyleBrackets:
        lines.append(''.join([varType,indent,varName,'(',','.join(parameters),')',indent,'{']))
    else:
        lines.append(''.join([varType,indent,varName,'(',','.join(parameters),')']))
        lines.append('{')
    lines.append(''.join([indent,'return',indent,str(returnValue),';']))
    lines.append('}')
    declaration = ''.join([varType,indent,varName,'(',','.join(parameters),');'])
    return (varName, lines, noOfParams, returnValue, declaration)

def randNonZero():
    value = random.randint(-2147483647, 2147483647)
    if value == 0:
        value = -2147483648
    return value

def randWithZero():
    value = random.randint(-2147483648, 2147483647)
    return value

def randGreaterThanZero():
    value = random.randint(1, 2147483647)
    return value

def generateValidCondition(variables, defines, functions, useStd, nestLevel = 2):
    bools = [True, False]
    if random.randint(1, 10) < 8 or nestLevel < 1:
        # Single condition
        conditionType = random.randint(0, 7)
        conditions = ['<', '<=', '>', '>=', '==', '!=', '&']
        if conditionType < 7:
            if conditionType < 6:
                filteredVars = variables
            else:
                filteredVars = filter(lambda x: x[2] not in dataTypesFloat, variables)
            v2Type = random.randint(1, 3)
            v1 = random.choice(filteredVars)
            if v2Type == 1 and len(defines) > 0:
                d = random.choice(defines)
                v2 = [d[0], d[2]]
            elif v2Type == 2 and len(filteredVars) > 1:
                v2 = random.choice(filteredVars)
                while v1[0] == v2[0]:
                    v2 = random.choice(filteredVars)
            else:
                d = randWithZero()
                v2 = [d, d]
            return '{0} {1} {2}'.format(v1[0], conditions[conditionType], v2[0])
        else:
            v1 = random.choice(variables)
            return '{0}'.format(v1[0])
    else:
        # Nested condition
        if random.choice(bools):
            return '({0}) && ({1})'.format(generateValidCondition(variables, defines, functions, useStd, nestLevel - 1), generateValidCondition(variables, defines, functions, useStd, nestLevel - 1))
        else:
            return '({0}) || ({1})'.format(generateValidCondition(variables, defines, functions, useStd, nestLevel - 1), generateValidCondition(variables, defines, functions, useStd, nestLevel - 1))
    return ''

def generateArithmeticStatement(variables, defines, functions, useStd):
    operations = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>']
    opType = random.randint(0, 22)
    bools = [True, False]
    varsNonFloat = filter(lambda x: x[2] not in dataTypesFloat and x[1] != 0, variables)
    if opType < 10:
        v0 = random.choice(filter(lambda x: x[1] != 0, variables))
        v1Type = random.randint(1, 10)
        if v1Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v1 = [d[0], d[2]]
        elif v1Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v1 = ['{0}({1})'.format(f[0], params), f[3]]
        else:
            v1 = random.choice(variables)
            if v1[2] in dataTypesFloat and opType > 3:
                if len(varsNonFloat) > 0:
                    v1 = random.choice(varsNonFloat)
                else:
                    opType = random.randint(1, 3)
        if opType < 4:
            filteredVars = variables
        else:
            filteredVars = filter(lambda x: x[0] != v0[0] and x[0] != v1[0], varsNonFloat)
        if random.choice(bools) and len(filteredVars) > 0:
            v2 = random.choice(filteredVars)
        else:
            v2 = [randGreaterThanZero()] * 2
        return '{0} = {1} {2} {3};'.format(v0[0], v1[0], operations[opType], v2[0])
    elif opType < 20:
        v0 = random.choice(filter(lambda x: x[1] != 0, variables))
        if v0[2] in dataTypesFloat and opType > 13:
                if len(varsNonFloat) > 0:
                    v0 = random.choice(varsNonFloat)
                else:
                    opType = random.randint(11, 13)
        if opType < 14:
            filteredVars = variables
        else:
            filteredVars = filter(lambda x: x[0] != v0[0], varsNonFloat)
        if random.choice(bools) and len(filteredVars) > 0:
            v2 = random.choice(filteredVars)
        else:
            v2 = [randGreaterThanZero()] * 2
        return '{0} {1}= {2};'.format(v0[0], operations[opType - 10], v2[0])
    elif opType < 22 and len(varsNonFloat) > 0:
        v0 = random.choice(varsNonFloat)
        ops = ['++', '--']
        return '{0}{1};'.format(v0[0], ops[opType - 20])
    else:
        v0 = random.choice(filter(lambda x: x[1] != 0, variables))
        v1Type = random.randint(1, 10)
        if v1Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v1 = [d[0], d[2]]
        elif v1Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v1 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v1Type < 6:
            v1 = [randNonZero()] * 2
        else:
            v1 = random.choice(variables)
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        return '{0} = ({1}) ? {2} : {3};'.format(v0[0], generateValidCondition(variables, defines, functions, useStd, 0), v1[0], v2[0])

def generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel = 3):
    value = random.randint(0, 12)
    bools = [True, False]
    if (nestLevel < 1):
        value = random.randint(-1, 1)
    lines = []
    if value == 0 and len(functions) > 0:
        # Usage of function
        f = random.choice(functions)
        random.shuffle(variables)
        paramsArray = []
        for i in range(f[2]):
            if random.choice(bools) and len(variables) > i:
                paramsArray.append(variables[i][0])
            else:
                paramsArray.append(str(randWithZero()))
        params = ', '.join(paramsArray)
        for v in variables:
            if v[1] != 0 and f[3] != 0:
                lines.append('{0} = {1}({2});'.format(v[0], f[0], params))
                break
            elif v[1] == 0 and f[3] == 0:
                lines.append('{0} = {1}({2});'.format(v[0], f[0], params))
                break
    elif value == 1:
        # Usage of stdlib function
        stdLibs = ['abs', 'ceil', 'floor']
        fun = random.choice(stdLibs)
        if fun == 'abs':
            filteredVariables = filter(lambda x: 'unsigned' not in x[2], variables)
        elif fun in ['ceil', 'floor']:
            filteredVariables = filter(lambda x: x[2] in dataTypesFloat, variables)
        else:
            filteredVariables = variables
        if len(filteredVariables) >= 2:
            v1 = random.choice(filteredVariables)
            v2 = random.choice(filteredVariables)
            while v1[0] == v2[0]:
                v2 = random.choice(filteredVariables)
            parts = ['{0} = (int){1}({2})'.format(v1[0], fun, v2[0])]
            if v1[1] == 0 and v2[1] != 0:
                parts.append(' * 0')
            elif v1[1] != 0 and v2[1] == 0:
                parts.append(' + ({0})'.format(randNonZero()))
            parts.append(';')
            lines.append(''.join(parts))
        else:
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel))
    elif value == 2:
        # Conditional instruction - only if
        lines.append("if ({0})".format(generateValidCondition(variables, defines, functions, useStd)))
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
    elif value == 3:
        # Conditional instruction - if ... else
        lines.append("if ({0})".format(generateValidCondition(variables, defines, functions, useStd)))
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
        lines.append("else")
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
    elif value == 4:
        # Conditional instruction if ... elseif (one or more) ... else
        lines.append("if ({0})".format(generateValidCondition(variables, defines, functions, useStd)))
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
        noOfElseIfs = random.randint(1, 5)
        for i in range(noOfElseIfs):
            lines.append("else if ({0})".format(generateValidCondition(variables, defines, functions, useStd)))
            lines.append("{")
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
            lines.append("}")
        lines.append("else")
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
    elif value == 5:
        # For loop
        noOfExecutions = random.randint(1, 10)
        for v in variables:
            if v[1] < 11 and v[1] > 0 and v[2] not in dataTypesFloat:
                noOfExecutions = v[0]
                break
        varNames = ['l', 'k', 'j', 'i']
        varName = varNames[nestLevel]
        if random.choice(bools):
            # Use postincrement
            if random.choice(bools):
                # Use ++
                lines.append("for (int {0} = 0; {0} < {1}; {0}++)".format(varName, noOfExecutions))
            else:
                # Use --
                lines.append("for (int {0} = {1}; {0} >= 0; {0}--)".format(varName, noOfExecutions))
        else:
            # Use preincrement
            if random.choice(bools):
                # Use ++
                lines.append("for (int {0} = 0; {0} < {1}; ++{0})".format(varName, noOfExecutions))
            else:
                # Use --
                lines.append("for (int {0} = {1}; {0} >= 0; --{0})".format(varName, noOfExecutions))
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
    elif value == 6:
        # While loop
        noOfExecutions = random.randint(1, 10)
        for v in variables:
            if v[1] < 11 and v[1] > 0 and v[2] not in dataTypesFloat:
                noOfExecutions = v[0]
                break
        varNames = ['l', 'k', 'j', 'i']
        varName = varNames[nestLevel]
        countUp = random.choice(bools)
        firstIncrement = random.choice(bools)
        lines.append("{")
        if countUp:
            lines.append('int {0} = 0;'.format(varName))
            lines.append("while ({0} < {1})".format(varName, noOfExecutions))
        else:
            lines.append('int {0} = {1};'.format(varName, noOfExecutions))
            lines.append("while ({0} >= 0)".format(varName))
        lines.append("{")
        if not firstIncrement:
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        if countUp:
            if random.choice(bools):
                lines.append('{0}++;'.format(varName))
            else:
                lines.append('++{0};'.format(varName))
        else:
            if random.choice(bools):
                lines.append('{0}--;'.format(varName))
            else:
                lines.append('--{0};'.format(varName))
        if firstIncrement:
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
        lines.append("}")
    elif value == 7:
        # Do ... while loop
        noOfExecutions = random.randint(1, 10)
        for v in variables:
            if v[1] < 11 and v[1] > 0 and v[2] not in dataTypesFloat:
                noOfExecutions = v[0]
                break
        varNames = ['l', 'k', 'j', 'i']
        varName = varNames[nestLevel]
        countUp = random.choice(bools)
        lines.append("{")
        firstIncrement = random.choice(bools)
        if countUp:
            lines.append('int {0} = 0;'.format(varName))
        else:
            lines.append('int {0} = {1};'.format(varName, noOfExecutions))
        lines.append('do')
        lines.append("{")
        if not firstIncrement:
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        if countUp:
            if random.choice(bools):
                lines.append('{0}++;'.format(varName))
            else:
                lines.append('++{0};'.format(varName))
        else:
            if random.choice(bools):
                lines.append('{0}--;'.format(varName))
            else:
                lines.append('--{0};'.format(varName))
        if firstIncrement:
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
        if countUp:
            lines.append("while ({0} < {1});".format(varName, noOfExecutions))
        else:
            lines.append("while ({0} >= 0);".format(varName))
        lines.append("}")
    elif value == 8:
        # Try ... catch
        lines.append("try")
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, nestLevel - 1))
        lines.append("}")
        lines.append("catch (int& errorCode)")
        lines.append("{")
        lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, 0))
        lines.append("}")
    elif value == 9:
        # Print
        noOfPrints = random.randint(1, 5)
        parts = []
        if useStd:
            parts.append('std::')
        parts.append('cout')
        for i in range(noOfPrints):
            printType = random.randint(1, 3)
            if printType == 1 and len(functions) > 0:
                f = random.choice(functions)
                paramsArray = []
                for j in range(f[2]):
                    if random.choice(bools) and len(variables) > j:
                        paramsArray.append(variables[j][0])
                    else:
                        paramsArray.append(str(randWithZero()))
                params = ', '.join(paramsArray)
                parts.append(" << {0}({1})".format(f[0], params))
            elif printType == 2:
                parts.append(' << "{0}"'.format(generateName()))
            else:
                v = random.choice(variables)
                parts.append(" << {0}".format(v[0]))
        parts.append(" << ")
        if useStd:
            parts.append('std::')
        parts.append("endl;")
        lines.append(''.join(parts))
    elif value == 10:
        # Assignment
        v1 = random.choice(variables)
        if random.choice(bools) and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        else:
            v2 = random.choice(variables)
            while v1[0] == v2[0]:
                v2 = random.choice(variables)
        parts = ['{0} = ({1})({2}'.format(v1[0], v1[2], v2[0])]
        if v1[1] == 0 and v2[1] != 0:
            if random.choice(bools) and len(defines) > 0:
                parts.append(' * ({0})'.format(random.choice(filter(lambda x: x[2] == 0, defines))[0]))
            else:
                parts.append(' * {0}'.format(v1[0]))
        elif v1[1] != 0 and v2[1] == 0:
            if random.choice(bools) and len(defines) > 1:
                parts.append(' + ({0})'.format(random.choice(filter(lambda x: x[2] != 0, defines))[0]))
            else:
                parts.append(' + ({0})'.format(randNonZero()))
        parts.append(');')
        lines.append(''.join(parts))
    elif value == 11:
        # Switch
        charSwitch = random.choice(bools)
        var = random.choice(filter(lambda x: x[2] not in dataTypesFloat, variables))
        lines.append("switch ({0})".format(var[0]))
        lines.append("{")
        noOfCases = random.randint(1, 10)
        useDefault = random.choice(bools)
        doubleCase = random.choice(bools) and charSwitch
        charsLow = ["'a'", "'b'", "'c'", "'d'", "'e'", "'f'", "'g'", "'h'", "'i'", "'j'"]
        charsHigh = ["'A'", "'B'", "'C'", "'D'", "'E'", "'F'", "'G'", "'H'", "'I'", "'J'"]
        for i in range(noOfCases):
            if charSwitch:
                lines.append('case {0}:'.format(charsLow[i]))
                if doubleCase:
                    lines.append('case {0}:'.format(charsHigh[i]))
            else:
                lines.append('case {0}:'.format(i))
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, 0))
            lines.append('break;')
        if useDefault:
            lines.append('default:')
            lines.append(generateDummyInstructionSet(variables, defines, functions, useStd, 0))
            lines.append('break;')
        lines.append("}")
    else:
        # Arithmetic operation
        lines.append(generateArithmeticStatement(variables, defines, functions, useStd))
    return '\r\n'.join(lines)

def generateInstructionWithBug(variables, defines, functions, useStd, useIf, useZeroReturningFunction):
    bugType = random.randint(1, 5)
    bools = [True, False]
    v0 = random.choice(filter(lambda x: x[1] != 0, variables))
    if bugType == 1 and useIf:
        # Bug preceded in if condition (if a = 0: b = 1/a)
        funcs = filter(lambda x: x[3] == 0, functions)
        if useZeroReturningFunction and len(funcs) > 0 and random.randint(1, 10) < 8:
            f = random.choice(funcs)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            var = '{0}({1})'.format(f[0], params)
        else:
            var = random.choice(filter(lambda x: x[1] == 0, variables))[0]
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        parts = []
        parts.append('if ({0} == 0)'.format(var))
        parts.append('{')
        parts.append('\t{0} = {1} / {2};'.format(v0[0], v2[0], var))
        parts.append('}')
        return "\r\n".join(parts)
    elif bugType == 2 and random.randint(1, 10) < 7:
        # Bug in printing cout << a << 1 / a
        funcs = filter(lambda x: x[3] == 0, functions)
        if useZeroReturningFunction and len(funcs) > 0 and random.randint(1, 10) < 8:
            f = random.choice(funcs)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            var = '{0}({1})'.format(f[0], params)
        else:
            var = random.choice(filter(lambda x: x[1] == 0, variables))[0]
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        std = ''
        if useStd:
            std = 'std::'
        return '{0}cout << {1} / {2} << {0}endl;'.format(std, v2[0], var)
    elif bugType == 3 and random.randint(1, 10) < 8:
        # Bug in if condition (if b / a == 1)
        funcs = filter(lambda x: x[3] == 0, functions)
        if useZeroReturningFunction and len(funcs) > 0 and random.randint(1, 10) < 8:
            f = random.choice(funcs)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            var = '{0}({1})'.format(f[0], params)
        else:
            var = random.choice(filter(lambda x: x[1] == 0, variables))[0]
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        std = ''
        if useStd:
            std = 'std::'
        parts = []
        opType = random.choice(['<', '<=', '>', '>=', '!=', '=='])
        parts.append('if (({0} / {1}) {2} {3})'.format(v2[0], var, opType, randWithZero()))
        parts.append('{')
        if random.choice(bools):
            parts.append(generateInstructionWithBug(variables, defines, functions, useStd, useIf, useZeroReturningFunction))
        else:
            parts.append(generateDummyInstructionSet(variables, defines, functions, useStd))
        parts.append('}')
        return "\r\n".join(parts)
    elif bugType == 4 and random.randint(1, 10) < 2:
        # Bug preceded in for (for i = 0: a = 1/i)
        funcs = filter(lambda x: x[3] == 0, functions)
        if useZeroReturningFunction and len(funcs) > 0 and random.randint(1, 10) < 8:
            f = random.choice(funcs)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            var = '{0}({1})'.format(f[0], params)
        else:
            var = random.choice(filter(lambda x: x[1] == 0, variables))[0]
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        parts = []
        if random.choice(bools):
            parts.append('for (int i = {1}; i < {0}; i++)'.format(random.randint(1, 200), var))
        else:
            parts.append('for (int i = 0; i < {0}; i++)'.format(random.randint(1, 200)))
        parts.append('{')
        if random.randint(1, 10) < 2:
            parts.append(generateInstructionWithBug(variables, defines, functions, useStd, useIf, useZeroReturningFunction))
        else:
            parts.append(generateDummyInstructionSet(variables, defines, functions, useStd))
        parts.append('\t{0} = {1} / i;'.format(v0[0], v2[0]))
        if random.randint(1, 10) < 2:
            parts.append(generateInstructionWithBug(variables, defines, functions, useStd, useIf, useZeroReturningFunction))
        else:
            parts.append(generateDummyInstructionSet(variables, defines, functions, useStd))
        parts.append('}')
        return "\r\n".join(parts)
    else:
        # Bug in normal operation a = 1/b
        funcs = filter(lambda x: x[3] == 0, functions)
        if useZeroReturningFunction and len(funcs) > 0 and random.randint(1, 10) < 8:
            f = random.choice(funcs)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            var = '{0}({1})'.format(f[0], params)
        else:
            var = random.choice(filter(lambda x: x[1] == 0, variables))[0]
        v2Type = random.randint(1, 10)
        if v2Type < 2 and len(defines) > 0:
            d = random.choice(defines)
            v2 = [d[0], d[2]]
        elif v2Type < 3 and len(functions) > 0:
            f = random.choice(functions)
            paramsArray = []
            for i in range(f[2]):
                if random.choice(bools) and len(variables) > i:
                    paramsArray.append(variables[i][0])
                else:
                    paramsArray.append(str(randWithZero()))
            params = ', '.join(paramsArray)
            v2 = ['{0}({1})'.format(f[0], params), f[3]]
        elif v2Type < 6:
            v2 = [randNonZero()] * 2
        else:
            v2 = random.choice(variables)
        return '{0} = {1} / {2};'.format(v0[0], v2[0], var)
    return ''

def main():
    bools = [True, False]
    configUseSeparateFunctionDefinitions = random.choice(bools)#
    configNoOfFunctions = random.randint(0, 5)#
    configUseIf = random.choice(bools)
    configUseZeroReturningFunction = random.choice(bools)
    configNoOfNonZeroVariables = random.randint(1, 100)#
    configNoOfZeroVariables = random.randint(1, 5)#
    configUseSeparateLineVariables = random.choice(bools)#
    configUseSeparateLineVariableInitialization = random.choice(bools)#
    configUseCommonVariableValue = random.randint(0, 9)#
    configUseNamespaceStd = random.choice(bools)#
    configUsingStd = random.choice(bools)#
    configUseStd = random.choice(bools)#
    configNoOfDummyInstructionsBeforeBug = random.randint(0, 20)#
    configNoOfDummyInstructionsAfterBug = random.randint(0, 20)#
    configUseDefines = random.choice(bools)#

    #Program structure - includes
    includes = ['iostream', 'cstdio', 'string', 'cmath', 'cstdint', 'cstdlib']
    random.shuffle(includes)
    for include in includes:
        print '#include <{0}>'.format(include)
    print ''

    #Program structure - defines
    defines = []
    noOfDefines = 0
    if configUseDefines:
        noOfDefines = random.randint(0, 5)
    for i in range(noOfDefines):
        if i == 0:
            returnValue = 0
        else:
            returnValue = randNonZero()
        defines.append(generateDefine(returnValue))
    random.shuffle(defines)

    for d in defines:
        print d[1][0]
    print ''

    #Program structure - using
    if configUseNamespaceStd:
        print 'using namespace std;'
    elif configUsingStd:
        print 'using std::cout;'
        print 'using std::endl;'
        print 'using std::abs;'
        print 'using std::ceil;'
        print 'using std::floor;'
    else:
        configUseStd = True
    print ''

    #Program structure - function declarations
    functions = []
    for i in range(configNoOfFunctions):
        if i == 0:
            returnValue = 0
        else:
            returnValue = randNonZero()
        functions.append(generateFunction(random.randint(0, 5), returnValue))
    
    random.shuffle(functions)
    if configUseSeparateFunctionDefinitions:
        for f in functions:
            print f[4]
            print ''
    else:
        for f in functions:
            print "\r\n".join(f[1])
            print ''
    
    #Program structure - main
    # Main declaration
    mainStyle = random.randint(0,2)
    javaStyleMain = random.choice(bools)
    if mainStyle == 0:
        if javaStyleMain:
            print 'int main(void) {'
        else:
            print 'int main(void)'
            print '{'
    elif mainStyle == 1:
        if javaStyleMain:
            print 'int main() {'
        else:
            print 'int main()'
            print '{'
    else:
        if javaStyleMain:
            print 'int main(int argc, char** argv) {'
        else:
            print 'int main(int argc, char** argv)'
            print '{'
    
    # Variables
    variables = []
    if configUseCommonVariableValue == 0:
        value = randNonZero()
        nonZeros = generateManyVariablesSingleValue(configNoOfNonZeroVariables, value)
        zeros = generateManyVariablesSingleValue(configNoOfZeroVariables, 0)
        for i in range(configNoOfNonZeroVariables):
            variables.append([nonZeros[0][i], nonZeros[2][i], nonZeros[3]])
        for i in range(configNoOfZeroVariables):
            variables.append([zeros[0][i], zeros[2][i], zeros[3]])
        if random.choice(bools):
            print "\r\n".join(nonZeros[1])
            print "\r\n".join(zeros[1])
        else:
            print "\r\n".join(zeros[1])
            print "\r\n".join(nonZeros[1])
    elif configUseSeparateLineVariables:
        lines = []
        for i in range(configNoOfNonZeroVariables):
            var = generateSingleVariable(randNonZero(), configUseSeparateLineVariableInitialization)
            variables.append([var[0], var[2], var[3]])
            lines.append("\r\n".join(var[1]))
        for i in range(configNoOfZeroVariables):
            var = generateSingleVariable(0, configUseSeparateLineVariableInitialization)
            variables.append([var[0], var[2], var[3]])
            lines.append("\r\n".join(var[1]))
        random.shuffle(lines)
        print "\r\n".join(lines)
    else:
        valuesNonZero = []
        valuesZero = [0] * configNoOfZeroVariables
        for i in range(configNoOfNonZeroVariables):
            valuesNonZero.append(randNonZero())
        nonZeros = generateManyVariables(configNoOfNonZeroVariables, valuesNonZero, configUseSeparateLineVariableInitialization)
        zeros = generateManyVariables(configNoOfZeroVariables, valuesZero, configUseSeparateLineVariableInitialization)
        for i in range(configNoOfNonZeroVariables):
            variables.append([nonZeros[0][i], nonZeros[2][i], nonZeros[3]])
        for i in range(configNoOfZeroVariables):
            variables.append([zeros[0][i], zeros[2][i], zeros[3]])
        if random.choice(bools):
            print "\r\n".join(nonZeros[1])
            print "\r\n".join(zeros[1])
        else:
            print "\r\n".join(zeros[1])
            print "\r\n".join(nonZeros[1])
    print ''

    # Instructions - before bug
    for i in range(configNoOfDummyInstructionsBeforeBug):
        print generateDummyInstructionSet(variables, defines, functions, configUseStd)
        if random.choice(bools):
            print ''
    
    # BUG
    print generateInstructionWithBug(variables, defines, functions, configUseStd, configUseIf, configUseZeroReturningFunction)
    if random.choice(bools):
        print ''

    # Instructions - after bug
    for i in range(configNoOfDummyInstructionsAfterBug):
        print generateDummyInstructionSet(variables, defines, functions, configUseStd)
        if random.choice(bools):
            print ''
    
    # Ending
    print 'return 0;'
    print '}'
    print ''

    # Function definitions
    if configUseSeparateFunctionDefinitions:
        for f in functions:
            print "\r\n".join(f[1])
            print ''

main()