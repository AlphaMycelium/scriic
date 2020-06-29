from parsy import *

from scriic.parser.primitives import variable, assignment, newline, text


Import = namedtuple("Import", "module path")
SubParameter = namedtuple("SubParameter", "name value")
Sub = namedtuple("Sub", "file parameters assign_to")


@generate("import path")
def import_path():
    """
    An import path.

    May be in the format:
    - ``python_module:/file/path.scriic``
    - ``/file/path.scriic``
    """
    module = yield (variable << string(":")).optional()
    file_path = yield regex(r"\S+")
    return Import(module, file_path)


@generate("PRM")
def sub_parameter():
    yield string("PRM ")
    parameter = yield assignment
    value = yield text
    return SubParameter(parameter, value)


@generate
def sub_parameters():
    parameters = yield newline >> sub_parameter.sep_by(newline, min=1)
    yield newline << string("GO")
    return parameters


@generate("SUB")
def sub():
    assign_to = yield assignment.optional()
    path = yield string("SUB ") >> import_path
    parameters = yield sub_parameters | success(list())
    return Sub(path, parameters, assign_to)
