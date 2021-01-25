# Formal_Veri-py-cation
Formal Veri-py-cation is a simple hoare logic verification engine built for Python code. A developer can provide code annotations in comments and Formal Veri-py-cation will generate verification conditions from the comment and use the Z3 smt solver to verify the conditions. 
## Usage
To use Formal Veri-py-cation run the `verify_python_script.py` and provide a file name. This will either output a successful result, or print the line number of the block the error was found in. For example:
![Photo of command line](https://github.com/Dyfox100/Formal_Veri-py-cation/blob/master/example_photos/example_command_line.png)

#### Structured Comments
 To specify verification conditions you use structured comments. The comments take the form:
 
 `#FV_<type of condition>_<starting_condition1>,<starting_condition2>_<condition1>_<condition2>`
 
 Any number of conditions can be provided, each seperated by an underscore. There are three types of verification conditions supported; commands, conditionals, and loop invariants. A command verification block is used to verify a set of python commands (eg. x = 1; x = x + 1). A conditional verifies an if/else branch, and a loop invariant verifies a while loop. Each block should be terminated with a `#END_FV` comment. For example:
 ```
    #FV_command_j==4,x==21_j==125

    j = 1 + j
    j = (x - 1 + j) * j

    #END_FV
  ``` 
  This block of commands verifies if j is equal to 4 and x is equal to 21, then at the end of the block, j is equal to 125.
  See the test_files for more examples.
  # Installation
  Download the source code from here. Run `pip install -r requirements.txt`. This may take a few minutes as Z3 is a fairly large package.
