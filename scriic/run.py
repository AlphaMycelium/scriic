import os.path
import re

from .substitute import substitute_variables
from .unknown import UnknownValue
from .errors import (
    ScriicSyntaxException,
    MissingMetadataException,
    InvalidMetadataException,
    MissingParamException,
    NoReturnValueException
)
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
            r'SUB (\S+)( INTO ([a-zA-Z_]\w*))?': self._sub,
            r'WITH (.+) AS ([a-zA-Z_]\w*)': self._with_as,
            r'GO': self._go,
            r'RETURN (.+)': self._return
        }

        self.code_begins_at = self._get_meta() + 1

    def _get_meta(self):
        """
        Read the metadata from the start of the code and prepare to run.

        :returns: Line number metadata ends on
        """
        self.title = None

        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                line = line.strip()

                if line.startswith('HOWTO '):
                    if self.title is None:
                        # Store the HOWTO text as the title
                        self.title = line[6:]
                    else:
                        raise InvalidMetadataException(
                            f'{self.file_path} has more than one HOWTO line')

                else:
                    if len(line) > 0:
                        # This must be a code line
                        line_no -= 1
                        break

        # Check that we got all required data
        if self.title is None:
            raise MissingMetadataException(
                f'{self.file_path} does not begin with a HOWTO line')

        # Create a list of required parameters based on the title
        self.params = list()
        for param in re.finditer(r'<([a-zA-Z_]\w*?)>', self.title):
            self.params.append(param.group(1))

        # Return the line metadata stopped at
        return line_no

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

        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                self._run_line(line, line_no)

        # Check for unfinished SUBs
        if self.sub_runner is not None:
            raise ScriicSyntaxException('Unfinished SUB')

        self.step.returned = self.return_value
        return self.step

    def _run_line(self, line, line_no):
        """
        Run one line of code.

        :param line: Text of this line
        :param line_no: Position of this line in the file
        """
        if line_no < self.code_begins_at:
            return  # Skip metadata

        line = line.strip()
        if len(line) == 0:
            return  # This is a blank line, skip it

        # Look for a command which matches this line
        for command, func in self.commands.items():
            # Attempt to match the line with the command regex
            match = re.match(command, line)
            if match:
                func(match)
                return

        # Unknown command
        raise ScriicSyntaxException(line)

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
        # Create a runner for the subscriic
        sub_path = os.path.join(self.dir_path, match.group(1))
        self.sub_runner = FileRunner(sub_path)

        if len(self.sub_runner.params) == 0:
            # This subscriic takes no parameters, run it now
            step = self.sub_runner.run()
            self.step.children.append(step)

            if match.group(3):
                # Store the returned value
                if step.returned is None:
                    raise NoReturnValueException(
                        f'{sub_path} did not return a value')
                self.variables[match.group(3)] = step.returned

            self.sub_runner = None
        else:
            # Parameters need to be given using WITH AS
            self.sub_params = dict()
            self.return_var = match.group(3)

    def _with_as(self, match):
        param = substitute_variables(match.group(1), self.variables)
        self.sub_params[match.group(2)] = param

    def _go(self, match):
        if self.sub_runner is None:
            raise ScriicSyntaxException('Unexpected GO')

        # Run the subscriic and get steps
        step = self.sub_runner.run(self.sub_params)
        self.step.children.append(step)

        if self.return_var:
            if step.returned is None:
                raise NoReturnValueException(
                    f'{self.sub_runner.file_path} did not return a value')
            self.variables[self.return_var] = step.returned

        # Remove the subscriic runner now we have finished with it
        self.sub_runner = None
        del self.sub_params
        del self.return_var

    def _return(self, match):
        self.return_value = substitute_variables(
            match.group(1), self.variables)
