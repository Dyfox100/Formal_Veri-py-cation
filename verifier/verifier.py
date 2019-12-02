import z3

class Verifier():

    def verify(self, parsed_verification_blocks):

        for parsed_verification_block in parsed_verification_blocks:
            type = parsed_verification_block['type']

            if type == 'invariant':
                counter_example = self._verify_invariant(parsed_verification_block)
                if counter_example:
                    parsed_verification_block['Counter Example'] = counter_example
                    return parsed_verification_block

            elif type == 'conditional':
                counter_example = self._verify_conditional(parsed_verification_block)
                if counter_example:
                    parsed_verification_block['Counter Example'] = counter_example
                    return parsed_verification_block

            elif type == 'command':
                counter_example = self._verify_command(parsed_verification_block)
                if counter_example:
                    parsed_verification_block['Counter Example'] = counter_example
                    return parsed_verification_block

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
        pass



if __name__ == '__main__':
    verifier = Verifier()
    parsed_blocks = [
          {
          'type': 'command',
           'precondition': ['j0==4'],
           'postcondition': ['j1==7'],
           'code': '',
            'commands': {'j': 'j', 'j0': 'j', 'j1': 'j0 + 3'}
            },

                        {'type': 'invariant',
                        'precondition': ['j0==0', 'initial0==x0'],
                           'postcondition': ['x2==initial0+2*j1'],
                            'code': 'while j<i:',
                             'commands': {'initial0': 'x0', 'x': 'x', 'x0': 'x', 'x1': 'x0 + 1', 'x2': 'x1 + 1', 'j': 'j', 'j0': 'j', 'j1': 'j0 + 1'}},
            ]
    print(verifier.verify(parsed_blocks))
