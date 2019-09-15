import sys
from enum import Enum

class Direction(Enum):
    Left = 0
    Right = 1

class Rule:
    def __init__(self, startState, curSymb, nextSymb, direction, endState):
        self.startState = startState
        self.curSymb = curSymb
        self.nextSymb = nextSymb
        self.direction = direction
        self.endState = endState

class Production:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def getString(self):
        return self.head + ' -> ' + self.tail + '\n'

def main(argv):
    if len(argv) < 3:
        print('Expected input: <input_turing_machine_file> <output_unrestricted_grammar_file>')
        return

    inputFilePath = argv[1]
    outputFilePath = argv[2]

    print('Reading file: ' + inputFilePath)

    with open(inputFilePath) as f:
        lines = f.readlines()

    lines = [x.strip() for x in lines]

    # ignore comments and empty
    lines = [x for x in lines 
             if not (x.startswith(';') or x.startswith('//'))
             and len(x) != 0]

    # let initial state be '0'
    initialState = '0'
    # all final state names must start with 'halt'
    finalStatePrefix = 'halt'

    blank = '_'
    leftSymb = 'l'
    rightSymb = 'r'

    # tape symbols, this set always has blank
    symbols = set(blank)

    # alphabet, must be an subset of tape symbols
    alphabet = set('I')

    alphabetWithEps = alphabet.copy()
    alphabetWithEps.add('')

    states = set()
    finalStates = set()
    rules = []

    print('Parsing turing machine rules...\n')

    for line in lines:
        delta = line.split(' ')

        dir = Direction.Right if delta[3] == rightSymb else Direction.Left

        rule = Rule(delta[0], delta[1], delta[2], dir, delta[4])
        rules.append(rule)

        # add any symbol to tape symbols
        symbols.add(rule.curSymb)
        symbols.add(rule.nextSymb)
        
        # add states
        states.add(rule.startState)
        states.add(rule.endState)

        # check if final state
        if rule.endState.startswith(finalStatePrefix):
            finalStates.add(rule.endState)

    print('TM alphabet: ' + str(alphabet))
    print('TM blank symbol is \'' + blank + '\'')
    print('TM line symbols: ' + str(symbols) + '\n')
    print('TM states amount: ' + str(len(states)))
    print('TM initial state is \'' + initialState + '\'')
    print('TM final states: ' + str(finalStates) + '\n')
    print('TM rules amount: ' + str(len(rules)) + '\n')
    
    print('Creating unrestricted grammar productions...')

    # create grammar
    productions = []

    # 1
    productions.append(
        Production('A1', initialState + ' ' + 'A2'))

    # 2
    productions += [
        Production('A2', '({},{}) A2'.format(a, a))
        for a in alphabet]

    # 3
    productions.append(
        Production('A2', 'A3'))

    # 4
    productions.append(
        Production('A3', '(,{}) A3'.format(blank)))
    
    # 5
    productions.append(
        Production('A3', ''))

    # 6, 7
    for rule in rules:

        q = rule.startState
        A = rule.curSymb
        p = rule.endState
        M = rule.nextSymb

        if rule.direction == Direction.Right:
            productions += [
                Production('{} ({},{})'.format(q, a, A), 
                           '({},{}) {}'.format(a, M, p))
                for a in alphabetWithEps]
        else:
            productions += [
                Production('({},{}) {} ({},{})'.format(b,C,q,a,A), 
                           '{} ({},{}) ({},{})'.format(p,b,C,a,M))
                for a in alphabetWithEps
                for b in alphabetWithEps
                for C in symbols]

            
    # 8, 9
    for a in alphabetWithEps:
        for C in symbols:
            for q in finalStates:
                head8 = '({},{}) {}'.format(a, C, q)
                head9 = '{} ({},{})'.format(q, a, C)
                tail = '{} {} {}'.format(q, a, q)

                productions.append(
                    Production(head8, tail))
                productions.append(
                    Production(head9, tail))

    # 10
    productions += [
        Production(q, '')
        for q in finalStates]

    print('UG productions amount: ' + str(len(productions)) + '\n')

    plines = [p.getString() for p in productions]

    print('Writing to file: ' + outputFilePath)

    with open(outputFilePath, 'w') as f:
        f.writelines(plines)

# call main method
main(sys.argv)