import sys
import random

def main(argv):
    
    argv.append('glba.txt')

    if len(argv) < 2:
        print('Expected input: <input_unrestricted_grammar_file>')
        return
    
    # how many space there needed after a word;
    # f.e.: if word is 'II' but 
    # number of blanks that uses TM is five times larger,
    # then multiplier must be 5
    lineMultiplier = 5
   
    with open(argv[1]) as f:
        lines = f.readlines()

    lines = [x.strip() for x in lines]

    productions = []
    heads = []

    for line in lines:
        splitted = line.split('->')

        # add spaces on the left and right (if needed),
        # also check if tail is epsilon 
        head = ' ' + splitted[0] if len(splitted) == 2 else ' ' + splitted[0] + ' '
        tail = splitted[1] + ' ' if len(splitted) == 2 else ''

        heads.append(head)

        productions.append((head, tail))

    nonTerminals = getNonTerminals(heads) 

    initialWords = []

    # assume, that result of first 5 types of non deterministic productions
    initialWords.append(' 0 ($,$) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) (1,1) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) (1,1) (1,1) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) ($,$) ')
    initialWords.append(' 0 ($,$) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) (1,1) ($,$) ')

    # actual simulation of the grammar
    for i in range(0, len(initialWords)):
        
        # adding blank symbol to the left of word 
        # as grammar that simulates TM works only on a half of the line
        current =  ' (,_)' + initialWords[i]
        
        error = False

        # while there are non terminals
        while containsNonTerminal(current, nonTerminals):
            simulated = False

            # check each production
            for head, tail in productions:
                (current, wasSimulated) = simulateProduction(current, head, tail)
                simulated = simulated or wasSimulated

                if wasSimulated:
                    # to prevent non-determinism when
                    # replacing to epsilon (step 10),
                    # we assume that it will be the last production in a list
                    break

            # if there is no simulation but there are non-terminals
            if not simulated:
                break

        # there are no non-terminals and there are no productions to simulate
        if simulated:

            # remove first (,_) that was added
            current = current.replace('(,_)', '', 1)
            
            printResult(current)

def simulateProduction(current, head, tail):
    wasSimulated = False

    # while head is contained by current
    while head in current:
        current = current.replace(head, tail, 1)
        wasSimulated = True

        #print(current)
        #printTM(current)

    return (current, wasSimulated)

def simulateProductionLimited(current, head, tail, limit):
    '''
    Try to simulate production, but number of replacements of current production is limited.
    Use this to prevent endless replacements.
    '''
    iteration = 0
    while head in current and iteration < limit:
        current = current.replace(head, tail, 1)
        iteration += 1
        #print(current)
        #printTM(current)

    return current

def containsNonTerminal(str, nonTerminals):
    # ignore first non terminal, as it's '(,_)'
    str = str.replace('(,_)', '', 1)

    return any(nonTerm in str for nonTerm in nonTerminals)

def getNonTerminals(productionHeads):
    nonTerminals = set()

    for head in productionHeads:
        ws = set(head.split(' '));
        nonTerminals = nonTerminals.union(ws)

    # ignore epsilon
    if '' in nonTerminals:
        nonTerminals.remove('')

    return nonTerminals

def printTM(str):
    '''
    Print turing machine's line. 
    I.e. prints only second part of tuples in str
    '''
    out = ''
    splitted = str.split(' ')
    for s in splitted:
        if '(' in s:
            s = s.replace(')', '')
            tuple = s.split(',')
            out += tuple[1]
    print(out)

def printResult(str):
    '''Removes spaces and prints result'''
    out = str.replace(' ', '')
    print("Result: " + out)

# call main method
main(sys.argv)