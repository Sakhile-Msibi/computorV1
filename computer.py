import re
import sys

def equationValidation(equation):
    equationRegex = re.compile('[0-9X\s\^\-\+\*\=\.\/]+$')
    equationValue1 = re.search('(?<=[^X])\^', equation)
    equationValue2 = re.search('\^(?![0-9])', equation)
    equationValue3 = re.search('(?<=\d)\s(?=\d)', equation)

    if not equationRegex.match(equation):
        print('There are wrong characters in the equation')
        return False
    if equationValue1 is not None or equationValue2 is not None or equationValue3 is not None:
        print('polynomial is not well formatted')
        return False
    return True

def equationConstruction(variable, sign):
    result = dict()
    errormsg = 'There is an error in the construction of the equation'
    splitVariable = variable.split('X')

    if len(splitVariable) > 2 or len(splitVariable) == 0:
        print('There is an error in the polynomial')
        exit(1)

    if len(splitVariable) == 2:
        splitVariable[0] = '1*' if splitVariable[0] == '' else splitVariable[0]
        splitVariable[1] = '^1' if splitVariable[1] == '' else splitVariable[1]
        if splitVariable[0][-1] != '*' or splitVariable[1][0] != '^':
            print(errormsg)
            exit(1)
        else:
            try:
                result['denominator'] = float(splitVariable[0][:-1]) if sign == '+' else -1 * float(splitVariable[0][:-1])
                pol = float(splitVariable[1][1:]) if splitVariable[1][1:] != '' else 1
                if not (pol).is_integer():
                    print('The application does not take float as exponents')
                    exit(1)
                result['polynomial'] = int(pol)
            except:
                print(errormsg)
                exit(1)
    else:
        try:
            result['denominator'] = float(splitVariable[0]) if sign == '+' else -1 * float(splitVariable[0])
            result['polynomial'] = 0
        except:
            print(errormsg)
            exit(1)
    return result

def reducedEquation(equation):
    reducedEqn = ''
    exponent = 0
    sign = False
    exponentList = sorted(list(equation.keys()))

    for value in exponentList:
        if int(value) > exponent:
            exponent = int(value)
        if equation[value] != 0:
            coefficient = int(equation[value]) if equation[value] % int(equation[value]) == 0 else equation[value] #The if/else statement caters for coefficients that are fractions
            #caters for coefficients that are negative
            if equation[value] < 0:
                reducedEqn += ' - ' if sign else '-'
            elif sign:
                reducedEqn += ' + '
            if int(value) > 1:
                reducedEqn += str(abs(coefficient)) + ' * X^' + str(value) if coefficient != 1 else 'X^' + value
                sign = True
            elif int(value) == 1:
                reducedEqn += str(abs(coefficient)) + ' * X' if coefficient != 1 else 'X'
                sign = True
            else:
                reducedEqn += str(abs(coefficient))
                sign = True
    if len(reducedEqn) > 0:
        print('Reduced form: ' + reducedEqn + ' = 0')
    return exponent

def printSolution(result):
    degree2 = 'Polynomial degree: 2'

    if result['solution'] is None:
        print('All real numbers are the solution')
    elif result['solution'] == False:
        print('There are no solutions')
    else:
        if result['discriminant'] is None and result['degree'] == 1:
            print('Polynomial degree: 1')
            print('The solution is: \n{}'.format(result['solution1']))
        elif result['discriminant'] == 0 and result['degree'] == 2:
            print(degree2)
            print('Discriminant is zero, the solution is: \n{}'.format(result['solution1']))
        elif result['discriminant'] < 0 and result['degree'] == 2:
            print(degree2)
            print('Discriminant is strictly negative, the two solutions are: \n{}\n{}'.format(result['solution1'], result['solution2']))
        else:
            print(degree2)
            print('Discriminant is strictly positive, the two solutions are: \n{}\n{}'.format(result['solution1'], result['solution2']))

def computer(equation):
    result = {
        'solution': True,
        'solution2': None,
        'discriminant': None,
        'exponent': 0
    }

    if not equationValidation(equation):
        exit(1)

    equation = equation.replace(' ','')

    equalSign = equation.split('=')
    if len(equalSign) != 2:
        print('The number of equal sign is not one')
        exit(1)
    
    leftSide = re.split(r'([\+\-])', equalSign[0] if equalSign != '0' else ['+', '0'])
    rightSide = re.split(r'([\+\-])', equalSign[1] if equalSign != '0' else ['+', '0'])

    for side in [leftSide, rightSide]:
        if side[0] == '':
            side.remove(side[0])
        if side[0] != '-':
            side.insert(0, '+')
    
    if '' in leftSide or '' in rightSide:
        print('There is a negative number in the equation')
        exit(1)
    
    sign = '+'
    leftSideClean = list()
    rightSideClean = list()
    for side, newSide in zip([leftSide, rightSide], [leftSideClean, rightSideClean]):
        for i in side:
            if i in ['-', '+']:
                sign = i
            else:
                temp = equationConstruction(i, sign)
                newSide.append(temp)
    
    firstStepEquation = leftSideClean
    for variable in rightSideClean:
        variable['denominator'] *= -1
        firstStepEquation.append(variable)
    
    equationDict = dict()
    for variable in firstStepEquation:
        if 'denominator' in variable and 'polynomial' in variable:
            if str(variable['polynomial']) not in equationDict:
                equationDict[str(variable['polynomial'])] = variable['denominator']
            else:
                equationDict[str(variable['polynomial'])] += variable['denominator']
        
    result['exponent'] = reducedEquation(equationDict)
    if result['exponent'] > 2:
        print('Polynomial Degree : {}\nThe polynomial degree is stricly greater than 2, I can\'t solve.'.format(result['exponent']))
        result['solution'] = False
        return result

    if len(equationDict) < result['exponent'] + 1:
        for i in range(0, result['exponent'] + 1):
            if str(i) not in equationDict:
                equationDict[str(i)] = 0
    
    if '2' in equationDict and equationDict['2'] != 0:
        result['degree'] = 2
        discriminant = equationDict['1'] ** 2 - 4 * equationDict['0'] * equationDict['2']
        result['discriminant'] = discriminant
        if discriminant > 0:
            result['solution1'] = (-1 * equationDict['1'] - discriminant**(1 / 2)) / (2 * equationDict['2'])
            result['solution2'] = (-1 * equationDict['1'] + discriminant**(1 / 2)) / (2 * equationDict['2'])
        elif discriminant == 0:
            result['solution1'] = (-1 * equationDict['1']) / (2 * equationDict['2'])
        else:
            result['solution1'] = str((-1 * equationDict['1']) / (2 * equationDict['2'])) + ' + i * ' + \
                                  str(abs(discriminant**(1 / 2)) / (2 * equationDict['2']))
            result['solution2'] = str((-1 * equationDict['1']) / (2 * equationDict['2'])) + ' - i * ' + \
                                  str(abs(discriminant**(1 / 2)) / (2 * equationDict['2']))
    elif '1' in equationDict and equationDict['1'] != 0:
        result['degree'] = 1
        result['solution1'] = -1 * equationDict['0'] / equationDict['1']
    elif '0' in equationDict and equationDict['0'] != 0:
        result['solution'] = False
    else:
        result['solution'] = None
    printSolution(result)
    return result

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('please add an equation')
        exit(1)
    elif len(sys.argv) > 2:
        print("Equation should be one string")
        exit(1)
    else:
        _= computer(sys.argv[1])