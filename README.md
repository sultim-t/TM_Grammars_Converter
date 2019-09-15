# Turing machine to Grammars Converter
Converter from turing machine to unrestricted and context-sensitive grammars.

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
Input format: <unrestricted_grammar_file>
'input_turing_machine_file' is a file which contains created unrestricted grammar from TM_UG_Converter.

#### Output
UG_Generator prints several generated words for specified unrestricted grammar.
