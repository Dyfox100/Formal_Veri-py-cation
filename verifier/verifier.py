import z3

class Verifier():

    def verify(self, parsed_verification_blocks):
        block_counter = 0
        for parsed_verification_block in parsed_verification_blocks:

            type = parsed_verification_block['type']

            counter_example = ""

            #try to find counter example. If found return it, else continue.
            if type == 'invariant':
                counter_example = self._verify_invariant(parsed_verification_block)

            elif type == 'conditional':
                counter_example = self._verify_conditional(parsed_verification_block)

            elif type == 'command':
                counter_example = self._verify_command(parsed_verification_block)

            if counter_example:
                return 'Error Found in Block At Line Number: ' + str(parsed_verification_block['line_number'])

        #no counter examples found, all blocks verified
        return 'All Conditions Verified and Passed'

    def _verify_invariant(self, parsed_verification_block):
        return self._verify_command(parsed_verification_block)

    def _verify_command(self, parsed_verification_block):
        solver = z3.Solver()

        for var in parsed_verification_block['commands'].keys():
            exec(var + ' = z3.Int(var)')
        #add pre Conditions
        for pre_condition in parsed_verification_block['precondition']:
            solver.add(eval(pre_condition))

        for post_condition in parsed_verification_block['postcondition']:
            solver.add(eval('z3.Not(' + post_condition + ')'))

        commands = parsed_verification_block['commands']
        for command in commands.keys():
            if commands[command].strip():
                solver.add(eval(command + '==' + commands[command]))

        if str(solver.check()) == 'sat':
            return solver.model()
        else:
             return None

    def _verify_conditional(self, parsed_verification_block):
        solver = z3.Solver()
        #Add all variables to z3
        for var in parsed_verification_block['if-commands'].keys():
            exec(var + ' = z3.Int(var)')
        for var in parsed_verification_block['else-commands'].keys():
            exec(var + ' = z3.Int(var)')

        for precondition in parsed_verification_block['precondition']:
            solver.add(eval(precondition))
        else_commands_string = if_commands_string = 'z3.And('
        #Create long "And()" z3 condition of every command in if statement block
        for command in parsed_verification_block['if-commands'].keys():
            if parsed_verification_block['if-commands'][command].strip():
                full_command = (command + '==' + parsed_verification_block['if-commands'][command])
                if_commands_string += full_command + ','
        if_commands_string += ')'
        #same for else
        for command in parsed_verification_block['else-commands'].keys():
            if parsed_verification_block['else-commands'][command].strip():
                full_command = (command + '==' + parsed_verification_block['else-commands'][command])
                else_commands_string += full_command + ','
        else_commands_string += ')'

        if_condition_from_code = parsed_verification_block['code'].replace('if', '').replace(':',"").strip()

        entire_if_else_z3_command = 'z3.If(' + if_condition_from_code + ','
        entire_if_else_z3_command += if_commands_string + ','
        entire_if_else_z3_command += else_commands_string + ',)'

        for postcondition in parsed_verification_block['postcondition']:
            solver.add(eval('z3.Not(z3.Implies(' + entire_if_else_z3_command + ',' + postcondition +'))'))

        if str(solver.check()) == 'sat':
            return solver.model()
        else:
             return None



if __name__ == '__main__':
    verifier = Verifier()
    parsed_blocks = [
          {
          'type': 'command',
           'precondition': ['j0==4'],
           'postcondition': ['j1==7'],
           'code': '',
            'commands': {'j': '', 'j0': '', 'j1': 'j0 + 3'}
            },
            {
            'type': 'invariant',
            'precondition': ['j0==0', 'initial0==x0'],
            'postcondition': ['x2==initial0+2*j1'],
            'code': 'while j<i:',
            'commands': {'initial0': '', 'x': '', 'x0': '', 'x1': 'x0 + 1', 'x2': 'x1 + 1', 'j': 'j', 'j0': 'j', 'j1': 'j0 + 1'}},
            {
            'type': 'conditional',
             'precondition': ['True'],
             'postcondition': ['x2==4 + j0'],
             'code': 'if (x0!=4):',
             'if-commands': {'x0': '', 'x1': ' 4', 'x2': ' x1 + j0', 'j0': ''},
             'else-commands': {'x0': '', 'j0': '', 'x2': ' x0 + j0'}}
            ]
    print(verifier.verify(parsed_blocks))
