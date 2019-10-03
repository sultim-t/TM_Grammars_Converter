# Turing machine to Grammars Converter
Converter from turing machine to unrestricted and context-sensitive grammars.

# Usage
Programs use Python 3.7.3

Firstly, create unrestricted grammar:
```
TM_UG_Converter.py lba.txt glba.txt
```
Then generate prime numbers from this grammar in range from a (inclusive) to b (inclusive):
```
UG_Generator.py lba.txt 2 10
```
Or just check some number:
```
UG_Generator.py lba.txt 5
```
# Unrestricted grammars
## Converter 
TM_UG_Converter.py is a converter from turing machine to unrestricted grammar.

#### Input
Input format: <input_turing_machine_file> <output_unrestricted_grammar_file>

'input_turing_machine_file' must contain delta functions of turing machine.
Syntax and simulator for turing machine: http://corelab.ntua.gr/tm/

#### Output
Output file will contain unrestricted grammar as a list of productions: "<> -> <>"

## Generator
UG_Generator.py is a word generator for unrestricted grammar.

#### Input
Input format: <input_unrestricted_grammar_file> <number_to_check>

Or: <input_unrestricted_grammar_file> <range_start_inclusive> <range_end_inclusive>

'input_turing_machine_file' is a file which contains created unrestricted grammar from TM_UG_Converter.

#### Output
UG_Generator prints generated words for specified unrestricted grammar.

Also, log file is generated with suffix '_Log.txt'.
