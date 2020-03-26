import os.path
import re
import pkg_resources

from .substitute import substitute_variables
from .unknown import UnknownValue
from .errors import ScriicSyntaxException, ScriicRuntimeException
from .step import Step


class FileRunner:
    """
    Runner for a Scriic file.

    :param file_path: Path to the file to run.
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
            r'RETURN (.+)': self._return
        }

        self._parse()
        print(self.lines)

    def _parse(self):
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
        for param in re.finditer(r'<([a-zA-Z_]\w*?)>', self.title):
            self.params.append(param.group(1))

    def _parse_line(self, line):
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

        :param params: Dictionary of parameters to pass to the script
        :returns: Step instance containing a tree of child steps
        """
        self.sub_runner = None
        self.return_value = None
        if params:
            self.variables = params.copy()
        else:
            self.variables = dict()

        # Check that all parameters have been set
        for param in self.params:
            if param not in self.variables:
                raise MissingParamException(
                    f'{self.file_path} is missing parameter {param}')

        # Run the script
        self.step = Step(*substitute_variables(self.title, params, True))

        for line in self.lines:
            # Call the function chosen during parsing
            line[0](line[1])

        # Check for unfinished SUBs
        if self.sub_runner is not None:
            raise ScriicRuntimeException('Unfinished SUB')

        self.step.returned = self.return_value
        return self.step

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

            self.variables[return_var] = step.returned

    # COMMANDS BEGIN HERE #
    def _do(self, match):
        text = substitute_variables(match.group(1), self.variables)
        self.step.add_child(*text)

    def _set_doing(self, match):
        # Create a step and get its index
        step = self.step.add_child(match.group(2))
        # Set the variable to reference the result of this step
        self.variables[match.group(1)] = UnknownValue(step)

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
