import re

class Parser():
    """Parses verification blocks into commands,
    Pre conditions, and post conditions"""

    def parse(self, verification_blocks):
        #go through each block. Get list of preconditions and post conditions out of first comment.
        #Get type out of first comment. #Get list of commands. Make new vars that are for commands that affect initial
        parsed_blocks = []
        for verification_block in verification_blocks:
            #Firest line with description of verification conditions
            FV_line = verification_block.pop(0)
            if "#FV" not in FV_line:
                raise ValueError("Incorrect Line is first in verification_block")

            type, pre_condition, post_condition = self._get_type_pre_and_post_conditions(FV_line)

            #get while or if condition
            if type in ['invariant', 'conditional']:
                code =  verification_block.pop(0)
            else:
                code = ""

            vars_and_commands = {}

            for command in verification_block:
                #split left and right sides of expression on equals sign.
                left_and_right_sides_expression = command.split('=', 1)
                if len(left_and_right_sides_expression) != 2:
                    raise ValueError("Left and Right sides of Expression are not of length 2")


                expression = left_and_right_sides_expression[1]
                vars_in_expression = re.split(r"[+\/\*\-\(\)(0-9)]", expression)
                for var in vars_in_expression:
                    if var.strip():
                        expression = expression.replace(var, self._replace_variable_name(vars_and_commands, var))

                variable_stem = left_and_right_sides_expression[0].strip()
                variable_assigned_to = variable_stem + '0'

                while variable_assigned_to in vars_and_commands:
                    incrementer = variable_assigned_to.replace(variable_stem, "")
                    new_incrementer = int(incrementer) + 1
                    variable_assigned_to = variable_stem + str(new_incrementer)


                vars_and_commands[variable_assigned_to] = expression



            parsed_block = {
                'type': type,
                'precondition': pre_condition,
                'postcondition': post_condition,
                'code': code,
                'commands': vars_and_commands
            }
            parsed_blocks.append(parsed_block)

        return parsed_blocks

    def _get_type_pre_and_post_conditions(self, first_line_verification_block):
        split_line = first_line_verification_block.split("_")
        type = split_line[1]
        pre_condition = split_line[2].split(',')
        post_condition = split_line[3].split(',')
        return type, pre_condition, post_condition

    def _replace_variable_name(self,vars_and_commands, variable):

        variable_stem = variable.strip()
        variable = variable_stem + '0'
        variable_incrementer = 0

        while variable in vars_and_commands:
            variable_incrementer = variable.replace(variable_stem, "")
            variable = variable_stem + str(int(variable_incrementer) + 1)

        return variable_stem + str(int(variable_incrementer))


if __name__=='__main__':
    parser = Parser()
    print(parser.parse([
            ['#FV_invariant_j==0,i==5_x==x+j', 'while j<i:', 'x = x + 1', 'x = x**1', 'x = x + 1','j= x + j', 'j = j + 1'],
            ['#FV_command_j==4_j==7', 'j = j + 3']
            ]))
