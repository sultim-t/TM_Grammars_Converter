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
        print('Expected input: <input_turing_machine_file> <output_cs_grammar_file>')
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
    
    print('Creating context sensitive grammar productions...')

    


# call main method
main(sys.argv)