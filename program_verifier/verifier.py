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
        pass

    def _verify_command(self, parsed_verification_blocks):
        pass

    def _verify_conditional(self, parsed_verification_block):
        pass





















if __name__ == '__main__':
    parsed_blocks = [
        {
        'type': 'invariant',
         'precondition': ['j==0','i==5'],
          'postcondition': ['x==x+j'],
           'code': 'while j<i:',
            'commands': {'x0': 'x0+ 1', 'x1': 'x0**1', 'x2': 'x1+ 1', 'j0': 'x2+j0', 'j1': 'j0+ 1'}},
        {
        'type': 'command',
        'precondition': ['j==4'],
        'postcondition': ['j==7'],
        'code': '',
        'commands': {'j0': 'j0+ 3'}}
    ]
