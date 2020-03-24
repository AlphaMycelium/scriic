import os.path
import re

from .substitute import substitute_variables


SUPPORTED_TYPES = [
    'str',
    'int',
    'sint',
    'float',
    'sfloat'
]
# Note that 'opt' is also supported


class MetadataException(Exception):
    pass

class ScriicSyntaxException(Exception):
    pass

class MissingParamException(Exception):
    pass


class FileRunner:
    def __init__(self, file_path):
        """
        Runner for a Scriic file.

        :param file_path: Path to the file to run.
        """
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)

        self.code_begins_at = self._get_meta() + 1

    def _get_meta(self):
        """
        Read the metadata from the start of the code and prepare to run.

        :returns: Line number metadata ends on
        """
        self.howto = None
        # Dictionary of param names to types
        self.params = dict()

        in_options = None
        options = None
        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                line = line.strip()

                if in_options:
                    if line == 'END':
                        # End of the options list
                        self.params[in_options] = options
                        in_options = None
                    else:
                        # Add this line as an option
                        options.append(line)
                    continue

                if line.startswith('HOWTO '):
                    if self.howto is not None:
                        raise MetadataException(
                            f'{self.file_path} has more than one HOWTO')

                    self._process_howto(line[6:])

                elif line.startswith('WHERE '):
                    match = re.match(r'WHERE (.+) IS (.+)', line)
                    if not match:
                        raise ScriicSyntaxException(line)

                    param = match.group(1)
                    type = match.group(2)

                    if type in SUPPORTED_TYPES:
                        self.params[param] = type
                    elif type == 'opt':
                        in_options = param
                        options = list()
                    else:
                        raise MetadataException(f'Unknown parameter type {type}')

                else:
                    if len(line) > 0:
                        # This line must be a code statement
                        line_no -= 1
                        break

        if not self.howto:
            raise MetadataException(f'{self.file_path} does not begin with HOWTO')

        for param in self.params:
            if self.params[param] is None:
                raise MetadataException(f'Type for parameter {param} not given')

        return line_no

    def _process_howto(self, howto):
        """
        Process the text of a HOWTO statement into self.params.

        :param howto: The text of the HOWTO statement, without 'HOWTO '
        """
        self.howto = howto

        for param in re.finditer(r'<(.+?)>', howto):
            param_name = param.group(1)
            # We will update the type once we reach a WHERE later
            self.params[param_name] = None

    def run(self, params=None):
        """
        Run the code and return generated steps.

        :param params: Dictionary of parameters to pass to the script
        :returns: List of steps as strings
        """
        if params:
            self.variables = params.copy()
        else:
            self.variables = dict()
        self.steps = list()

        # Check that all parameters have been set
        for param in self.params:
            if not param in self.variables:
                raise MissingParamException(
                    f'{self.file_path} is missing parameter {param}')

        # Run the script
        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                self._run_line(line, line_no)

        return self.steps

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

        if line.startswith('DO '):
            step = substitute_variables(line[3:], self.variables)
            self.steps.append(step)
            return
