import os.path
import re


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
                        break  # This line must be a code statement

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

    
