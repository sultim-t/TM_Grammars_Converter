import sys
import random

def main(argv):

    #TODO: REMOVE
    argv.append('grammar.txt')
    
    if len(argv) < 2:
        print('Expected input: <input_unrestricted_grammar_file>')
        return

    with open(argv[1]) as f:
        lines = f.readlines()

    lines = [x.strip() for x in lines]

    productions = []
    heads = []

    for line in lines:
        splitted = line.split('->')

        head = ' ' + splitted[0] if len(splitted) == 2 else ' ' + splitted[0] + ' '
        tail = splitted[1] + ' ' if len(splitted) == 2 else '' # check epsilon

        heads.append(head)

        productions.append((head, tail))

    initialNt =' (,_) 0 (I,I) (I,I) (I,I) (I,I) (I,I) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) (,_) ' #' A1 '

    for i in range(3, 4):
        current = initialNt
        depth = 0

        # while there are non terminals
        while any(key in current for key in heads):
            # check each production
            for head, tail in productions:

                # while head is contained by current
                while head in current: #and depth < i:
                    current = current.replace(head, tail, 1)
                    depth += 1
                    #print(current)
                    #printTM(current)

                depth = 0
            
        printTMWord(current)

def printTM(str):
    '''Print turing machine's line'''
    out = ''
    splitted = str.split(' ')
    for s in splitted:
        if '(' in s:
            s = s.replace(')', '')
            tuple = s.split(',')
            out += tuple[1]
    print(out)

def printTMWord(str):
    '''Print turing machine's initial word'''
    out = ''
    splitted = str.split(' ')
    for s in splitted:
        if not '(' in s:
            out += s
    print(out)


# call main method
main(sys.argv)