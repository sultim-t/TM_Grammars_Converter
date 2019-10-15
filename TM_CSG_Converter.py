import sys
from enum import Enum

class Direction(Enum):
    Left = 0
    Right = 1

class Rule:
    def __init__(self, curState, curSymb, nextSymb, direction, nextState):
        self.curState = curState
        self.curSymb = curSymb
        self.nextSymb = nextSymb
        self.direction = direction
        self.nextState = nextState

class Production:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def getString(self):
        return self.head + ' -> ' + self.tail + '\n'

class Tree:
    def __init__(self, headNt):
        self.headNt = headNt
        self.productions = list()

    def findChildren(self, reviewedTrees, allProductions):
        subtreeNts = set()

        for p in allProductions:
            hs = p.head.split(' ')

            for h in hs:
                if self.headNt == h:
                    ts = set(p.tail.split(' '))
                    if self.headNt in ts:
                        ts.remove(self.headNt)
                    
                    if '1' in ts:
                        ts.remove('1')

                    # save all tail non-terminals
                    # that have 'headNt' as a head
                    subtreeNts = subtreeNts.union(ts)

                    # save production which
                    # contains 'headNt' of this tree
                    self.productions.append(p)

                    break

        # find children of all trees
        for subtreeNt in subtreeNts:

            if subtreeNt in reviewedTrees:
                continue

            reviewedTrees.add(subtreeNt)

            subtree = Tree(subtreeNt)
            subtree.findChildren(reviewedTrees, allProductions)


            self.productions += subtree.productions
    
def main(argv):

    if len(argv) < 3:
        print('Expected input: <input_turing_machine_file> <output_ncg_grammar_file>')
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
    q0 = '0'
    # all final state names must start with 'halt'
    finalStatePrefix = 'halt'

    leftSymb = 'l'
    rightSymb = 'r'

    lm = 'c'
    rm = '$'

    alphabet = {'1', rm, lm}
    alphabetWM = {'1'}
    
    gamma = set()
    gammaWM = set()

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
        
        # add states
        states.add(rule.curState)
        states.add(rule.nextState)

        gamma.add(rule.curSymb)
        gamma.add(rule.nextSymb)

        if not rule.nextState in leftSymbolForState:
            leftSymbolForState[rule.nextState] = set()

        if rule.direction == Direction.Right:
            leftSymbolForState[rule.nextState].add(rule.nextSymb)

        # check if final state
        if rule.nextState.startswith(finalStatePrefix):
            finalStates.add(rule.nextState)

    gammaWM = gamma.copy()
    gammaWM.remove(lm)
    gammaWM.remove(rm)

    print('TM alphabet: ' + str(alphabet))

    print('TM gamma: ' + str(gamma) + '\n')
    print('TM states amount: ' + str(len(states)))
    print('TM initial state is \'' + q0 + '\'')
    print('TM final states: ' + str(finalStates) + '\n')
    print('TM rules amount: ' + str(len(rules)) + '\n')
    
    print('Creating noncontracting grammar productions...')

    # create grammar
    productions = []

    # 1 - initial state
    productions += [
        Production('A1', 
                   '[{},{},{},{},{}]'.format(q0, lm, a, a, rm))
        for a in alphabetWM]

    # 2
    for rule in rules:
        q = rule.curState

        if q in finalStates:
            continue

        p = rule.nextState
        X = rule.curSymb
        Y = rule.nextSymb

        if rule.direction == Direction.Right:
            if X == lm and Y == lm:
                productions += [
                    Production('[{},{},{},{},{}]'.format(q,lm,I,a,rm),
                               '[{},{},{},{},{}]'.format(lm,p,I,a,rm))
                    for a in alphabetWM
                    for I in gammaWM]
            else:
                productions += [
                    Production('[{},{},{},{},{}]'.format(lm,q,X,a,rm),
                               '[{},{},{},{},{}]'.format(lm,Y,a,p,rm))
                    for a in alphabetWM]
            
        else:
            if X == rm and Y == rm:
                productions += [
                    Production('[{},{},{},{},{}]'.format(lm,I,a,q,rm),
                               '[{},{},{},{},{}]'.format(lm,p,I,a,rm))
                    for a in alphabetWM
                    for I in gammaWM]
            else:
                productions += [
                    Production('[{},{},{},{},{}]'.format(lm,q,X,a,rm),
                               '[{},{},{},{},{}]'.format(p,lm,Y,a,rm))
                    for a in alphabetWM]
    
    # 3
    for q in finalStates:
        for a in alphabetWM:
            for X in gammaWM:
                productions.append(
                    Production('[{},{},{},{},{}]'.format(q,lm,X,a,rm),
                               '{}'.format(a)))

                productions.append(
                    Production('[{},{},{},{},{}]'.format(lm,q,X,a,rm),
                               '{}'.format(a)))

                productions.append(
                    Production('[{},{},{},{},{}]'.format(lm,X,a,q,rm),
                               '{}'.format(a)))


    # 4
    for a in alphabetWM:
        productions.append(
            Production('A1',
                       '[{},{},{},{}] A2'.format(q0,lm,a,a)))

        productions.append(
            Production('A2',
                       '[{},{}] A2'.format(a,a)))

        productions.append(
            Production('A2',
                       '[{},{},{}]'.format(a,a,rm)))

    # 5
    for rule in rules:
        q = rule.curState

        if q in finalStates:
            continue

        p = rule.nextState
        X = rule.curSymb
        Y = rule.nextSymb

        if rule.direction == Direction.Right:
            
            if X == lm and Y == lm:
                productions += [
                    Production('[{},{},{},{}]'.format(q,lm,I,a),
                               '[{},{},{},{}]'.format(lm,p,I,a))
                    for a in alphabetWM
                    for I in gammaWM]
            else:
                productions += [
                    Production('[{},{},{},{}] [{},{}]'.format(lm,q,X,a,Z,b),
                               '[{},{},{}] [{},{},{}]'.format(lm,Y,a,p,Z,b))
                    for a in alphabetWM
                    for b in alphabetWM
                    for Z in gammaWM]
        else:
            productions += [
                Production('[{},{},{},{}]'.format(lm,q,X,a),
                           '[{},{},{},{}]'.format(p,lm,Y,a))
                for a in alphabetWM]

        # 6
        if rule.direction == Direction.Right:
            productions += [
                Production('[{},{},{}] [{},{}]'.format(q,X,a,Z,b),
                           '[{},{}] [{},{},{}]'.format(Y,a,p,Z,b))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]

            productions += [
                Production('[{},{},{}] [{},{},{}]'.format(q,X,a,Z,b,rm),
                           '[{},{}] [{},{},{},{}]'.format(Y,a,p,Z,b,rm))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]
            
            # if word length is 2
            productions += [
                Production('[{},{},{},{}] [{},{},{}]'.format(lm,q,X,a,Z,b,rm),
                           '[{},{},{}] [{},{},{},{}]'.format(lm,Y,a,p,Z,b,rm))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]
        else:
            productions += [
                Production('[{},{}] [{},{},{}]'.format(Z,b,q,X,a),
                           '[{},{},{}] [{},{}]'.format(p,Z,b,Y,a))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]

            productions += [
                Production('[{},{},{}] [{},{},{}]'.format(lm,Z,b,q,X,a),
                           '[{},{},{},{}] [{},{}]'.format(lm,p,Z,b,Y,a))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]

            # if word length is 2
            productions += [
                Production('[{},{},{}] [{},{},{},{}]'.format(lm,Z,b,q,X,a,rm),
                           '[{},{},{},{}] [{},{},{}]'.format(lm,p,Z,b,Y,a,rm))
                for a in alphabetWM
                for b in alphabetWM
                for Z in gammaWM]

        # 7
        if rule.direction == Direction.Right:
            productions += [
                Production('[{},{},{},{}]'.format(q,X,a,rm),
                           '[{},{},{},{}]'.format(Y,a,p,rm))
                for a in alphabetWM]
        else:
            if X == rm and Y == rm:
                productions += [
                    Production('[{},{},{},{}]'.format(I,a,q,rm),
                               '[{},{},{},{}]'.format(p,I,a,rm))
                    for a in alphabetWM
                    for I in gammaWM]
            else:
                productions += [
                    Production('[{},{}] [{},{},{},{}]'.format(Z,b,q,X,a,rm),
                               '[{},{},{}] [{},{},{}]'.format(p,Z,b,Y,a,rm))
                    for a in alphabetWM
                    for b in alphabetWM
                    for Z in gammaWM]

    for a in alphabetWM:
        for X in gammaWM:

            # 8
            for q in finalStates:

                productions.append(
                    Production('[{},{},{},{}]'.format(q,lm,X,a), 
                               a))
                
                productions.append(
                    Production('[{},{},{},{}]'.format(lm,q,X,a), 
                               a))
                
                productions.append(
                    Production('[{},{},{}]'.format(q,X,a), 
                               a))
                
                productions.append(
                    Production('[{},{},{},{}]'.format(q,X,a,rm), 
                               a))

                productions.append(
                    Production('[{},{},{},{}]'.format(X,a,q,rm), 
                               a))
            
            # 9
            for b in alphabetWM:
                productions.append(
                    Production('{} [{},{}]'.format(a,X,b), 
                               '{} {}'.format(a,b)))
                
                productions.append(
                    Production('{} [{},{},{}]'.format(a,X,b,rm), 
                               '{} {}'.format(a,b)))
                
                productions.append(
                    Production('[{},{}] {}'.format(X,a,b), 
                               '{} {}'.format(a,b)))
                
                productions.append(
                    Production('[{},{},{}] {}'.format(lm,X,a,b), 
                               '{} {}'.format(a,b)))

    # optimization
    root = Tree('A1')

    reviewedTrees = set()
    root.findChildren(reviewedTrees, productions)

    result = list(dict.fromkeys(root.productions))

    result = removeUnnecessary(result)
    result = removeUnnecessaryHeads(result)

    print('Noncontracting grammar productions amount: ' + str(len(result)) + '\n')

    plines = [p.getString() for p in result]

    print('Writing to file: ' + outputFilePath)

    with open(outputFilePath, 'w') as f:
        f.writelines(plines)
        
def removeUnnecessary(allProductions):
    flag = True

    prevProductions = allProductions
    
    while flag:

        result = list()
        allHeadNts = set()
        flag = False

        for p in prevProductions:
            allHeadNts = allHeadNts.union(p.head.split(' '))

        for p in prevProductions:
            ts = p.tail.split(' ')

            exist = True

            for t in ts:
                if t not in allHeadNts and 'not_prime' not in t:
                    exist = False
                    break

            if exist:
                result.append(p)
            else:
                flag = True

        prevProductions = result
    
    return result


def removeUnnecessaryHeads(allProductions):
    flag = True

    prevProductions = allProductions
    
    while flag:

        result = list()
        allTailNts = set()
        flag = False

        for p in prevProductions:
            allTailNts = allTailNts.union(p.tail.split(' '))

        for p in prevProductions:
            hs = p.head.split(' ')

            exist = True

            for h in hs:
                if h not in allTailNts and h != 'A1':
                    exist = False
                    break

            if exist:
                result.append(p)
            else:
                flag = True

        prevProductions = result
    
    return result

# call main method
main(sys.argv)