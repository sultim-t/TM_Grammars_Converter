# Turing machine to Grammars Converter
Converter from turing machine to unrestricted and context-sensitive grammars.

Note: optimized for LBA that recognizes prime numbers.

# Usage
Programs use Python 3.7.3

To create unrestricted grammar:
```
TM_UG_Converter.py lba.txt ug.txt
```
Then generate prime numbers from this grammar in range from a (inclusive) to b (inclusive) (a,b are positive integers):
```
UG_Generator.py ug.txt 2 10
```
Or just check some number:
```
UG_Generator.py ug.txt 5
```

Same for context-sensitive grammars:
```
TM_CSG_Converter.py lba.txt ncg.txt
CSG_Generator.py ncg.txt 2 10
```

# Info
## Converters
TM_UG_Converter.py is a converter from turing machine to unrestricted grammar.

TM_CSG_Converter.py is to context-sensitive grammar.
Actually, to noncontracting grammars as they can be transformed to context-sensitive ones.

#### Input
Input format: <input_turing_machine_file> <output_grammar_file>

'input_turing_machine_file' must contain delta functions of turing machine. This turing machine must be an LBA with endmarkers 'c' and '$'.

Syntax and simulator for turing machine: http://corelab.ntua.gr/tm/

#### Output
Output file will contain unrestricted or context-sensitive (noncontracting) grammar as a list of productions: "<> -> <>"

## Generators
UG_Generator.py is a word generator for unrestricted grammar.

CSG_Generator.py is for context-sensitive (noncontracting) grammar.

#### Input
Input format: <input_grammar_file> <number_to_check>

Or: <input_grammar_file> <range_start_inclusive> <range_end_inclusive>

#### Output
UG_Generator prints generated words for specified unrestricted or context-sensitive (noncontracting) grammar.

Also, log file is generated and written to file with suffix '_Log.txt'.
