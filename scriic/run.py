import os.path
import re
import pkg_resources

from .substitute import substitute_variables
from .value import Value, UnknownValue
from .errors import ScriicSyntaxException, ScriicRuntimeException
from .step import Step


class FileRunner:
    """
    Runner for a Scriic file.

    The file will be loaded and parsed as soon as this class is constructed.

    :param file_path: Path to the file to run.
    :var params: List of parametrs required by this Scriic.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)

        self.commands = {
            r'DO (.+)': self._do,
            r'SET ([a-zA-Z_]\w*) DOING (.+)': self._set_doing,
            r'SUB (([a-zA-Z_]\w*):)?(\S+)( INTO ([a-zA-Z_]\w*))?': self._sub,
            r'WITH (.+) AS ([a-zA-Z_]\w*)': self._with_as,
            r'GO': self._go,
            r'RETURN (.+)': self._return,
            r'LETTERS ([a-zA-Z_]\w*) IN (.+)': self._letters_in,
            r'REPEAT ((\d+)|([a-zA-Z_]\w*))': self._repeat,
            r'END': self._end
        }

        self._parse()

    def _parse(self):
        """
        Load the file and parse it into self.lines.

        :raises ScriicSyntaxException: One or more lines have invalid syntax.
        """
        self.lines = list()
        self.title = None

        with open(self.file_path) as file:
            for line in file:
                line = line.strip()
                if len(line) == 0:
                    continue  # This line is blank, skip it

                parsed_line = self._parse_line(line)
                if parsed_line is not None:
                    self.lines.append(parsed_line)

        if self.title is None:
            raise ScriicSyntaxException(f'{self.file_path} has no HOWTO')

        # Create list of required parameters based on the title
        self.params = list()
        for param in re.finditer(r'<([a-zA-Z_]\w*?)"?>', self.title):
            self.params.append(param.group(1))

    def _parse_line(self, line):
        """
        Parse a single line.

        :returns: Tuple of (function, regex match), or None.
        :raises ScriicSyntaxException: The line did not match any commands.
        """
        if line.startswith('HOWTO '):
            self.title = line[6:]
            return

        # Find a command which matches this line
        for command, func in self.commands.items():
            match = re.match(command, line)
            if match is not None:
                return func, match

        # No commands matched
        raise ScriicSyntaxException(line)

    def run(self, params=None):
        """
        Run the code and return generated step tree.

        :param params: Dictionary of parameters to pass to the script.
        :returns: Step instance containing a tree of child steps.
        :raises ScriicRuntimeException:
            A problem was encountered during execution.
        """
        self.sub_runner = None
        self.return_value = None
        if params:
            self.variables = params.copy()
        else:
            self.variables = dict()

        # List of functions to call when END is reached
        # There should be one for each open block
        # It is up to the function to remove itself if the block has closed
        # The function may return a line to jump to (for creating loops)
        self.open_blocks = list()

        # Check that all parameters have been set
        for param in self.params:
            if param not in self.variables:
                raise ScriicRuntimeException(
                    f'{self.file_path} is missing parameter {param}')

        # Run the script
        self.step = Step(substitute_variables(self.title, params, True))

        self.current_line = 0
        while self.current_line < len(self.lines):
            # Call the function chosen during parsing
            line = self.lines[self.current_line]
            next_line = line[0](line[1])

            if next_line is not None:
                # The function returned a line number, go to that line
                self.current_line = next_line
            else:
                # Go to the next line
                self.current_line += 1

        # Check for unfinished SUBs
        if self.sub_runner is not None:
            raise ScriicRuntimeException('Unfinished SUB')
        # Check for unclosed blocks
        if len(self.open_blocks) > 0:
            raise ScriicRuntimeException('Missing END')

        self.step.returned = self.return_value
        return self.step

    def _set_variable(self, name, value):
        """
        Set the given variable to the given value.

        If the value is not an instance of Value, it will be converted to one.

        :param name: Name of the variable to set.
        :param value: Value to set.
        """
        if type(value) != Value:
            value = Value(value)

        self.variables[name] = value

    def _run_subscriic(self, params, return_var=None):
        """
        Run self.sub_runner with the given parameters.

        :param params: Parameters to pass to the subscriic
        :param return_var: Variable to store return value in
        """
        # Run the subscriic and save steps
        step = self.sub_runner.run(params)
        self.step.children.append(step)

        if return_var:
            if step.returned is None:
                # We expected the subscriic to have returned something
                raise ScriicRuntimeException(
                    f'{self.sub_runner.file_path} did not return a value')

            self._set_variable(return_var, step.returned)

    # COMMANDS BEGIN HERE #
    def _do(self, match):
        text = substitute_variables(match.group(1), self.variables)
        self.step.add_child(text)

    def _set_doing(self, match):
        # Create a step and get its index
        text = substitute_variables(match.group(2), self.variables)
        step = self.step.add_child(text)
        # Set the variable to reference the result of this step
        self._set_variable(match.group(1), UnknownValue(step))

    def _sub(self, match):
        if self.sub_runner is not None:
            raise ScriicRuntimeException(
                f'{self.file_path}: SUB before GO of previous SUB')

        package_name = match.group(2)
        file_path = match.group(3)
        return_var = match.group(5)

        if package_name is not None:
            # Look for file inside a Python package
            path = pkg_resources.resource_filename(package_name, file_path)
        else:
            # Look for file relative to current scriic
            path = os.path.join(self.dir_path, file_path)

        # Create a runner for the subscriic
        self.sub_runner = FileRunner(path)

        if len(self.sub_runner.params) == 0:
            # This subscriic takes no parameters, run it now
            self._run_subscriic({}, return_var)
            self.sub_runner = None
        else:
            # Parameters need to be given using WITH AS
            self.sub_params = dict()
            self.return_var = return_var

    def _with_as(self, match):
        param = substitute_variables(match.group(1), self.variables)
        self.sub_params[match.group(2)] = param

    def _go(self, match):
        if self.sub_runner is None:
            raise ScriicRuntimeException('Unexpected GO')

        self._run_subscriic(self.sub_params, self.return_var)

        # Remove the subscriic runner now we have finished with it
        self.sub_runner = None
        del self.sub_params
        del self.return_var

    def _return(self, match):
        self.return_value = substitute_variables(
            match.group(1), self.variables)

    def _repeat(self, match):
        if match.group(2):
            # Literal value
            times = Value(match.group(2))
        else:
            # Variable name
            try:
                times = self.variables[match.group(3)]
            except KeyError:
                raise ScriicRuntimeException(
                    f'{self.file_path}: Invalid variable for REPEAT')

            if len(times) > 1:
                # The value has more than the single number we are looking for
                raise ScriicRuntimeException(
                    f'Cannot parse {times} as a number of times for REPEAT')

        if times.is_unknown():
            # We cannot just repeat the instructions because we do not know
            # an exact amount of times
            self._repeat_unknown(times[0])
        else:
            try:
                times = int(times[0])
            except ValueError:
                raise ScriicRuntimeException(
                    f'Cannot parse {times} as a number of times for REPEAT')
            self._repeat_known(times)

    def _repeat_known(self, times):
        """REPEAT for a known number of times."""
        i = 0
        block_start = self.current_line + 1

        def loop():
            nonlocal i
            i += 1
            if i >= times:
                # Reached the target number of times
                self.open_blocks.pop(-1)
                return

            # Loop back to the beginning of the block
            return block_start
        self.open_blocks.append(loop)

    def _repeat_unknown(self, times):
        """REPEAT for an UnknownValue of times."""
        goto_index = len(self.step.children)

        def add_repeat_step():
            # Get the first step inside the block
            if len(self.step.children) > goto_index:
                return_step = self.step.children[goto_index]

                # Add a step telling the user to go back to it
                self.step.add_child(Value(
                    'Go to ', return_step,
                    ' and repeat the number of times from ', times.step
                ))

            # If we don't have a step then the loop is empty

            self.open_blocks.pop(-1)
        self.open_blocks.append(add_repeat_step)

    def _letters_in(self, match):
        var = match.group(1)
        substitution = substitute_variables(match.group(2), self.variables)

        if substitution.is_unknown():
            # We don't know the exact value of the string
            # Ask the user to jump back and repeat for each letter
            self._letters_unknown(var, substitution)
        else:
            # We know the exact value of the string
            # Repeat the instructions directly
            self._letters_known(var, str(substitution))

    def _letters_known(self, var, string):
        """LETTERS IN for a string we know the exact value of."""
        block_start = self.current_line + 1

        i = 0
        self._set_variable(var, string[0])

        def loop():
            nonlocal i
            i += 1
            if i >= len(string):
                # Reached the end of the string
                self.open_blocks.pop(-1)
                return

            self._set_variable(var, string[i])
            # Loop back to the beginning of the block
            return block_start
        self.open_blocks.append(loop)

    def _letters_unknown(self, var, string):
        """LETTERS IN for an unknown string."""
        goto_step = self.step.add_child(Value(
            'Get the first letter of ', string, ', or the next letter '
            'if you are returning from a future step'
        ))
        self._set_variable(var, UnknownValue(goto_step))

        def add_repeat_step():
            self.step.add_child(Value(
                'If you haven\'t yet reached the last letter of ', string,
                ', go to ', goto_step
            ))
            self.open_blocks.pop(-1)
        self.open_blocks.append(add_repeat_step)

    def _end(self, match):
        if len(self.open_blocks) == 0:
            raise ScriicRuntimeException(f'{self.file_path}: Unexpected END')

        # Call the function registered when this block was opened
        return self.open_blocks[-1]()
