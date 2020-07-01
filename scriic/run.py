import os.path
import re

import pkg_resources
from parsy import ParseError

from scriic.errors import ScriicRuntimeException, ScriicSyntaxException
from scriic.instruction import Instruction
from scriic.parser import parse
from scriic.parser.do import Do
from scriic.parser.howto import Parameter
from scriic.parser.letters import Letters
from scriic.parser.repeat import Repeat
from scriic.parser.return_ import Return
from scriic.parser.sub import Sub
from scriic.substitute import substitute_variables
from scriic.value import UnknownValue, Value


class FileRunner:
    """
    Runner for a Scriic file.

    The file will be loaded and parsed as soon as this class is constructed, and can
    then be executed using :meth:`FileRunner.run`. Use the ``required_parameters``
    property to check what parameters must be passed when running.

    :param file_path: Path to the file to run.
    :var parameters: List of parametrs required by this Scriic.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)

        with open(self.file_path) as file:
            try:
                self.title, self.steps = parse(file.read())
            except ParseError as e:
                raise ScriicSyntaxException(self.file_path, str(e)) from e

        self.required_parameters = {
            x.name for x in self.title if isinstance(x, Parameter)
        }

    def run(self, parameters=None):
        """
        Run this file and return a tree of Instructions.

        :param parameters: Dictionary of parameters to pass to the script.
        :returns: Tree of instructions. The root instruction's text will be the title.
        :raises ScriicRuntimeException: A problem was encountered during execution.
        """
        self.variables = parameters or dict()
        self.return_value = None

        given_parameters = set(self.variables.keys())
        missing_parameters = self.required_parameters.difference(given_parameters)
        if len(missing_parameters) > 0:
            raise ScriicRuntimeException(
                self.file_path,
                "Missing one or more parameters: " + ", ".join(missing_parameters),
            )

        title = substitute_variables(self.title, self.variables, self.file_path)
        self.instruction = Instruction(title)
        for step in self.steps:
            self._run_step(step)
        return self.instruction

    def _run_step(self, step):
        """
        :param step: Step to execute.
        :raises ScriicRuntimeException: We do not know how to run this step.
        """
        if isinstance(step, Do):
            self._do(step)
        elif isinstance(step, Sub):
            self._sub(step)
        elif isinstance(step, Repeat):
            self._repeat(step)
        elif isinstance(step, Letters):
            self._letters(step)
        elif isinstance(step, Return):
            self.return_value = substitute_variables(
                step.value, self.variables, self.file_path
            )
        else:
            raise ScriicRuntimeException(self.file_path, f"Unrecognized step: {step}")

    def _set_variable(self, name, value):
        """
        Set a variable value, casting to an instance of Value.

        :param name: Name of the variable to set.
        :param value: Value to set. May or may not already be a Value.
        """
        if type(value) != Value:
            value = Value(value)

        self.variables[name] = value

    # COMMANDS BEGIN HERE #
    def _do(self, step):
        text = substitute_variables(step.text, self.variables, self.file_path)
        child = self.instruction.add_child(text)

        if step.assign_to is not None:
            self._set_variable(step.assign_to, UnknownValue(child))

    def _sub(self, step):
        if step.file.module is not None:
            # Look for file inside a Python package
            path = pkg_resources.resource_filename(step.file.module, step.file.path)
        else:
            # Look for file relative to current scriic
            path = os.path.join(self.dir_path, step.file.path)

        # Build dictionary of parameters
        parameters = {
            parameter.name: substitute_variables(
                parameter.value, self.variables, self.file_path
            )
            for parameter in step.parameters
        }
        # Run the subscriic and add its resulting instruction
        runner = FileRunner(path)
        self.instruction.children.append(runner.run(parameters))

        if step.assign_to is not None:
            if runner.return_value is not None:
                # Add return value into a variable
                self._set_variable(step.assign_to, runner.return_value)
            else:
                raise ScriicRuntimeException(
                    self.file_path,
                    "Expecting a return value from {path}, but one was not given",
                )

    def _return(self, step):
        self.return_value = substitute_variables(
            step.value, self.variables, self.file_path
        )

    def _repeat(self, step):
        if isinstance(step.times, int):
            # Literal number
            times = Value(step.times)
        else:
            # Variable name
            try:
                times = self.variables[step.times]
            except KeyError:
                raise ScriicRuntimeException(
                    self.file_path, "Variable {step.times} does not exist"
                )

            if len(times) > 1:
                # The value has more than the single number we are looking for
                raise ScriicRuntimeException(
                    self.file_path,
                    f"Cannot parse {times} as a number of times to REPEAT",
                )

        if times.is_unknown():
            # We cannot just repeat the instructions because we do not know
            # an exact amount of times
            self._repeat_unknown(step, times[0])
        else:
            try:
                times = int(times[0])
            except ValueError:
                raise ScriicRuntimeException(
                    self.file_path,
                    f"Cannot parse {times} as a number of times to REPEAT",
                )
            else:
                self._repeat_known(step, times)

    def _repeat_known(self, step, times):
        """REPEAT for a known number of times."""
        for i in range(times):
            for block_step in step.steps:
                self._run_step(block_step)

    def _repeat_unknown(self, step, times):
        """REPEAT for an UnknownValue of times."""
        # This index will be the first instruction added inside the loop
        return_to_index = len(self.instruction.children)

        for block_step in step.steps:
            self._run_step(block_step)

        # Add a step telling the user to go back to the start of the loop
        self.instruction.add_child(
            Value(
                "Go to ",
                self.instruction.children[return_to_index],
                " and repeat the number of times from ",
                times.instruction,
            )
        )

    def _letters(self, step):
        substitution = substitute_variables(step.text, self.variables, self.file_path)

        if substitution.is_unknown():
            # We don't know the exact value of the string
            # Ask the user to jump back and repeat for each letter
            self._letters_unknown(step, substitution)
        else:
            # We know the exact value of the string
            # Repeat the instructions directly
            self._letters_known(step, str(substitution))

    def _letters_known(self, step, string):
        """LETTERS for a string we know the exact value of."""
        for letter in string:
            for block_step in step.steps:
                if step.assign_to is not None:
                    self.variables[step.assign_to] = letter
                self._run_step(block_step)

    def _letters_unknown(self, step, string):
        """LETTERS for an unknown string."""
        return_to = self.instruction.add_child(
            Value(
                "Get the first letter of ",
                string,
                ", or the next letter if you are returning from a future instruction",
            )
        )
        if step.assign_to is not None:
            self._set_variable(step.assign_to, UnknownValue(return_to))

        for block_step in step.steps:
            self._run_step(block_step)

        self.instruction.add_child(
            Value(
                "If you haven't yet reached the last letter of ",
                string,
                ", go to ",
                return_to,
            )
        )
