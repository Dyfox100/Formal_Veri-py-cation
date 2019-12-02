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


            type, pre_conditions, post_conditions = self._get_type_pre_and_post_conditions(FV_line)

            vars_and_commands = {}

            for index, pre_condition in enumerate(pre_conditions):
                pre_conditions[index], vars_and_commands = self._replace_variable_names(pre_condition, vars_and_commands)

            #get while or if condition
            if type in ['invariant', 'conditional']:
                code =  verification_block.pop(0)
            else:
                code = ""


            for command in verification_block:
                #split left and right sides of expression on equals sign.
                left_and_right_sides_expression = command.split('=', 1)
                if len(left_and_right_sides_expression) != 2:
                    raise ValueError("Left and Right sides of Expression are not of length 2")

                expression, vars_and_commands = self._replace_variable_names(left_and_right_sides_expression[1], vars_and_commands)

                variable_stem = left_and_right_sides_expression[0].strip()
                vars_and_commands[variable_stem + '0'] = ""
                variable_assigned_to = variable_stem + '1'

                while variable_assigned_to in vars_and_commands:
                    incrementer = variable_assigned_to.replace(variable_stem, "")
                    new_incrementer = int(incrementer) + 1
                    variable_assigned_to = variable_stem + str(new_incrementer)

                vars_and_commands[variable_assigned_to] = expression

            for index, post_condition in enumerate(post_conditions):
                post_conditions[index], vars_and_commands = self._replace_variable_names(post_condition, vars_and_commands)

            parsed_block = {
                'type': type,
                'precondition': pre_conditions,
                'postcondition': post_conditions,
                'code': code,
                'commands': vars_and_commands
            }
            parsed_blocks.append(parsed_block)

        return parsed_blocks

    def _get_type_pre_and_post_conditions(self, first_line_verification_block):
        split_line = first_line_verification_block.split("_")
              
        type = split_line[1]
        pre_conditions = split_line[2].split(',')
        post_conditions = split_line[3].split(',')

        return type, pre_conditions, post_conditions

    def _replace_variable_names(self, expression, vars_and_commands):
        vars_in_expression = re.split(r"[=<>%+\/\*\-\(\)(0-9)]", expression)
        for var in vars_in_expression:
            if var.strip():
                variable_stem = var.strip()
                var = variable_stem + '0'
                variable_incrementer = 0

                while var in vars_and_commands:
                    variable_incrementer = var.replace(variable_stem, "")
                    var = variable_stem + str(int(variable_incrementer) + 1)
                    
                if not variable_stem + str(int(variable_incrementer)) in vars_and_commands:
                    vars_and_commands[variable_stem + str(int(variable_incrementer))] = ''

                expression = expression.replace(variable_stem, variable_stem + str(int(variable_incrementer)))
        return expression, vars_and_commands



if __name__=='__main__':
    parser = Parser()
    print(parser.parse([
            ['#FV_invariant_j==0,x==initial_x==initial+j', 'while j<i:', 'x = x + 1', 'x = x**1', 'x = x + 1','j= x + j', 'j = j + 1'],
            ['#FV_command_j==4_j==7', 'j = j + 3']
            ]))
