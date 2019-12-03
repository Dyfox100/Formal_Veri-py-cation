import re

class Parser():
    """Parses verification blocks into commands,
    Pre conditions, and post conditions"""

    def parse(self, verification_blocks):
        #go through each block. Get list of preconditions and post conditions out of first comment.
        #Get type out of first comment. #Get list of commands. Make new vars that are for commands that affect initial
        parsed_blocks = []
        for verification_block in verification_blocks:
            #First line with description of verification conditions
            FV_line = verification_block.pop(0)
            if "#FV" not in FV_line:
                raise ValueError("Incorrect Line is first in verification_block")
            line_number = verification_block.pop(0)

            type, pre_conditions, post_conditions = self._get_type_pre_and_post_conditions(FV_line)

            if type == 'conditional':
                parsed_blocks.append(self._parse_conditionals(\
                verification_block, type, line_number, pre_conditions, post_conditions))
            else:
                parsed_blocks.append(self._parse_command_and_invariant(\
                    verification_block, type, line_number, pre_conditions, post_conditions))

        return parsed_blocks

    def _get_type_pre_and_post_conditions(self, first_line_verification_block):
        split_line = first_line_verification_block.split("_")

        type = split_line[1]
        pre_conditions = split_line[2].split(',')
        post_conditions = split_line[3].split(',')

        return type, pre_conditions, post_conditions

    def _parse_conditionals(self, verification_block, type, line_number, pre_conditions, post_conditions):
        vars_and_commands = {}

        for index, pre_condition in enumerate(pre_conditions):
            pre_conditions[index], vars_and_commands = self._replace_variable_names(pre_condition, vars_and_commands)

        if_variables_and_commands = vars_and_commands.copy()
        else_variables_and_commands = vars_and_commands.copy()
        #if condition is first. else is somewhere lower in code.
        if_condition =  verification_block.pop(0).split('if')[1]
        if_condition_renamed, vars_and_commands = self._replace_variable_names(if_condition, vars_and_commands)
        if_condition = 'if' + if_condition_renamed

        else_condition = ""
        #parse if block into if vars and commands, and else into else vars and commands
        for index, command in enumerate(verification_block):
            if 'else' in command:
                #parse the if and else blocks of code
                if_variables_and_commands = self._parse_commands(verification_block[:index], if_variables_and_commands)
                else_variables_and_commands = self._parse_commands(verification_block[index+1:], else_variables_and_commands)

        for index, post_condition in enumerate(post_conditions):
            post_condition_vars = [var.strip() for var in self._extract_variable_names_from_expression(post_condition) if var.strip()]

            for var in post_condition_vars:
                new_var_name = ''

                new_variable_name_if, _ = self._replace_variable_names(var, if_variables_and_commands)
                new_variable_incrementer_if = int(new_variable_name_if.replace(var, ""))
                new_variable_name_else, _ = self._replace_variable_names(var, else_variables_and_commands)
                new_variable_incrementer_else = int(new_variable_name_else.replace(var, ""))

                if new_variable_incrementer_if > new_variable_incrementer_else:
                    new_var_name = new_variable_name_if
                    else_variables_and_commands[new_var_name] = \
                        else_variables_and_commands.pop(new_variable_name_else)
                else:
                    new_var_name = new_variable_name_else
                    if_variables_and_commands[new_var_name] = \
                        if_variables_and_commands.pop(new_variable_name_if)

                post_conditions[index] = post_conditions[index].replace(var, new_var_name)

        code = if_condition

        parsed_block = {
            'type': type,
            'line_number': line_number,
            'precondition': pre_conditions,
            'postcondition': post_conditions,
            'code': code,
            'if-commands': if_variables_and_commands,
            'else-commands': else_variables_and_commands
        }
        return parsed_block

    def _parse_command_and_invariant(self, verification_block, type, line_number, pre_conditions, post_conditions):
        vars_and_commands = {}
        for index, pre_condition in enumerate(pre_conditions):
            pre_conditions[index], vars_and_commands = self._replace_variable_names(pre_condition, vars_and_commands)

        #get while condition if parsing an invariant.
        if type in ['invariant']:
            while_condition = verification_block.pop(0).split('while')[1]
            while_condition_renamed, vars_and_commands = self._replace_variable_names(while_condition, vars_and_commands)
            code = 'while' + while_condition_renamed
        else:
            code = ""

        vars_and_commands = self._parse_commands(verification_block, vars_and_commands)

        for index, post_condition in enumerate(post_conditions):
            post_conditions[index], vars_and_commands = self._replace_variable_names(post_condition, vars_and_commands)

        parsed_block = {
            'type': type,
            'line_number': line_number,
            'precondition': pre_conditions,
            'postcondition': post_conditions,
            'code': code,
            'commands': vars_and_commands
        }

        return parsed_block

    def _parse_commands(self, commands, parsed_vars_and_commands):

        for command in commands:
            #split left and right sides of expression on equals sign.
            left_and_right_sides_expression = command.split('=', 1)
            if len(left_and_right_sides_expression) != 2:
                raise ValueError("Left and Right sides of Expression are not of length 2")

            expression, parsed_vars_and_commands = self._replace_variable_names(left_and_right_sides_expression[1], parsed_vars_and_commands)

            variable_stem = left_and_right_sides_expression[0].strip()
            parsed_vars_and_commands[variable_stem + '0'] = ""
            variable_assigned_to = variable_stem + '1'

            while variable_assigned_to in parsed_vars_and_commands:
                incrementer = variable_assigned_to.replace(variable_stem, "")
                new_incrementer = int(incrementer) + 1
                variable_assigned_to = variable_stem + str(new_incrementer)

            parsed_vars_and_commands[variable_assigned_to] = expression

        return parsed_vars_and_commands

    def _replace_variable_names(self, expression, vars_and_commands):
        vars_in_expression = self._extract_variable_names_from_expression(expression)
        expression = ' ' + expression + ' '
        for var in vars_in_expression:
            variable_stem = var.strip()
            if variable_stem:
                variable_name = variable_stem + '0'
                variable_incrementer = 0

                while variable_name in vars_and_commands:
                    variable_incrementer = variable_name.replace(variable_stem, "")
                    variable_name = variable_stem + str(int(variable_incrementer) + 1)

                if not variable_stem + '0' in vars_and_commands:
                    vars_and_commands[variable_stem + '0'] = ""

                expression = re.sub(r"(?<=[^a-zA-Z])" + variable_stem + "[0-9]*(?=[^a-zA-Z])", variable_stem + str(int(variable_incrementer)),expression)

        expression = expression.strip()
        return expression, vars_and_commands

    def _extract_variable_names_from_expression(self, expression):
        return re.split(r"True|False|[!:=<>%+\/\*\-\(\)0-9]", expression)

if __name__=='__main__':
    parser = Parser()
    print(parser.parse([
            ['#FV_invariant_j==0,x==initial_x==initial+j', 'while j<i:', 'x = x + 1', 'x = x**1', 'x = x + 1','j= x + j', 'j = j + 1'],
            ['#FV_command_j==4_j==7', 'j = j + 3'],
            ['#FV_conditional_True_x==4 + j', 'if (x!=4):', 'x = 4', 'x = x + j', 'else:', 'x = x + j']]
            ))
