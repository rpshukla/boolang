""" Definitions for all types of objects in boolang
"""


from AST import *
from Environment import Environment
from BoolangError import BoolangRuntimeError


class Function:
    """ Class to represent a boolang function
    """

    expr = Expr    # the actual expression of the function
    variable_list = [] # a list of all variables in the function

    def __repr__(self):
        return "Function of {}, expr: {}".format(self.variable_list, self.expr)


    def __init__(self, **kwargs):
        """ Pass the expression generated by the AST and a list of variables
        """
        self.expr = kwargs['expr']
        self.variable_list = kwargs['variable_list']


    def evaluate(self, inputs):
        """ Evaluates the function at inputs (dictionary) and returns either
            true or false

            inputs: a list of boolean values to be substituted into the
                    function. Should be the correct size
        """
        if len(inputs) != len(self.variable_list):
            raise BoolangRuntimeError('Error: a function requires {} inputs but {} were supplied'.format(len(self.variable_list), len(inputs)))

        # Create a temporary enviroment and store the inputs 
        environment = Environment()
        for i in range(len(inputs)):
            environment.bind(self.variable_list[i], inputs[i])

        return self.expr.evaluate(environment)


    def truth(self):
        """ Return a string of the truth table for the function
        """

        # Get number of variables
        var_count = len(self.variable_list)

        # Iterate over all 2^n combination of n variables
        for i in range(2**var_count):
            inputs = [0] * var_count
            for j in range(len(self.variable_list)):
                # Fill the list from the right first
                inputs[-(j+1)] = (i >> j) & 1

            print(', '.join(map(str, inputs)), end='')
            print(' => ', end='')

            print(int(self.evaluate(inputs)))
