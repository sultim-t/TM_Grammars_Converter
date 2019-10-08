import sys
import random

def main(argv):
    
    if len(argv) < 3:
        print('Expected input:\n  <input_unrestricted_grammar_file> <number_to_check> or \n  <input_unrestricted_grammar_file> <range_start> <range_end>')
        return

    numbersToCheck = []

    if (len(argv) == 3):
        numbersToCheck.append(int(argv[2]))
    else:
        numbersToCheck = range(int(argv[2]), int(argv[3]) + 1)
   
    with open(argv[1]) as f:
        lines = f.readlines()

    logText = []

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
    results = []

    # assume, that result of first 5 types of non deterministic productions
    for i in range(0, len(numbersToCheck)):
        amount = '(1,1) ' * numbersToCheck[i]
        initialWords.append(' 0 (c,c) ' + amount + '($,$) ')

    # actual simulation of the grammar
    for i in range(0, len(initialWords)):

        current = initialWords[i]
        
        logText.append('Created word: \"' + current + '\". Processing...\n')

        error = False

        # while there are non terminals
        while containsNonTerminal(current, nonTerminals):
            simulated = False

            # check each production
            for head, tail in productions:
                (current, wasSimulated) = simulateProduction(current, head, tail)
                simulated = simulated or wasSimulated

                if wasSimulated:
                    logText.append('Using: ' + head + '->' + tail + ':\n' + current + '\n\n')

                    # if was simulated, start from the beginning of the production list

                    # to prevent non-determinism when
                    # replacing to epsilon (step 10),
                    # we assume that it will be the last production in a list
                    break

            # if there is no simulation but there are non-terminals
            if not simulated:
                break

        # simulated is True if
        # there are no non-terminals and there are no productions to simulate
        printResult(current, numbersToCheck[i], simulated)

        logText.append('\n\n\n')

    # write log to file
    with open(argv[1] + '_Log.txt', 'w+') as logFile:
        logFile.writelines(logText)

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

def printResult(current, number, isPrime):
    '''Removes spaces and prints result'''
    out = current
    print(str(number) + ' is ' + ('    PRIME' if isPrime else 'NOT prime') + 
          ('. Grammar result:' + out if isPrime else '. Word has non terminals but hasn\'t needed productions'))

# call main method
main(sys.argv)