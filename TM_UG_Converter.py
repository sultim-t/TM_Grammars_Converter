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

    leftSymb = 'l'
    rightSymb = 'r'

    # tape symbols, this set always has blank
    symbols = set()

    # alphabet, must be an subset of tape symbols
    alphabet = {'1', '$', 'c'}

    alphabetWithEps = alphabet.copy()
    # epsilon is not used in current LBA
    #alphabetWithEps.add('')

    states = set()
    finalStates = set()
    rules = []

    leftSymbolForState = dict()

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

        if not rule.endState in leftSymbolForState:
            leftSymbolForState[rule.endState] = set()

        if rule.direction == Direction.Right:
            leftSymbolForState[rule.endState].add(rule.nextSymb)

        # check if final state
        if rule.endState.startswith(finalStatePrefix):
            finalStates.add(rule.endState)

    print('TM alphabet: ' + str(alphabet))

    print('TM line symbols: ' + str(symbols) + '\n')
    print('TM states amount: ' + str(len(states)))
    print('TM initial state is \'' + initialState + '\'')
    print('TM final states: ' + str(finalStates) + '\n')
    print('TM rules amount: ' + str(len(rules)) + '\n')
    
    print('Creating unrestricted grammar productions...')

    # create grammar
    productions = []

    # 1 - initial state
    productions.append(
        Production('A1', initialState + ' ' + 'A2'))

    # 2 - generate words
    productions += [
        Production('A2', '({},{}) A2'.format(a, a))
        for a in alphabet]

    # 3 - stop non-deterministic word generating
    productions.append(
        Production('A2', 'A3'))

    # 4 - add blanks
    # blanks are not used in current LBA
    #productions.append(
    #    Production('A3', '(,{}) A3'.format(blank)))
    
    # 5 - stop generating blanks
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
                for a in alphabetWithEps if (a != '$' and A != '$' and a != 'c' and A != 'c') or (a == '$' and A == '$') or (a == 'c' and A == 'c')]
                # can't be: '($,*)' where * is not '$'
                # can't be: '(c,*)' where * is not 'c'

        else:
            productions += [
                Production('({},{}) {} ({},{})'.format(b,C,q,a,A), 
                           '{} ({},{}) ({},{})'.format(p,b,C,a,M))
                for a in alphabetWithEps if (a != '$' and A != '$' and a != 'c' and A != 'c') or (a == '$' and A == '$') or (a == 'c' and A == 'c')
                for b in alphabetWithEps
                for C in symbols if ((b != '$' and C != '$' and b != 'c' and C != 'c') or (b == 'c' and C == 'c'))
                    and (C in leftSymbolForState[q] or len(leftSymbolForState[q]) == 0)
                    ]

            
    # 8, 9 - collapse
    for a in alphabetWithEps:
        for C in symbols:
            if (a != '$' and C != '$' and a != 'c' and C != 'c') or (a == '$' and C == '$') or (a == 'c' and C == 'c'):
                
                for q in finalStates:
                    head8 = '({},{}) {}'.format(a, C, q)
                    head9 = '{} ({},{})'.format(q, a, C)
                    tail = '{} {} {}'.format(q, a, q)

                    if a != '$':
                        productions.append(Production(head8, tail))

                    if a != 'c':
                        productions.append(Production(head9, tail))

    # 10
    productions += [
        Production(q, '')
        for q in finalStates]

    # optimization


    print('UG productions amount: ' + str(len(productions)) + '\n')

    plines = [p.getString() for p in productions]

    print('Writing to file: ' + outputFilePath)

    with open(outputFilePath, 'w') as f:
        f.writelines(plines)

# call main method
main(sys.argv)